
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import logging
from utils.env import load_environment_variables
from agents.invoice_info.invoice_info_agent import show_invoice_info_subagent_graph
from agents.music_catalog.music_catalog_agent import show_music_catalog_subagent_graph
from agents.supervisor.digital_store import show_digital_store_graph


if __name__ == '__main__':
    """
    Main function to generate agent graphs.
    """
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting agent graph generation...")
    
    # Load environment variables
    load_environment_variables()
    
    try:
        logging.info("Generating invoice info agent graph...")
        show_invoice_info_subagent_graph()
        
        logging.info("Generating music catalog agent graph...")
        show_music_catalog_subagent_graph()
        
        logging.info("Generating digital store (supervisor) agent graph...")
        show_digital_store_graph()
        
        logging.info("All agent graphs generated successfully!")
    except Exception as e:
        logging.error("An error occurred: %s", e)
        logging.debug("Traceback: ", exc_info=True)
        raise