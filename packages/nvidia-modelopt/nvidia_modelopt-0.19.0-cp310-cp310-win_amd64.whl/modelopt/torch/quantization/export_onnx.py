# SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

"""Utility to export a quantized torch model to quantized ONNX."""

import torch
import torch._C._onnx as _C_onnx

onnx_dtype_map = {
    "Float": _C_onnx.TensorProtoDataType.FLOAT,
    "Half": _C_onnx.TensorProtoDataType.FLOAT16,
    "BFloat16": _C_onnx.TensorProtoDataType.BFLOAT16,
}

torch_dtype_map = {"Float": torch.float32, "Half": torch.float16, "BFloat16": torch.bfloat16}


def export_int8(
    g: torch.onnx._internal.jit_utils.GraphContext,
    inputs: torch.Value,
    amax: torch.Tensor,
    num_bits: int,
    unsigned: bool,
    narrow_range: bool,
    trt_high_precision_dtype: str,
):
    """Export quantized model to INT8 ONNX."""
    assert num_bits == 8, "Only INT8 ONNX export is supported for now."
    output_shape = torch.onnx.symbolic_helper._get_tensor_sizes(inputs)
    maxbound = (1 << (num_bits - 1 + int(unsigned))) - 1

    if amax.numel() == 1:
        zero_point, axis = torch.tensor(0.0, device=amax.device), None
    else:
        amax_init_shape = amax.shape
        amax = amax.squeeze().data
        assert len(amax.shape) == 1, "ONNX does not support multi-axis quantization."
        zero_point = torch.zeros_like(amax, dtype=torch.int32).data
        axis = list(amax_init_shape).index(list(amax.shape)[0])

    zero_point = g.op("Constant", value_t=zero_point.to(torch_dtype_map[trt_high_precision_dtype]))

    if not unsigned:
        assert not narrow_range, "ONNX does not support unsigned narrow range INT8."
        zero_point = g.op("Cast", zero_point, to_i=_C_onnx.TensorProtoDataType.INT8)
    else:
        zero_point = g.op("Cast", zero_point, to_i=_C_onnx.TensorProtoDataType.UINT8)

    amax = amax.to(torch_dtype_map[trt_high_precision_dtype])
    scale = amax / maxbound
    scale.masked_fill_(scale == 0, 1.0)
    scale = g.op("Constant", value_t=scale)

    input_type = inputs.type().scalarType()

    assert (
        trt_high_precision_dtype == input_type or trt_high_precision_dtype == "Float"
    ), "TRT StronglyType requires both weights and amax to be in the BF16/FP16, or the QDQ in Float."

    # custom ops, so cast the input if needed.
    if trt_high_precision_dtype != input_type:
        inputs = g.op("Cast", inputs, to_i=onnx_dtype_map[trt_high_precision_dtype])
    quantized = g.op("QuantizeLinear", inputs, scale, zero_point, axis_i=axis)
    out = g.op("DequantizeLinear", quantized, scale, zero_point, axis_i=axis).setType(
        inputs.type().with_dtype(torch_dtype_map[trt_high_precision_dtype]).with_sizes(output_shape)
    )

    # custom ops, so cast the output if needed.
    if trt_high_precision_dtype != input_type:
        inputs = g.op("Cast", inputs, to_i=onnx_dtype_map[input_type])

    return out


def _fp8_quantize(
    g: torch.onnx._internal.jit_utils.GraphContext,
    inputs: torch.Value,
    scale_inv: float,
    trt_high_precision_dtype: str,
):
    """Helper Function for Quantization."""
    output_shape = torch.onnx.symbolic_helper._get_tensor_sizes(inputs)

    # TRT StronglyType only supports FP16 QDQs
    # custom ops, so cast the input if needed.
    input_type = inputs.type().scalarType()
    assert (
        trt_high_precision_dtype == input_type or trt_high_precision_dtype == "Float"
    ), "TRT StronglyType requires both weights and amax to be in the BF16/FP16, or the QDQ in Float."
    if trt_high_precision_dtype != input_type:
        inputs = g.op("Cast", inputs, to_i=onnx_dtype_map[trt_high_precision_dtype])

    scale = g.op(
        "Constant",
        value_t=torch.tensor(scale_inv).to(torch_dtype_map[trt_high_precision_dtype]),
    )
    q_op = g.op("trt::TRT_FP8QuantizeLinear", inputs, scale).setType(
        inputs.type().with_dtype(torch.uint8).with_sizes(output_shape)
    )
    return q_op


def _fp8_dequantize(
    g: torch.onnx._internal.jit_utils.GraphContext,
    inputs: torch.Value,
    scale_inv: float,
    trt_high_precision_dtype: str = "Float",
    otype: str = None,
):
    """Helper Function for Dequantization."""
    output_shape = torch.onnx.symbolic_helper._get_tensor_sizes(inputs)
    assert (
        trt_high_precision_dtype == otype or trt_high_precision_dtype == "Float"
    ), "TRT StronglyType requires both weights and amax to be in the BF16/FP16, or the QDQ in Float."
    scale = g.op(
        "Constant",
        value_t=torch.tensor(scale_inv, dtype=torch_dtype_map[otype]),
    )
    out = g.op("trt::TRT_FP8DequantizeLinear", inputs, scale).setType(
        inputs.type().with_dtype(torch_dtype_map[trt_high_precision_dtype]).with_sizes(output_shape)
    )

    # DQ outputs are currently constrained to FP32 due to a similar limitation in ORT
    # custom ops, so cast the output if needed.
    if trt_high_precision_dtype != otype:
        out = g.op("Cast", out, to_i=onnx_dtype_map[otype])
    return out


def export_fp8(
    g: torch.onnx._internal.jit_utils.GraphContext,
    inputs: torch.Value,
    amax: float,
    trt_high_precision_dtype: str,
):
    """Export quantized model to FP8 ONNX."""
    if amax is None:
        scale = 1.0
    else:
        scale = 448.0 / float(amax)
    otype = inputs.type().scalarType()
    q_tensor = _fp8_quantize(g, inputs, 1.0 / scale, trt_high_precision_dtype)
    return _fp8_dequantize(g, q_tensor, 1.0 / scale, trt_high_precision_dtype, otype)
