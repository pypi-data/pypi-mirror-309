# Copyright (C) 2023 Patrick Godwin, Cardiff University
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# <https://mozilla.org/MPL/2.0/>.
#
# SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

import os
from typing import Callable


def is_abs_or_url(path: str) -> bool:
    """Check whether a path is absolute or URL-based."""
    if os.path.isabs(path):
        return True
    return "://" in str(path)


def normalize(path: str, *, basename: bool | Callable[[str], bool] = False) -> str:
    """Selectively return the path's basename based on a condition."""
    if (callable(basename) and basename(path)) or basename is True:
        return os.path.basename(path)
    return path
