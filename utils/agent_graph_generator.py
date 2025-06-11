

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import logging
from agents.invoice_info.invoice_info_agent import show_invoice_info_subagent_graph
from agents.music_catalog.music_catalog_agent import show_music_catalog_subagent_graph
from agents.supervisor.digital_store import show_digital_store_graph
# from utils.env import load_environment_variables


if __name__ == '__main__':
    """
    Main function to generate agent graphs.
    """
    logging.basicConfig(level=logging.DEBUG)
    logging.info("Starting agent graph generation...")
    try:
        show_invoice_info_subagent_graph()
        show_music_catalog_subagent_graph()
        show_digital_store_graph()
    except Exception as e:
        logging.error("An error occurred: %s", e)
        logging.debug("Traceback: ", exc_info=True)