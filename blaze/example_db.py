import logging

from config import DB_NAME
from modules import BaseDB

logger = logging.getLogger(__name__)

db = BaseDB(DB_NAME, echo=False, reset=False)

msgs = db.get_messages_query("代发")
for msg in msgs:
    print(msg.user_id, msg.text)

db.add_status(msg.message_id, "DAIFA")
