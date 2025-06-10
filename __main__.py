
import logging
from tests.music_catalog_test import test_music_catalog_agent
from utils.env import load_environment_variables


if __name__ == '__main__':
    """
    Main function to run the test.
    
    This function is the entry point for running the music catalog agent test.
    """
    logging.basicConfig(level=logging.DEBUG)
    logging.info("Starting music catalog agent test...")
    try:
        load_environment_variables()
        test_music_catalog_agent()
    except Exception as e:
        logging.error("An error occurred: %s", e)
        logging.debug("Traceback: ", exc_info=True)