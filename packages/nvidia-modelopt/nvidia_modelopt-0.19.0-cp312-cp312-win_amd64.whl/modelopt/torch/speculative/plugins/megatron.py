# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

"""Plugin to add Medusa support for megatron-core GPT model."""

import warnings
from typing import Optional

import torch
import torch.nn.functional as F
from megatron.core import tensor_parallel
from megatron.core.dist_checkpointing.mapping import ShardedStateDict
from megatron.core.models.gpt import GPTModel
from megatron.core.parallel_state import get_tensor_model_parallel_rank
from megatron.core.tensor_parallel.mappings import gather_from_tensor_model_parallel_region
from megatron.core.transformer.module import MegatronModule

from ..medusa.conversion import MedusaDMRegistry
from ..medusa.medusa_model import MedusaModel


class MedusaLayer(MegatronModule):
    """MedusaLayer impl following TensorRT-LLM's model definition.

    Medusa layer consists of a column parallel linear following a silu.
    """

    def __init__(self, config):
        """Constructor.

        Args:
            config: MCore transformer config
        """
        super().__init__(config=config)

        self.activation_func = F.silu

        self.linear = tensor_parallel.ColumnParallelLinear(
            config.hidden_size,
            config.hidden_size,
            config=config,
            init_method=config.init_method,
            bias=True,
            skip_bias_add=False,
            gather_output=True,
            skip_weight_param_allocation=False,
        )

    def forward(self, x):
        """Forward function."""
        y, _ = self.linear(x)
        return x + self.activation_func(y), None

    def sharded_state_dict(
        self, prefix: str = "", sharded_offsets: tuple = (), metadata: Optional[dict] = None
    ) -> ShardedStateDict:
        """Return MCore sharded_state_dict."""
        return self.linear.sharded_state_dict(f"{prefix}linear.", sharded_offsets, metadata)


class MedusaHead(MegatronModule):
    """MedusaHead impl following TensorRT-LLM's model definition.

    https://github.com/NVIDIA/TensorRT-LLM/blob/main/tensorrt_llm/models/medusa/model.py
    Medusa head consists of several MedusaLayers and an lm_head.
    """

    def __init__(self, config, vocab_size: int, num_layers: int = 1, parallel_output: bool = True):
        """Constructor.

        Args:
            config: MCore transformer config
            vocab_size: vocabulary size
            num_layers: number of Medusa layers
            parallel_output: if False, then all_gather the logits
        """
        super().__init__(config=config)

        self.medusa_layers = torch.nn.ModuleList([MedusaLayer(config) for _ in range(num_layers)])

        self.lm_head = tensor_parallel.ColumnParallelLinear(
            config.hidden_size,
            vocab_size,
            config=config,
            init_method=config.init_method,
            bias=False,
            skip_bias_add=False,
            gather_output=not parallel_output,
            skip_weight_param_allocation=False,
        )

        def load_state_dict_post_hook(module, incompatible_keys):
            incompatible_keys.missing_keys.clear()
            incompatible_keys.unexpected_keys.clear()

        self.register_load_state_dict_post_hook(load_state_dict_post_hook)

    def forward(self, x):
        """Forward function."""
        for layer in self.medusa_layers:
            x, _ = layer(x)
        return self.lm_head(x)

    def sharded_state_dict(
        self, prefix: str = "", sharded_offsets: tuple = (), metadata: dict = None
    ) -> ShardedStateDict:
        """Return MCore sharded_state_dict."""
        assert not sharded_offsets, "Unexpected sharded offsets"
        sharded_state_dict = {}
        layer_prefix = f"{prefix}medusa_layers."
        for i, layer in enumerate(self.medusa_layers):
            state_dict_prefix = f"{layer_prefix}{i}."
            sharded_pp_offset = []
            layer_sharded_state_dict = layer.sharded_state_dict(
                state_dict_prefix, sharded_pp_offset, metadata
            )
            sharded_state_dict.update(layer_sharded_state_dict)
        sharded_state_dict.update(
            self.lm_head.sharded_state_dict(f"{prefix}lm_head.", sharded_offsets, metadata)
        )
        return sharded_state_dict


