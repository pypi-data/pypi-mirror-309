# SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

"""Code that export quantized Hugging Face models for deployment."""

import json
import tempfile
import traceback
from pathlib import Path
from typing import Any, Dict, Tuple, Union

import torch
import torch.nn as nn

from modelopt import __version__
from modelopt.torch.quantization.qtensor.nvfp4_tensor import NVFP4QTensor

from . import QUANTIZATION_FP8, QUANTIZATION_INT4_AWQ, QUANTIZATION_NVFP4, QUANTIZATION_NVFP4_AWQ
from .layer_utils import (
    get_kv_cache_dtype,
    get_qkv_and_avg_prequant_scale,
    get_quantization_format,
    get_weight_block_size,
    get_weight_scaling_factor,
    get_weight_scaling_factor_2,
    is_attention,
    is_quantlinear,
)
from .model_config import QUANTIZATION_NONE
from .model_config_utils import process_layer_quant_config, to_quantized_weight
from .scaling_factor_utils import (
    convert_state_dict_amax_to_scales,
    get_weights_scaling_factor_and_amax,
    resmooth_and_get_scale_and_amax,
)


def export_hf_checkpoint(
    model: nn.Module,
    dtype: torch.dtype = torch.float16,
    export_dir: Union[Path, str] = tempfile.gettempdir(),
) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    """Exports the torch model to the packed checkpoint with original HF naming and save to the export_dir.

    The packed checkpoint will be consumed by the TensorRT-LLM unified converter.

    Args:
        model: the torch model.
        dtype: the weights data type to export the unquantized layers.
        export_dir: the target export path.

    Returns:
        post_state_dict: Dict containing quantized weights
        quant_config: config information to export hf_quant_cfg.json
        per_layer_quantization: Dict containing layerwise quantization information to export quant_cfg.json
        in mixed_precision case.
    """
    export_dir = Path(export_dir)
    export_dir.mkdir(parents=True, exist_ok=True)

    if dtype != model.config.torch_dtype:
        print(
            f"Warning: Model's original dtype ({model.config.torch_dtype}) differs from target dtype ({dtype}), \
                which may lead to numerical errors."
        )

    # Layer config dict holds quantization format of each layer.
    # It also holds awq_block_size information for applicable layers.
    layer_config_dict = {}
    for name, sub_module in model.model.layers.named_modules():
        if is_attention(sub_module):
            quantization_format = QUANTIZATION_NONE
            for _, sub_submodule in sub_module.named_children():
                if "QuantLinear" in type(sub_submodule).__name__:
                    quantization_format = get_quantization_format(sub_submodule)
                    break
            if quantization_format == QUANTIZATION_FP8:
                # We no longer adjust the amax values for qkv due to accuracy drop in vLLM path
                pass
            elif quantization_format in [QUANTIZATION_INT4_AWQ, QUANTIZATION_NVFP4_AWQ]:
                (
                    avg_prequant_scale,
                    q_prequant_scaling_factor,
                    k_prequant_scaling_factor,
                    v_prequant_scaling_factor,
                ) = get_qkv_and_avg_prequant_scale(sub_module, dtype)

            elif quantization_format == QUANTIZATION_NVFP4:
                # TODO: adjust amax values for NVFP4
                pass

            continue

        if is_quantlinear(sub_module):
            quantization_format = get_quantization_format(sub_module)
            block_size = get_weight_block_size(sub_module)
            weight_scaling_factor_2 = None

            # Construct per layer config dictionary
            layer_config_dict.update(
                {"model.layers." + name + ".quantization": quantization_format}
            )
            layer_config_dict.update({"model.layers." + name + ".awq_block_size": block_size})

            if quantization_format == QUANTIZATION_FP8:
                maxbound = sub_module.weight_quantizer.maxbound

                # Convert amax to float32
                sub_module.weight_quantizer._amax = sub_module.weight_quantizer._amax.to(
                    torch.float32
                )

                if sub_module.weight_quantizer._amax.dim() == 1:
                    weight_scaling_factor = torch.tensor(
                        sub_module.weight_quantizer.amax.item()
                        / sub_module.weight_quantizer.maxbound
                    )
                else:
                    # Per-channel amax
                    weight_scaling_factor = torch.tensor(
                        sub_module.weight_quantizer.amax / sub_module.weight_quantizer.maxbound
                    )
                sub_module.weight_scale = weight_scaling_factor

                if hasattr(sub_module.input_quantizer, "_amax"):
                    sub_module.input_quantizer._amax = sub_module.input_quantizer._amax.to(
                        torch.float32
                    )

                    sub_module.input_scale = (
                        sub_module.input_quantizer.export_amax().to(torch.float32)
                        / sub_module.input_quantizer.maxbound
                    )

                if hasattr(sub_module.output_quantizer, "_amax"):
                    sub_module.output_quantizer._amax = sub_module.output_quantizer._amax.to(
                        torch.float32
                    )

            elif quantization_format in [QUANTIZATION_INT4_AWQ, QUANTIZATION_NVFP4_AWQ]:
                resmooth_func = (
                    NVFP4QTensor.resmooth_weights_and_get_scales
                    if quantization_format == QUANTIZATION_NVFP4_AWQ
                    else resmooth_and_get_scale_and_amax
                )

                for key in ["q", "k", "v"]:
                    if key in name:
                        prequant_scaling_factor = {
                            "q": q_prequant_scaling_factor,
                            "k": k_prequant_scaling_factor,
                            "v": v_prequant_scaling_factor,
                        }[key]

                        new_weight, weight_scaling_factor, _, scale_or_amax = resmooth_func(
                            merged_weights=sub_module.weight.to(dtype),
                            pre_quant_scales=[prequant_scaling_factor],
                            ranks=1,
                            group_size=block_size,
                            avg_pre_quant_scale=avg_prequant_scale,
                        )

                        if quantization_format == QUANTIZATION_NVFP4_AWQ:
                            # scale_or_amax contains weight_scaling_factor_2 in this case
                            weight_scaling_factor_2 = scale_or_amax
                            sub_module.weight_quantizer._amax = weight_scaling_factor
                            # Scale or amax contains weight_scaling_factor_2 in this case
                            sub_module.register_buffer("weight_scale_2", weight_scaling_factor_2)
                            sub_module.input_quantizer.amax.copy_(
                                NVFP4QTensor.get_activation_scaling_factor(
                                    sub_module.input_quantizer
                                )
                            )
                        else:
                            # scale_or_amax  contains weight_amax in this case
                            sub_module.weight_quantizer._amax = scale_or_amax

                        sub_module.input_quantizer.pre_quant_scale.copy_(avg_prequant_scale)
                        sub_module.weight = nn.Parameter(new_weight, requires_grad=False)
                        break

                else:
                    weight_scaling_factor = get_weight_scaling_factor(sub_module)
                    weight_scaling_factor_2 = None
                    if quantization_format == QUANTIZATION_NVFP4_AWQ:
                        weight_scaling_factor_2 = get_weight_scaling_factor_2(sub_module)
                        # We do not scale amax values during postprocessing for NVFP4_AWQ.
                        maxbound = 1.0
                        # Record quantized weight_scaling_factor in weight_quantizer._amax
                        sub_module.weight_quantizer._amax = weight_scaling_factor

                        # Register weight_scale_2
                        sub_module.register_buffer(
                            "weight_scale_2",
                            weight_scaling_factor_2.reshape(1),
                        )
                        # Record activation_scaling_factor in input_quantizer._amax
                        sub_module.input_quantizer.amax.copy_(
                            NVFP4QTensor.get_activation_scaling_factor(sub_module.input_quantizer)
                        )
                    else:
                        # INT4_AWQ scales quantizer amax values using maxbound during postprocessing
                        maxbound = sub_module.weight_quantizer.maxbound
                        _, sub_module.weight_quantizer._amax = get_weights_scaling_factor_and_amax(
                            sub_module.weight, block_size
                        )

            elif quantization_format == QUANTIZATION_NVFP4:
                # We do not further scale the scaling factors for NVFP4, as the scales are directly recorded in amax
                maxbound = 1.0

                # Global weight scale stored as fp32
                weight_scaling_factor_2 = NVFP4QTensor.get_weights_scaling_factor_2(
                    sub_module.weight
                ).to(torch.float32)
                sub_module.register_buffer(
                    "weight_scale_2",
                    weight_scaling_factor_2,
                )

                # Compute per_block scaling factor
                weight_scaling_factor = NVFP4QTensor.get_weights_scaling_factor(
                    sub_module.weight, block_size
                )
                sub_module.weight_quantizer._amax = weight_scaling_factor

                # Compute activation scaling factor
                sub_module.input_quantizer._amax = NVFP4QTensor.get_activation_scaling_factor(
                    sub_module.input_quantizer
                )

            # Check if quantization format is None, to support auto_quant
            if quantization_format != QUANTIZATION_NONE:
                quantized_weight = to_quantized_weight(
                    sub_module.weight.to(dtype),
                    weight_scaling_factor,
                    quantization_format,  # type:ignore [arg-type]
                    weight_scaling_factor_2,
                    block_size,
                )
                sub_module.weight = nn.Parameter(quantized_weight, requires_grad=False)

            # Find kv cache quant format
            kv_cache_format = get_kv_cache_dtype(sub_module)

    quantized_state_dict = model.state_dict()

    # Process per layer quantization config dict
    per_layer_quantization = process_layer_quant_config(layer_config_dict)

    # Convert the amax to scales
    if not per_layer_quantization:
        layers_quant_config = quantization_format
    else:
        layers_quant_config = layer_config_dict
    post_state_dict = convert_state_dict_amax_to_scales(
        quantized_state_dict, maxbound, layers_quant_config
    )

    # Create the quantization config
    # TODO: add support for customized mixed precision config
    quant_config: Dict[str, Any] = {
        "producer": {
            "name": "modelopt",
            "version": __version__,
        },
        "quantization": {"quant_algo": None, "kv_cache_quant_algo": None},
    }

    if quantization_format == "fp8":
        quant_config["quantization"].update({"quant_algo": "FP8"})
        # TODO: add info about per-channel weight scale and dynamic per token input scale
    elif quantization_format == "int4_awq":
        quant_config["quantization"].update(
            {
                "quant_algo": "W4A16_AWQ",
                "group_size": block_size,
                "has_zero_point": False,
                "pre_quant_scale": True,
                "exclude_modules": ["lm_head"],
            }
        )
    elif quantization_format == "nvfp4":
        quant_config["quantization"].update(
            {
                "quant_algo": "NVFP4",
                "group_size": block_size,
                "exclude_modules": ["lm_head"],
            }
        )
    elif quantization_format == "nvfp4_awq":
        quant_config["quantization"].update(
            {
                "quant_algo": "NVFP4_AWQ",
                "group_size": block_size,
                "has_zero_point": False,
                "pre_quant_scale": True,
                "exclude_modules": ["lm_head"],
            }
        )
    else:
        quant_config["quantization"].update(
            {
                "quant_algo": (
                    quantization_format if quantization_format != QUANTIZATION_NONE else None
                ),
            }
        )

    if kv_cache_format is not None:
        quant_config["quantization"].update(
            {
                "kv_cache_quant_algo": kv_cache_format,
            }
        )

    return post_state_dict, quant_config, per_layer_quantization


