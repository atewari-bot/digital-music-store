# Digital Music Store AI Agent

A multi-agent AI system for a digital music store built with LangGraph and LangSmith. This system uses a supervisor pattern to orchestrate multiple specialized sub-agents that handle different aspects of customer service.

## Architecture

The system consists of:

1. **Supervisor Agent** (`digital_store_agent`): Orchestrates the workflow and routes queries to appropriate sub-agents
2. **Music Catalog Agent** (`music_catalog_subagent`): Handles music-related queries, searches the catalog, and manages user preferences
3. **Invoice Information Agent** (`invoice_info_agent`): Retrieves and provides information about customer invoices and purchases

### Features

- **Multi-Agent Architecture**: Supervisor pattern with specialized sub-agents
- **Memory Management**: Saves and loads user preferences for personalized recommendations
- **Customer ID Extraction**: Automatically extracts customer ID from messages (supports ID, email, or phone)
- **Tool Integration**: Agents use tools to query the Chinook music database
- **State Management**: Maintains conversation state and context across agent calls

## Setup

### Prerequisites

- Python 3.8+
- Node.js 18+ and npm (for frontend)
- API keys for your LLM provider (OpenAI, Together AI, etc.)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd digital-music-store
```

2. **Backend Setup:**
```bash
# Option 1: Use the setup script (recommended)
./setup.sh

# Option 2: Manual setup
# Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

**Important**: Always activate the virtual environment before running the backend:
```bash
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Frontend Setup:**
```bash
cd frontend
npm install
```

4. **Set up environment variables:**
Create a `.env` file in the root directory:
```bash
OPENAI_API_KEY=your_openai_api_key
# or
TOGETHER_API_KEY=your_together_api_key

# Optional: LangSmith for monitoring
LANGSMITH_API_KEY=your_langsmith_api_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
```

Create a `.env` file in the `frontend` directory (optional):
```bash
VITE_API_URL=http://localhost:8000
```

## Usage

### Web Interface (Recommended)

The easiest way to interact with the agent is through the web interface:

1. **Start the backend API server:**
```bash
# Make sure your virtual environment is activated first!
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Then start the server
python3 api/server.py

# Or use the convenience script:
./start_backend.sh
```

2. **Start the frontend development server:**
```bash
# In another terminal
cd frontend
npm install  # First time only
npm run dev
```

3. **Open your browser:**
   - Navigate to `http://localhost:3000`
   - Start chatting with the AI agent!

### Running Examples

Run the example queries to see the agent in action:

```bash
python main.py
```

This will run four example queries demonstrating different capabilities:
1. Music catalog query
2. Invoice information query
3. Combined query (both catalog and invoice)
4. Music preference query (saves preferences for future use)

### Interactive Mode

Run the agent in interactive mode for real-time conversations:

```bash
python main.py --interactive
```

Type your queries and the agent will respond. Type 'exit' or 'quit' to exit.

### Running Tests

Run all tests:

```bash
make test
```

Or run individual tests:

```bash
python tests/tests.py
```

### Generating Agent Graphs

Generate visualizations of the agent workflows:

```bash
python utils/agent_graph_generator.py
```

This creates PNG files in the `images/` directory showing the workflow graphs.

## Project Structure

```
digital-music-store/
├── agents/
│   ├── customer_service/     # Customer ID extraction utilities
│   ├── invoice_info/         # Invoice information agent and tools
│   ├── music_catalog/        # Music catalog agent, nodes, edges, and tools
│   ├── supervisor/           # Supervisor agent that orchestrates sub-agents
│   └── user/                 # User input handling
├── api/                      # Backend API
│   └── server.py             # FastAPI server exposing agent as REST API
├── da/                       # Data access layer
│   ├── db.py                 # Database connection (Chinook)
│   ├── memory.py             # Memory management (checkpointer and store)
│   ├── memory_utils.py       # User preference save/load utilities
│   └── state.py              # State schema definition
├── frontend/                 # React + TypeScript frontend
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── api/              # API client
│   │   └── types.ts          # TypeScript type definitions
│   ├── package.json          # Frontend dependencies
│   └── vite.config.ts        # Vite configuration
├── tests/                    # Test files
├── utils/                    # Utility functions
│   ├── agent_graph_display.py    # Graph visualization
│   ├── agent_graph_generator.py  # Generate all graphs
│   ├── env.py                # Environment variable loading
│   ├── llm.py                # LLM configuration
│   └── state_utils.py        # State initialization utilities
├── main.py                   # Main entry point (CLI)
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## How It Works

### Workflow

1. **User Query**: User sends a message to the system
2. **State Initialization**: System extracts customer ID and loads user preferences
3. **Supervisor Routing**: Supervisor agent analyzes the query and decides which sub-agent to call
4. **Sub-Agent Processing**: Selected sub-agent processes the query using its specialized tools
5. **Response**: Agent returns response, and preferences may be saved for future use

### Example Queries

**Music Catalog Query:**
```
"My customer ID is 1. What albums do you have by U2?"
```

**Invoice Query:**
```
"My customer ID is 1. How much was my most recent purchase?"
```

**Combined Query:**
```
"My customer ID is 1. How much was my most recent purchase? 
Also, what albums do you have by The Rolling Stones?"
```

**Preference Saving:**
```
"My customer ID is 1. I like the Rolling Stones. 
What songs do you recommend by them or by other artists that I might like?"
```
(This query will save your preferences for future conversations)

## Configuration

### LLM Model

The default model is configured in `utils/llm.py`. By default, it uses:
- `meta-llama/Llama-3.3-70B-Instruct` (via Together AI)

To use a different model, modify `utils/llm.py` or set the model name in your code.

### Memory Storage

The system uses:
- **MemorySaver**: For short-term memory (conversation checkpoints)
- **InMemoryStore**: For long-term memory (user preferences)

Both use in-memory storage by default. For production, consider persistent storage solutions.

## Development

### Adding New Agents

1. Create agent directory under `agents/`
2. Implement agent, nodes, edges, and tools
3. Add agent to supervisor in `agents/supervisor/digital_store.py`

### Adding New Tools

1. Create tool functions using `@tool` decorator
2. Add tools to agent's tool list
3. Tools will be automatically available to the agent

## Troubleshooting

### Import Errors

If you encounter import errors, ensure:
- Virtual environment is activated
- All dependencies are installed: `pip install -r requirements.txt`
- Python path includes the project root

### Database Connection Issues

The Chinook database is loaded in-memory from a remote URL. If loading fails:
- Check internet connection
- Verify the Chinook database URL is accessible

### LLM API Errors

If you see LLM API errors:
- Verify your API key is set in `.env`
- Check API rate limits and quotas
- Ensure the model name is correct for your provider

## References

This project is based on the article:
[Building a Multi-Agent AI System with LangGraph and LangSmith](https://levelup.gitconnected.com/building-a-multi-agent-ai-system-with-langgraph-and-langsmith-6cb70487cd81)

## License

See LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
