from typing import Dict, Optional, Set, Union
from pydantic import BaseModel, Field, field_validator, ConfigDict

from .sql.enums import AggregationType, Access, JoinType, Operation


class ColumnSchema(BaseModel):
    """Schema defining security rules for a database column."""

    access: Access = Field(default=Access.DENIED)
    allowed_operations: Set[Operation] = Field(default_factory=lambda: {Operation.SELECT})
    allowed_aggregations: Set[AggregationType] = Field(default_factory=set)

    model_config = ConfigDict(validate_assignment=True, arbitrary_types_allowed=True)

    @classmethod
    def create_default(cls, **kwargs) -> "ColumnSchema":
        """Create a default column schema with optional overrides."""
        valid_fields = {k: v for k, v in kwargs.items() if k in cls.model_fields}
        return cls(**valid_fields)


class TableSchema(BaseModel):
    """Schema defining security rules for a database table."""

    columns: Dict[str, ColumnSchema] = Field(default_factory=dict)
    allowed_joins: Dict[str, Set[JoinType]] = Field(default_factory=dict)
    default_allowed_join: Optional[Set[JoinType]] = Field(default_factory=set)

    model_config = ConfigDict(validate_assignment=True, arbitrary_types_allowed=True)

    def get_table_allowed_joins(self, column: str) -> Set[JoinType]:
        """Get join rules for a column, returning default JoinRule if none specified."""
        return self.allowed_joins.get(column, self.default_allowed_join or set())

    @field_validator("allowed_joins", mode="before")
    @classmethod
    def ensure_join_rules(cls, v: Optional[Dict]) -> Dict[str, Set[JoinType]]:
        """Ensures join rules are properly instantiated."""
        if not isinstance(v, dict):
            return {}

        return {k: v[k] if isinstance(v[k], set) else set(v[k] or []) for k in v}

    @field_validator("default_allowed_join", mode="before")
    @classmethod
    def ensure_default_join_rule(
        cls, v: Optional[Union[Dict, Set[JoinType]]]
    ) -> Optional[Set[JoinType]]:
        """Ensures default join rule is properly instantiated."""
        if v is None:
            return None
        if isinstance(v, set):
            return v
        return set(v or [])

    @classmethod
    def create_default(cls, **kwargs) -> "TableSchema":
        """Create a default table schema with optional overrides."""
        valid_fields = {k: v for k, v in kwargs.items() if k in cls.model_fields}
        return cls(**valid_fields)


class SecuritySchema(BaseModel):
    """Schema defining overall security rules for database access."""

    tables: Dict[str, TableSchema] = Field(default_factory=dict)
    max_joins: int = Field(default=3, ge=0)
    allow_subqueries: bool = True
    allow_temp_tables: bool = False  # TODO: Implement temp tables
    max_query_length: Optional[int] = Field(default=None, ge=0)
    sql_injection_protection: bool = True
    forbidden_keywords: Set[str] = Field(
        default_factory=lambda: {
            "TRUNCATE",
            "DROP",
            "DELETE",
            "UPDATE",
            "1=1",
            "ALTER",
            "GRANT",
            "REVOKE",
            "EXECUTE",
            "EXEC",
            "SYSADMIN",
            "DBADMIN",
        }
    )
    access: Optional[Access] = Field(default=None)
    allowed_aggregations: Optional[Set[AggregationType]] = Field(default=None)

    # Default schemas with proper typing
    default_table_security_schema: TableSchema = Field(default_factory=TableSchema)
    default_column_security_schema: ColumnSchema = Field(default_factory=ColumnSchema)

    model_config = ConfigDict(validate_assignment=True, arbitrary_types_allowed=True)

    def __init__(self, **data):
        # Initialize default schemas before parent initialization
        column_fields = {
            "access": data.get("access"),
            "allowed_operations": data.get("allowed_operations"),
            "allowed_aggregations": data.get("allowed_aggregations"),
        }
        # Only include non-None values
        column_fields = {k: v for k, v in column_fields.items() if v is not None}

        # Create default schemas
        if "default_column_security_schema" not in data:
            data["default_column_security_schema"] = ColumnSchema(**column_fields)

        if "default_table_security_schema" not in data:
            table_fields = {
                "columns": {},  # Empty default columns
                "allowed_joins": {},  # Empty default joins
                "default_allowed_join": (
                    # Set default allowed joins only if JOIN is an allowed operation
                    set({JoinType.INNER, JoinType.LEFT})
                    if column_fields.get("allowed_operations")
                    and "JOIN" in column_fields["allowed_operations"]
                    else set()
                ),
            }
            data["default_table_security_schema"] = TableSchema(**table_fields)

        super().__init__(**data)

    def get_prompt(self) -> str:
        """Generate a prompt describing the security constraints."""
        prompt = "Generate an SQL query adhering to the following constraints:\n"
        prompt += f"- Maximum joins allowed: {self.max_joins}\n"
        prompt += f"- Subqueries allowed: {'Yes' if self.allow_subqueries else 'No'}\n"
        prompt += (
            f"- Temporary tables allowed: {'Yes' if self.allow_temp_tables else 'No'}\n"
        )
        prompt += f"- Maximum query length: {self.max_query_length if self.max_query_length else 'Unlimited'}\n"
        prompt += f"- SQL Injection Protection: {'Enabled' if self.sql_injection_protection else 'Disabled'}\n"
        prompt += (
            f"- Forbidden keywords: {', '.join(sorted(self.forbidden_keywords))}\n"
        )
        # TODO: Get this from the default column settings
        # if self.allowed_operations:
        #     prompt += (
        #         f"- Allowed operations: {', '.join(sorted(self.allowed_operations))}\n"
        #     )
        if self.allowed_aggregations:
            prompt += f"- Allowed aggregations: {', '.join(sorted(agg.name for agg in self.allowed_aggregations))}\n"
        if self.access:
            prompt += f"- Default access level: {self.access.name}\n"
        return prompt

    def get_table_schema(self, table_name: str) -> TableSchema:
        """Returns the table schema, or the default if not found."""
        return self.tables.get(table_name, self.default_table_security_schema)

    def get_column_schema(self, table_name: str, column_name: str) -> ColumnSchema:
        """Returns the column schema, or the default if not found."""
        table_schema = self.get_table_schema(table_name)
        return table_schema.columns.get(
            column_name, self.default_column_security_schema
        )

    @field_validator("tables", mode="before")
    @classmethod
    def ensure_table_schemas(cls, v: Union[Dict, None]) -> Dict[str, TableSchema]:
        """Ensures table schemas are properly instantiated."""
        if not isinstance(v, dict):
            return {}

        return {
            k: v[k] if isinstance(v[k], TableSchema) else TableSchema(**(v[k] or {}))
            for k in v
        }
