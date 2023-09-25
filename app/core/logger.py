import logging

logging.basicConfig(
    level=logging.INFO, filename='log.log', filemode='a',
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)
