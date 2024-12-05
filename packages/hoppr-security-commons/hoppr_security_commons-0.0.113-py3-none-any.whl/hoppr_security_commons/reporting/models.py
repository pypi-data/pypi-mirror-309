"""The available reporting formats."""
# This file is part of hoppr-cop
#
# Licensed under the MIT License;
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://opensource.org/licenses/MIT
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# Copyright (c) 2022 Lockheed Martin Corporation
from __future__ import annotations

from enum import Enum


class ReportFormat(Enum):
    """The available reporting formats."""

    TABLE = "table"
    HTML = "html"
    CYCLONE_DX = "cyclone_dx"
    GITLAB = "gitlab"
