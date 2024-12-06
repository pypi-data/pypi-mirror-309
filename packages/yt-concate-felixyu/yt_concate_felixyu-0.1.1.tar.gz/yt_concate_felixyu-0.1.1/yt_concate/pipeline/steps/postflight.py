from .step import Step
import logging

class Postflight(Step):
    def process(self, data, inputs, utils):
        logger = logging.getLogger()
        logger.info('In Postflight...')
        cleanUp = inputs['cleanUp']
        if cleanUp == 'True':
            utils.remove_downloaded_files()