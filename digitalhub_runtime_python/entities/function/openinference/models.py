# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class TensorDatatype(Enum):
    """
    Tensor data types supported.
    """

    BOOL = "BOOL"
    BYTES = "BYTES"
    UINT8 = "UINT8"
    INT8 = "INT8"
    UINT16 = "UINT16"
    INT16 = "INT16"
    UINT32 = "UINT32"
    INT32 = "INT32"
    UINT64 = "UINT64"
    INT64 = "INT64"
    FP16 = "FP16"
    FP32 = "FP32"
    FP64 = "FP64"


class TensorValidator(BaseModel):
    """
    Tensor params.
    """

    model_config = ConfigDict(use_enum_values=True)

    name: str = None
    "Tensor name."

    shape: list[int] = Field(default_factory=list)
    "Tensor shape."

    datatype: TensorDatatype = Field(default=TensorDatatype.FP32.value)
    "Tensor data type."
