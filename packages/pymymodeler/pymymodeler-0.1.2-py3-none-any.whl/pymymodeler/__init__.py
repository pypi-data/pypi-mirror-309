import logging

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

from .gen_pydantic_model import generate_pydantic_models
from .gen_sql_model import generate_sqlalchemy_models

__all__ = ["generate_sqlalchemy_models", "generate_pydantic_models"]

__varsion__ = "0.1.2"
