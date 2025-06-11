import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import logging
from invoice_info_test import test_invoice_info_agent
from music_catalog_test import test_music_catalog_agent
from utils.env import load_environment_variables


if __name__ == '__main__':
    """
    Main function to run the test.
    
    This function is the entry point for running the music catalog agent test.
    """
    logging.basicConfig(level=logging.DEBUG)
    logging.info("Starting invoice info agent test...")
    try:
        load_environment_variables()
        test_music_catalog_agent()
        test_invoice_info_agent()
    except Exception as e:
        logging.error("An error occurred: %s", e)
        logging.debug("Traceback: ", exc_info=True)