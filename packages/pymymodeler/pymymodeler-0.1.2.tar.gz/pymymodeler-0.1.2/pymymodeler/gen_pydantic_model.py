import os
from sqlalchemy import MetaData, Enum, inspect
from sqlalchemy.exc import SQLAlchemyError
from pymymodeler import log
from pymymodeler.engines import get_engine


def generate_pydantic_models(
    host: str,
    user: str,
    password: str,
    database: str,
    output_file: str = "pydantic_models.py",
):
    try:
        engine = get_engine(host, user, password, database)
        pydantic_code = "from pydantic import BaseModel, Field\nfrom typing import Optional, Literal\n\n"
        metadata = MetaData()
        metadata.reflect(bind=engine)

        # デフォルト値を取得するためのインスペクタ
        inspector = inspect(engine)

        # `pydantic_models.py` が存在しない場合は作成
        if not os.path.exists(output_file):
            log.info(f"Creating new file: {output_file}")
            open(output_file, "w").close()

        # 各テーブルのスキーマ情報を取得して Pydantic モデルを生成
        for table_name, table in metadata.tables.items():
            pydantic_code += f"class {table_name.capitalize()}Base(BaseModel):\n"

            # テーブルのカラム情報を取得
            columns_info = inspector.get_columns(table_name)

            for column in table.columns:
                col_name = column.name
                col_type = column.type
                is_nullable = column.nullable
                default_value = None

                # デフォルト値を取得
                for col_info in columns_info:
                    if col_info["name"] == col_name:
                        default_value = col_info.get("default", None)
                        break

                # AUTO_INCREMENT チェック：整数型かつ `autoincrement` が True の場合のみ適用
                is_integer_type = col_type.__class__.__name__ in [
                    "INTEGER",
                    "SMALLINT",
                    "TINYINT",
                    "MEDIUMINT",
                    "BIGINT",
                ]
                is_autoincrement = column.autoincrement and is_integer_type

                if is_autoincrement:
                    field_type = "Optional[int]"
                    pydantic_code += f"    {col_name}: {field_type} = Field(default=None, description='Auto-incrementing ID column')\n"
                    continue

                # 型のマッピング
                if is_integer_type:
                    field_type = "int"
                elif col_type.__class__.__name__ in [
                    "VARCHAR",
                    "TEXT",
                    "CHAR",
                    "LONGTEXT",
                    "MEDIUMTEXT",
                ]:
                    field_type = "str"
                elif col_type.__class__.__name__ in [
                    "FLOAT",
                    "DOUBLE",
                    "REAL",
                    "DECIMAL",
                    "NUMERIC",
                ]:
                    field_type = "float"
                elif col_type.__class__.__name__ == "BOOLEAN":
                    field_type = "bool"
                elif col_type.__class__.__name__ == "DATETIME":
                    field_type = "str"
                elif col_type.__class__.__name__ == "DATE":
                    field_type = "str"
                elif col_type.__class__.__name__ == "TIME":
                    field_type = "str"
                elif col_type.__class__.__name__ == "TIMESTAMP":
                    field_type = "str"
                elif isinstance(col_type, Enum):
                    enum_values = col_type.enums
                    enum_values_repr = ", ".join(
                        [f"'{value}'" for value in enum_values]
                    )
                    field_type = f"Literal[{enum_values_repr}]"
                else:
                    field_type = "str"

                # Optional 型の設定
                if is_nullable:
                    field_type = f"Optional[{field_type}]"

                # Field の設定
                if default_value is not None:
                    pydantic_code += f"    {col_name}: {field_type} = Field(default={repr(default_value)}, description='Column: {col_name}')\n"
                else:
                    pydantic_code += f"    {col_name}: {field_type} = Field(description='Column: {col_name}')\n"

            pydantic_code += "\n"

        # `pydantic_models.py` に書き込む
        with open(output_file, "w") as f:
            f.write(pydantic_code)

        log.info(f"Pydanticモデルが '{output_file}' に生成されました。")

    except SQLAlchemyError as e:
        log.exception(f"Failed to generate Pydantic models: {e}")
        raise
