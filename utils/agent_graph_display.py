import nest_asyncio
from IPython.display import Image
from langchain_core.runnables.graph import MermaidDrawMethod

def show_graph(graph, xray=False):
    """
    Displays the graph using the show_graph function.
    
    Args:
        graph: The graph to be displayed.
        xray: If True, displays additional information about the graph.
    """
    try:
        # Try the default mermaid renderer first (uses mermaid.ink service)
        return Image(graph.get_graph(xray=xray).draw_mermaid_png())
    except Exception as e:
        print(f"Default renderer failed: ({e}), falling back to pyppeteer renderer")
        nest_asyncio.apply()
        return Image(graph.get_graph().draw_mermaid_png(draw_method=MermaidDrawMethod.PYPPETEER))
