# Copyright (c) 2024 Moritz E. Beber
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.


"""Provide a value object for an agent's thought."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, NamedTuple


class Thought(NamedTuple):
    """Define an agent's thought, an intermediate step in an exchange."""

    subquery: str
    context: Any
    parent: Thought | None = None

    def with_parent(self, parent: Thought) -> Thought:
        """Return a copy of the thought with a parent set."""
        return type(self)(
            subquery=self.subquery,
            context=deepcopy(self.context),
            parent=parent,
        )
