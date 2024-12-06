from nonebot.utils import logger_wrapper

log = logger_wrapper("Mail")

# logging.basicConfig(level=logging.NOTSET)
# aioimaplib_logger = logging.getLogger("aioimaplib.aioimaplib")
# for handler in aioimaplib_logger.handlers:
#     aioimaplib_logger.removeHandler(handler)
# loguru_handler = LoguruHandler()
# aioimaplib_logger.addHandler(loguru_handler)

# import logging
# logging.basicConfig(level=logging.DEBUG)
# aioimaplib_logger = logging.getLogger("aioimaplib.aioimaplib")
# sh = logging.StreamHandler()
# sh.setLevel(logging.DEBUG)
# sh.setFormatter(
#     logging.Formatter("%(asctime)s %(levelname)s [%(module)s:%(lineno)d] %(message)s")
# )
# aioimaplib_logger.addHandler(sh)
# aioimaplib_logger.debug("This is a debug message")
