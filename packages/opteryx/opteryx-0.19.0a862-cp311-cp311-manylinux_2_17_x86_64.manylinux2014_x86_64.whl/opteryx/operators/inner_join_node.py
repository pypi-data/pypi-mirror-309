# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Inner Join Node

This is a SQL Query Execution Plan Node.

PyArrow has a good LEFT JOIN implementation, but it errors when the
relations being joined contain STRUCT or ARRAY columns, this is true
for all of the JOIN types, however we've only written our own INNER
and LEFT JOINs.

It is comparible performance to the PyArrow INNER JOIN, in benchmarks
sometimes native is faster, sometimes PyArrow is faster. Generally
PyArrow is more forgiving when the relations are the "wrong" way around
(unoptimized order) but native is faster for well-ordered relations, as
we intend to take steps to help ensure relations are well-ordered, this
should work in our favour.

This is a hash join, this is completely rewritten from the earlier
pyarrow_ops implementation which was a variation of a sort-merge join.
"""

import pyarrow
from pyarrow import Table

from opteryx import EOS
from opteryx.compiled.structures.hash_table import hash_join_map
from opteryx.models import QueryProperties
from opteryx.utils.arrow import align_tables

from . import JoinNode


def inner_join_with_preprocessed_left_side(left_relation, right_relation, join_columns, hash_table):
    """
    Perform an INNER JOIN using a preprocessed hash table from the left relation.

    Parameters:
        left_relation: The preprocessed left pyarrow.Table.
        right_relation: The right pyarrow.Table to join.
        join_columns: A list of column names to join on.
        hash_table: The preprocessed hash table from the left table.

    Returns:
        A tuple containing lists of matching row indices from the left and right relations.
    """
    left_indexes = []
    right_indexes = []

    right_hash = hash_join_map(right_relation, join_columns)

    for h, right_rows in right_hash.hash_table.items():
        left_rows = hash_table.get(h)
        if left_rows is None:
            continue
        for l in left_rows:
            for r in right_rows:
                left_indexes.append(l)
                right_indexes.append(r)

    return align_tables(right_relation, left_relation, right_indexes, left_indexes)


class InnerJoinNode(JoinNode):
    def __init__(self, properties: QueryProperties, **parameters):
        JoinNode.__init__(self, properties=properties, **parameters)
        self._join_type = parameters["type"]
        self._on = parameters.get("on")
        self._using = parameters.get("using")

        self._left_columns = parameters.get("left_columns")
        self._left_relation = parameters.get("left_relation_names")

        self._right_columns = parameters.get("right_columns")
        self._right_relation = parameters.get("right_relation_names")

        self.stream = "left"
        self.left_buffer = []
        self.left_hash = None

    @classmethod
    def from_json(cls, json_obj: str) -> "BasePlanNode":  # pragma: no cover
        raise NotImplementedError()

    @property
    def name(self):  # pragma: no cover
        return "Inner Join"

    @property
    def config(self):  # pragma: no cover
        return ""

    def execute(self, morsel: Table) -> Table:
        if self.stream == "left":
            if morsel == EOS:
                self.stream = "right"
                self.left_relation = pyarrow.concat_tables(self.left_buffer, promote_options="none")
                self.left_buffer.clear()

                # in place until #1295 resolved
                if self._left_columns[0] not in self.left_relation.column_names:
                    self._right_columns, self._left_columns = (
                        self._left_columns,
                        self._right_columns,
                    )

                self.left_hash = hash_join_map(self.left_relation, self._left_columns)
            else:
                self.left_buffer.append(morsel)
            return None

        if morsel == EOS:
            return EOS

        # do the join
        new_morsel = inner_join_with_preprocessed_left_side(
            left_relation=self.left_relation,
            right_relation=morsel,
            join_columns=self._right_columns,
            hash_table=self.left_hash,
        )

        return new_morsel
