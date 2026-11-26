# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.plugins import RunStatus


class RunStatusBaseRun(RunStatus):
    """
    RunStatusBaseRun status.
    """

    outputs: dict | None = None
    results: dict | None = None
    service: dict | None = None
