# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import sys


def get_current_python_version() -> str:
    """Return the current Python version in the runtime's version format."""
    return f"PYTHON{sys.version_info.major}_{sys.version_info.minor}"