@MedusaDMRegistry.register({GPTModel: "megatron.core.models.gpt.GPTModel"})
class _DynamicMedusaGPTModel(MedusaModel):
    """A ``megatron.core.models.gpt.GPTModel`` model with dynamic hyperparams."""

    def _setup(self):
        super()._setup()
        self._register_temp_attribute("medusa_report_acc", True)
        self._register_temp_attribute("medusa_freeze_base_model", True)

    def modify(
        self,
        medusa_num_heads=0,
        medusa_num_layers=0,
        medusa_freeze_base_model=True,
        medusa_report_acc=True,
    ):
        """Constructor.

        Args:
            config: MedusaConfig that specifies the medusa head configuration as well as
                    weights of base model and medusa head.
        """
        if self.config.pipeline_model_parallel_size > 1:
            warnings.warn(
                "Pipeline parallelism detected! _DynamicMedusaGPTModel only supports "
                "pipeline parallelism during TensorRT-LLM checkpoint export."
            )
        super().modify(medusa_num_heads=medusa_num_heads, medusa_num_layers=medusa_num_layers)

        self.medusa_report_acc = medusa_report_acc
        self.medusa_freeze_base_model = medusa_freeze_base_model

        # Freeze all parameters
        if self.medusa_freeze_base_model:
            for name, param in self.named_parameters():
                param.requires_grad = False

        if self.post_process:
            self.medusa_heads = torch.nn.ModuleList(
                [
                    MedusaHead(self.config, self.vocab_size, num_layers=self.medusa_num_layers)
                    for _ in range(self.medusa_num_heads)
                ]
            )

    def forward(self, *args, labels: torch.Tensor = None, **kwargs):
        """Forward pass of the Medusa GPTModel.

        Returns:
            torch.Tensor: If labels are provided, then return lm_loss of all heads. Otherwise,
                return the original logits.
        """
        if self.post_process:
            # Set the post_process to False such that the forward will return the hidden_state.
            self.post_process = False
            # Calling parent's forward to get hidden_states
            hidden_states = GPTModel.forward(self, *args, labels=labels, **kwargs)
            # Reset the post_process to True
            self.post_process = True
        else:
            # return GPTModel.forward(self, *args, labels=labels, **kwargs)
            return GPTModel.forward(self, *args, labels=None, **kwargs)

        # Original output logits
        logits, _ = self.output_layer(hidden_states)

        report_acc = self.medusa_report_acc and labels is not None

        acc = []

        # Medusa heads forward. We want to run through all the heads just to make sure all modules
        # are exercised during calibration.
        for i, head in enumerate(self.medusa_heads):
            new_logits, _ = head(hidden_states)

            # If label is not provided, then this is the inference/generation case. We didn't
            # implement fast decoding; hence we want to return the original logits untouched.
            if labels is not None:
                logits = torch.cat((logits, new_logits), dim=0)

            if report_acc:
                seq_len = new_logits.shape[0]
                gathered_logits = gather_from_tensor_model_parallel_region(new_logits)
                medusa_top1 = gathered_logits.transpose(0, 1).argmax(dim=-1)
                medusa_labels = labels[:, (i + 1) * seq_len : (i + 2) * seq_len]
                top1_p = torch.eq(medusa_labels, medusa_top1).sum() / medusa_top1.numel()
                acc.append(top1_p)

        # Return the original logits untouched.
        if labels is None:
            # [s b h] => [b s h]
            return logits.transpose(0, 1).contiguous()

        if report_acc and get_tensor_model_parallel_rank() == 0:
            print("Medusa Training Accuracy: {}".format(acc))

        loss = self.compute_language_model_loss(labels, logits)

        return loss

    def sharded_state_dict(
        self, prefix: str = "", sharded_offsets: tuple = (), metadata: dict = None
    ) -> ShardedStateDict:
        """Override the shared_state_dict to take care medusa_heads."""
        assert not sharded_offsets, "Unexpected sharded offsets"

        sharded_state_dict = GPTModel.sharded_state_dict(self, prefix, sharded_offsets, metadata)

        if not hasattr(self, "medusa_heads") or self.medusa_heads is None:
            return sharded_state_dict

        layer_prefix = f"{prefix}medusa_heads."
        for i, layer in enumerate(self.medusa_heads):
            layer_sharded_state_dict = layer.sharded_state_dict(f"{layer_prefix}{i}.", [], metadata)
            sharded_state_dict.update(layer_sharded_state_dict)
        return sharded_state_dict
