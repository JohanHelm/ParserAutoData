import asyncio
from pathlib import Path

from utils.logging_settings import configure_logger, init_logger
from bot.start_bot import start_bot
from settings import WORKDIR



if __name__ == "__main__":
    log_dirpath: Path = WORKDIR.joinpath("logs")
    logger = init_logger()
    configure_logger(logger, file_path=log_dirpath.joinpath("logfile.log"), rotation=10)
    asyncio.run(start_bot())
