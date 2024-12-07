import logging

from .brain.agent import Agent
from .brain.lm import get_openai_model

__AUTHOR__ = '吴子豪 / Vortez Wohl'
__EMAIL__ = 'vortez.wohl@gmail.com'
__VERSION__ = '0.6.5-preview'

logger = logging.getLogger('ceo')
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(levelname)s] %(asctime)s %(name)s : %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
logger = logging.getLogger('ceo.prompt')
logger.setLevel(logging.INFO)
