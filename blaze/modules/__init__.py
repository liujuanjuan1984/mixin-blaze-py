from sqlalchemy.orm import declarative_base

Base = declarative_base()

from modules.base import BaseDB
from modules.message import Message
