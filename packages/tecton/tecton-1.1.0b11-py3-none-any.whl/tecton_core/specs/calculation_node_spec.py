from abc import ABC
from abc import abstractmethod
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import pypika.functions as fn
from pypika import NULL
from pypika.terms import BasicCriterion
from pypika.terms import Equality
from pypika.terms import Field
from pypika.terms import Term
from pypika.terms import ValueWrapper

from tecton_core import data_types
from tecton_core.data_types import DataType
from tecton_core.data_types import data_type_from_proto
from tecton_core.errors import TectonInternalError
from tecton_core.specs import utils
from tecton_proto.common import calculation_node__client_pb2 as calculation_node_pb2


COMPARISON_OPERATION_TYPE_TO_PYPIKA_EQUALITY: Dict[calculation_node_pb2.OperationType.ValueType, Equality] = {
    calculation_node_pb2.OperationType.EQUALS: Equality.eq,
    calculation_node_pb2.OperationType.NOT_EQUALS: Equality.ne,
    calculation_node_pb2.OperationType.GREATER_THAN: Equality.gt,
    calculation_node_pb2.OperationType.GREATER_THAN_EQUALS: Equality.gte,
    calculation_node_pb2.OperationType.LESS_THAN: Equality.lt,
    calculation_node_pb2.OperationType.LESS_THAN_EQUALS: Equality.lte,
}


@utils.frozen_strict
class AbstractSyntaxTreeNodeSpec(ABC):
    dtype: Optional[DataType]

    @classmethod
    def from_proto(cls, node: calculation_node_pb2.AbstractSyntaxTreeNode) -> "AbstractSyntaxTreeNodeSpec":
        value_type = node.WhichOneof("value")
        if value_type == "literal_value":
            return LiteralValueNodeSpec.from_proto(node)
        elif value_type == "column_reference":
            return ColumnReferenceNodeSpec.from_proto(node)
        elif value_type == "operation":
            return OperationNodeSpec.from_proto(node)
        elif value_type == "date_part":
            return DatePartNodeSpec.from_proto(node)
        else:
            msg = "Unknown AbstractSyntaxTreeNode Type"
            raise TectonInternalError(msg)

    @abstractmethod
    def to_query_term(self, column_reference_resolver: Callable[[str], str]) -> Term:
        raise NotImplementedError


@utils.frozen_strict
class OperationNodeSpec(AbstractSyntaxTreeNodeSpec):
    dtype: DataType
    operation: calculation_node_pb2.OperationType
    operands: List[AbstractSyntaxTreeNodeSpec]

    @classmethod
    def from_proto(cls, proto: calculation_node_pb2.AbstractSyntaxTreeNode) -> "OperationNodeSpec":
        operation_proto = proto.operation
        return cls(
            dtype=data_type_from_proto(proto.dtype),
            operation=operation_proto.operation,
            operands=[AbstractSyntaxTreeNodeSpec.from_proto(operand) for operand in operation_proto.operands],
        )

    def to_query_term(self, column_reference_resolver: Callable[[str], str]) -> Term:
        if self.operation == calculation_node_pb2.OperationType.COALESCE:
            return self._build_coalesce_query(column_reference_resolver)
        elif self.operation in COMPARISON_OPERATION_TYPE_TO_PYPIKA_EQUALITY:
            return self._build_comparison_query(
                column_reference_resolver=column_reference_resolver, comparator_operation=self.operation
            )
        else:
            msg = f"In Calculation sql generation, calculation operation {self.operation.name} not supported."
            raise TectonInternalError(msg)

    def _build_coalesce_query(self, column_reference_resolver: Callable[[str], str]) -> Term:
        if len(self.operands) < 1:
            msg = "Calculation function Coalesce must have at least 1 operand."
            raise TectonInternalError(msg)
        operand_sqls = [operand.to_query_term(column_reference_resolver) for operand in self.operands]
        return fn.Coalesce(*operand_sqls)

    def _build_comparison_query(
        self,
        column_reference_resolver: Callable[[str], str],
        comparator_operation: calculation_node_pb2.OperationType.ValueType,
    ) -> Term:
        if len(self.operands) != 2:
            msg = "Calculation function must have exactly 2 operands."
            raise TectonInternalError(msg)
        left = self.operands[0].to_query_term(column_reference_resolver)
        right = self.operands[1].to_query_term(column_reference_resolver)

        comparator_term = COMPARISON_OPERATION_TYPE_TO_PYPIKA_EQUALITY[comparator_operation]
        return BasicCriterion(comparator_term, left, right)


@utils.frozen_strict
class LiteralValueNodeSpec(AbstractSyntaxTreeNodeSpec):
    dtype: Optional[DataType]
    value: Optional[Union[float, int, bool, str]]

    @classmethod
    def from_proto(cls, proto: calculation_node_pb2.AbstractSyntaxTreeNode) -> "LiteralValueNodeSpec":
        literal_value_proto = proto.literal_value
        value_type = literal_value_proto.WhichOneof("value")
        if value_type == "null_value":
            return cls(dtype=None, value=None)
        else:
            return cls(dtype=data_type_from_proto(proto.dtype), value=getattr(literal_value_proto, value_type))

    def to_query_term(self, column_reference_resolver: Callable[[str], str]) -> Term:
        if self.dtype is None or self.value is None:
            return NULL
        sql = ValueWrapper(self.value)
        if isinstance(self.dtype, data_types.Int64Type):
            sql = fn.Cast(sql, "BIGINT")
        elif isinstance(self.dtype, data_types.Float64Type):
            sql = fn.Cast(sql, "DOUBLE")
        return sql


@utils.frozen_strict
class ColumnReferenceNodeSpec(AbstractSyntaxTreeNodeSpec):
    dtype: DataType
    value: str

    @classmethod
    def from_proto(cls, proto: calculation_node_pb2.AbstractSyntaxTreeNode) -> "ColumnReferenceNodeSpec":
        return cls(dtype=data_type_from_proto(proto.dtype), value=proto.column_reference)

    def to_query_term(self, column_reference_resolver: Callable[[str], str]) -> Term:
        internal_column_name = column_reference_resolver(self.value)
        return Field(internal_column_name)


@utils.frozen_strict
class DatePartNodeSpec(AbstractSyntaxTreeNodeSpec):
    value: calculation_node_pb2.DatePart.ValueType

    @classmethod
    def from_proto(cls, proto: calculation_node_pb2.AbstractSyntaxTreeNode) -> "DatePartNodeSpec":
        return cls(value=proto.date_part, dtype=None)

    def to_query_term(self, column_reference_resolver: Callable[[str], str]) -> Term:
        raise NotImplementedError
