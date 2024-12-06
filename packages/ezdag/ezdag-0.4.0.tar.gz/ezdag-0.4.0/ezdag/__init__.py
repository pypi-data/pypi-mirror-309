# Copyright (C) 2022 Patrick Godwin
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# <https://mozilla.org/MPL/2.0/>.
#
# SPDX-License-Identifier: MPL-2.0

from .dags import DAG as DAG
from .layers import Layer as Layer
from .layers import Node as Node
from .options import Argument as Argument
from .options import Option as Option

try:
    from ._version import version as __version__
except ModuleNotFoundError:  # development mode
    __version__ = ""
