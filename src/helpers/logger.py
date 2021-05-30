import logging
from logging.handlers import TimedRotatingFileHandler

class MyFilter(object):
    def _init_(self, level):
        self.__level = level

    def filter(self, logRecord):
        return logRecord.levelno <= self.__level

# region  [Criando o logger]
formatter = logging.Formatter("%(asctime)s - %(levelname)s::%(message)s")
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# endregion

# region [default handler]
handler = TimedRotatingFileHandler('Logs/General/general.log', when="H", interval=2, encoding='utf8', backupCount=72)
handler.suffix = "%Y-%m-%d_%H.log"
handler.setFormatter(formatter)
logger.addHandler(handler)
# endregion

# region [Info only]
handler_info = TimedRotatingFileHandler('Logs/Infos/info.log', when="midnight", encoding='utf8')
handler_info.suffix = "%Y-%m-%d.log"
handler_info.setFormatter(formatter)
handler_info.setLevel(logging.INFO)
# handler_info.addFilter(MyFilter(logging.INFO))
logger.addHandler(handler_info)
# endregion

# region [Warning only]
handler_warning = TimedRotatingFileHandler('Logs/Warnings/warnings.log', when="W0", encoding='utf8')
handler_warning.suffix = "%Y-%m-%d.log"
handler_warning.setFormatter(formatter)
handler_warning.setLevel(logging.WARNING)
# handler_warning.addFilter(MyFilter(logging.WARNING))
logger.addHandler(handler_warning)
# endregion

# region [Errors only]
handler_error = TimedRotatingFileHandler('Logs/Errors/error.log', when="midnight", encoding='utf8')
handler_error.suffix = "%Y-%m-%d.log"
handler_error.setFormatter(formatter)
handler_error.setLevel(logging.ERROR)
# handler_error.addFilter(MyFilter(logging.ERROR))
logger.addHandler(handler_error)
# endregion

# region [Critical only]
handler_critical = TimedRotatingFileHandler('Logs/Critical/critical.log', when="midnight", interval=1, encoding='utf8')
handler_critical.suffix = "%Y-%m-%d.log"
handler_critical.setFormatter(formatter)
handler_critical.setLevel(logging.CRITICAL)
# handler_critical.addFilter(MyFilter(logging.CRITICAL))
logger.addHandler(handler_critical)
# endregion

logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
logging.getLogger("sqlalchemy.pool").setLevel(logging.INFO)