def export_hf(
    model: nn.Module,
    dtype: torch.dtype = torch.float16,
    export_dir: Union[Path, str] = tempfile.gettempdir(),
):
    """Exports the torch model to unified checkpoint and saves to export_dir.

    Args:
        model: the torch model.
        dtype: the weights data type to export the unquantized layers.
        export_dir: the target export path.


    """
    try:
        post_state_dict, hf_quant_config, per_layer_quantization = export_hf_checkpoint(
            model, dtype=dtype, export_dir=export_dir
        )

        # If auto_quant is used, save per layer quantization information in quant_cfg.json
        if per_layer_quantization:
            # Update auto quant related information in quantization.json
            per_layer_quantization["kv_cache_quant_algo"] = hf_quant_config["quantization"][
                "kv_cache_quant_algo"
            ]

            # Update auto quant related informaion in hf_quant_config.json
            # We remove group_size, has_zero_point and pre_quant_scale information from config.json
            hf_quant_config["quantization"] = {
                k: per_layer_quantization[k] for k in ("quant_algo", "kv_cache_quant_algo")
            }

            with open(f"{export_dir}/quant_cfg.json", "w") as file:
                json.dump(per_layer_quantization, file, indent=4)

        # Save config
        with open(f"{export_dir}/hf_quant_config.json", "w") as file:
            json.dump(hf_quant_config, file, indent=4)

        # Save model
        model.save_pretrained(export_dir, state_dict=post_state_dict)

    except Exception as e:
        fallback_model_path = export_dir / "modelopt_model.pth"
        torch.save(model.state_dict(), fallback_model_path)
        print(
            "Cannot export model to the model_config. The modelopt-optimized model state_dict"
            f" (including the quantization factors) is saved to {fallback_model_path} using"
            " torch.save for further inspection."
        )
        print(f"Detailed export error: {e}")
        traceback.print_exc()
