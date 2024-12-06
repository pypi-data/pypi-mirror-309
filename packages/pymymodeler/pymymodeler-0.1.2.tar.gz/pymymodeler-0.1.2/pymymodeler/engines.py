from sqlalchemy.engine import create_engine


def get_engine(host: str, user: str, password: str, database: str):
    db_url = f"mysql+pymysql://{user}:{password}@{host}/{database}"
    return create_engine(db_url)
