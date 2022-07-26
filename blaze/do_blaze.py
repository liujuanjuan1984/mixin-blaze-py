import datetime
import logging

from config import DB_NAME, MIXIN_KEYSTORE
from mixinsdk.clients.blaze_client import BlazeClient
from mixinsdk.clients.user_config import AppConfig
from mixinsdk.types.message import MessageView
from modules import BaseDB

logger = logging.getLogger(__name__)


class BlazeBot:
    def __init__(self, db_name, mixin_keystore):
        self.config = AppConfig.from_payload(mixin_keystore)
        self.db = BaseDB(db_name, echo=False, reset=False)


def message_handle_error_callback(error, details):
    logger.error("===== error_callback =====")
    logger.error(f"error: {error}")
    logger.error(f"details: {details}")


async def message_handle(message):
    global bot
    action = message["action"]

    if action == "ACKNOWLEDGE_MESSAGE_RECEIPT":
        # logger.info("Mixin blaze server: received the message")
        return

    if action == "LIST_PENDING_MESSAGES":
        # logger.info("Mixin blaze server: list pending message")
        return

    if action == "ERROR":
        logger.warning(message["error"])
        await bot.blaze.echo(msgview.message_id)
        return

    if action != "CREATE_MESSAGE":
        await bot.blaze.echo(msgview.message_id)
        return

    error = message.get("error")
    if error:
        logger.info(str(error))
        await bot.blaze.echo(msgview.message_id)
        return

    msgview = MessageView.from_dict(message["data"])

    # 和 server 有 -8 时差。也就是只处理 1 小时内的 message
    if msgview.created_at <= datetime.datetime.now() + datetime.timedelta(hours=-9):
        await bot.blaze.echo(msgview.message_id)
        return

    if msgview.type != "message":
        await bot.blaze.echo(msgview.message_id)
        return

    if msgview.conversation_id in ("", None):
        await bot.blaze.echo(msgview.message_id)
        return

    if msgview.data_decoded in ("", None):
        await bot.blaze.echo(msgview.message_id)
        return

    if type(msgview.data_decoded) != str:
        await bot.blaze.echo(msgview.message_id)
        return

    print(msgview.message_id, msgview.data_decoded[:20])
    if bot.db.add_message(msgview):
        await bot.blaze.echo(msgview.message_id)
    return


bot = BlazeBot(DB_NAME, MIXIN_KEYSTORE)  # config.py
bot.blaze = BlazeClient(
    bot.config,
    on_message=message_handle,
    on_message_error_callback=message_handle_error_callback,
)
bot.blaze.run_forever(2)
