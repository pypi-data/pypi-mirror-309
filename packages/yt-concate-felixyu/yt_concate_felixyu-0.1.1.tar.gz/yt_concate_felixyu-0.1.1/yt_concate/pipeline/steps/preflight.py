import logging
from .step import Step

class Preflight(Step):
    def process(self, data, inputs, utils):
        utils.init_logger(inputs['loggingLevel'])
        logger = logging.getLogger()
        logger.info('In Preflight...')
        utils.create_dir()