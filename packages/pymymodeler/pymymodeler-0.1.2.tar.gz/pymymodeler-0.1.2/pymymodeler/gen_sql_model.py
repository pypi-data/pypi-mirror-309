import subprocess
from pymymodeler import log


def generate_sqlalchemy_models(
    host: str,
    user: str,
    password: str,
    database: str,
    output_file: str = "sql_models.py",
):
    command = [
        "sqlacodegen_v2",
        f"mysql+pymysql://{user}:{password}@{host}/{database}",
        "--outfile",
        output_file,
    ]
    try:
        subprocess.run(command, check=True)
        log.info(f"SQLAlchemyモデルが '{output_file}' に生成されました。")
    except subprocess.CalledProcessError as e:
        log.exception(f"モデル生成に失敗しました: {e}")
        raise
