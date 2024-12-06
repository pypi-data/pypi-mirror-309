from sqlmodel import SQLModel, Field, create_engine
from sqlalchemy import inspect
from typing import Dict, Any, Type


class SqlModelBuilder:
    def __init__(self, database_url: str, table_name: str):
        self.database_url = database_url
        self.table_name = table_name
        self.engine = create_engine(self.database_url)
        self.inspector = inspect(self.engine)

    def build_model(self) -> Type[SQLModel]:
        columns = self.get_table_columns()
        if not columns:
            raise ValueError(f"Table '{self.table_name}' not found in the database.")

        model_fields = self.parse_columns_to_fields(columns)
        model_name = self.table2model(self.table_name)

        # Dynamically create the model
        model = type(
            model_name,
            (SQLModel,),
            model_fields
        )
        return model

    def get_table_columns(self) -> list:
        """Retrieve column information from the database table."""
        if self.table_name not in self.inspector.get_table_names():
            return []
        return self.inspector.get_columns(self.table_name)

    @staticmethod
    def parse_columns_to_fields(columns: list) -> Dict[str, Any]:
        """Convert database columns to SQLModel Field definitions."""
        fields = {"__tablename__": columns[0]["table"]}
        for column in columns:
            name = column["name"]
            type_ = column["type"]
            nullable = column["nullable"]
            default = column["default"]
            primary_key = column["primary_key"]

            fields[name] = Field(default=default, nullable=nullable, primary_key=primary_key, sa_column_args={"type_": type_})
        return fields

    @staticmethod
    def table2model(table_name: str) -> str:
        """Convert table name to PascalCase model name."""
        return "".join(word.capitalize() for word in table_name.split("_"))


# Example Usage
#if __name__ == "__main__":
#    DATABASE_URL = "sqlite:///example.db"  # Replace with your database URL
#    TABLE_NAME = "example_table"

#    builder = SqlModelBuilder(DATABASE_URL, TABLE_NAME)
#    dynamic_model = builder.build_model()

#    print(dynamic_model)
#    # Use the dynamically created model in queries