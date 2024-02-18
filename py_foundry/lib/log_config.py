import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        # logging.FileHandler('deployments.log'),
        logging.StreamHandler()
    ]
)

cf_logger = logging.getLogger(__name__)
