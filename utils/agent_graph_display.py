import os
import nest_asyncio
import logging
from langchain_core.runnables.graph import MermaidDrawMethod

def show_graph(graph, xray=False):
    """
    Displays the graph using the show_graph function.
    
    Args:
        graph: The graph to be displayed.
        xray: If True, displays additional information about the graph.
    """
    try:
        os.makedirs("images", exist_ok=True)
        # Try the default mermaid renderer first (uses mermaid.ink service)
        image = graph.get_graph(xray=xray).draw_mermaid_png()
        
        image_path = f"images/{graph.name}.png"

        with open(image_path, "wb") as f:
            f.write(image)
        logging.info(f"Graph image saved as {image_path}")
    except Exception as e:
        logging.debug(f"Default renderer failed: ({e}), falling back to pyppeteer renderer")
        nest_asyncio.apply()
        image = graph.get_graph().draw_mermaid_png(draw_method=MermaidDrawMethod.PYPPETEER)
        image_path = f"images/{graph.name}.png"

        with open(image_path, "wb") as f:
            f.write(image)
        logging.info(f"Graph image saved as {image_path} using pyppeteer renderer")
    except Exception as e:
        logging.error(f"Failed to display graph: {e}")
        raise e
