import json
import logging

from modules import Base
from modules.message import Message
from modules.status import MsgStatus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)


def _check_str_param(param):
    if param is None:
        return ""
    elif type(param) in [dict, list]:
        return json.dumps(param)
    elif type(param) != str:
        try:
            return str(param)
        except:
            return ""
    return param


class BaseDB:
    def __init__(self, db_name, echo, reset):
        # 创建数据库
        engine = create_engine(db_name, echo=echo, connect_args={"check_same_thread": False})
        if reset:
            Base.metadata.drop_all(engine)
        # 创建表
        Base.metadata.create_all(engine)
        # 创建会话
        self.Session = sessionmaker(bind=engine, autoflush=False)
        self.session = self.Session()
        logger.debug(f"init db, name: {db_name}, echo: {echo}, reset: {reset}")

    def __commit(self):
        """Commits the current db.session, does rollback on failure."""
        from sqlalchemy.exc import IntegrityError

        logger.debug("db commit")

        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()

    def add(self, obj):
        """Adds this model to the db (through db.session)"""
        self.session.add(obj)
        self.__commit()
        return self

    def commit(self):
        self.__commit()
        return self

    def delete(self, obj):
        """Deletes this model from the db (through db.session)"""
        self.session.delete(self)
        self.__commit()

    def add_message(self, msgview):
        existed = self.get_message(msgview.message_id)
        if not existed:
            _c = {
                "message_id": msgview.message_id,
                "quote_message_id": msgview.quote_message_id,
                "conversation_id": msgview.conversation_id,
                "user_id": msgview.user_id,
                "text": _check_str_param(msgview.data_decoded),
                "category": msgview.category,
                "timestamp": str(msgview.created_at),
            }
            self.add(Message(_c))
            logger.info(f"add message: {msgview.message_id}")
        else:
            logger.info(f"message already exists: {msgview.message_id}")
        return True

    def get_message(self, message_id):
        return self.session.query(Message).filter(Message.message_id == message_id).first()

    def get_messages(self, user_id):
        return self.session.query(Message).filter(Message.user_id == user_id).all()

    def get_messages_query(self, text_piece):
        return self.session.query(Message).filter(Message.text.like("%" + text_piece + "%")).all()

    def get_messages_status(self, message_id: str, status: str):
        return (
            self.session.query(MsgStatus)
            .filter(MsgStatus.message_id == message_id)
            .filter(MsgStatus.status == status)
            .first()
        )

    def add_status(self, message_id, status: str):
        existed = self.get_messages_status(message_id, status)
        if not existed:
            _c = {
                "message_id": message_id,
                "status": status,
            }
            self.add(MsgStatus(_c))
            logger.info(f"add status: {message_id},{status}")
        else:
            logger.info(f"status already exists: {message_id},{status}")
        return True
