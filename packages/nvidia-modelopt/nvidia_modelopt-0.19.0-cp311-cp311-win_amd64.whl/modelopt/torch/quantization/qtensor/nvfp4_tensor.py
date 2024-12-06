# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.
"""Not Implemented!"""

from modelopt.torch.quantization.qtensor.base_qtensor import BaseQuantizedTensor

__all__ = ["NVFP4QTensor"]


class NVFP4QTensor(BaseQuantizedTensor):
    """Not Implemented!"""

    @classmethod
    def resmooth_weights_and_get_scales(
        cls,
        *args,
        **kwargs,
    ):
        """Not Implemented!"""
        raise NotImplementedError("NVFP4 quantization is not supported!")

    @classmethod
    def get_weights_scaling_factor(
        cls,
        *args,
        **kwargs,
    ):
        """Not Implemented!"""
        raise NotImplementedError("NVFP4 quantization is not supported!")

    @classmethod
    def get_weights_scaling_factor_2(
        cls,
        *args,
        **kwargs,
    ):
        """Not Implemented!"""
        raise NotImplementedError("NVFP4 quantization is not supported!")

    @classmethod
    def get_activation_scaling_factor(
        cls,
        *args,
        **kwargs,
    ):
        """Not Implemented!"""
        raise NotImplementedError("NVFP4 quantization is not supported!")

    @staticmethod
    def _cast_fp4(
        *args,
        **kwargs,
    ):
        """Not Implemented!"""
        raise NotImplementedError("NVFP4 quantization is not supported!")

    @classmethod
    def quantize(
        cls,
        *args,
        **kwargs,
    ):
        """Not Implemented!"""
        raise NotImplementedError("NVFP4 quantization is not supported!")

    def dequantize(
        self,
        *args,
        **kwargs,
    ):
        """Not Implemented!"""
        raise NotImplementedError("NVFP4 quantization is not supported!")
