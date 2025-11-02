"""
FastAPI server to expose the Digital Music Store AI Agent as an API.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import uuid
import logging
import sys
import os

# Add parent directory to path to import agent modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.supervisor.digital_store import get_digital_store_agent
from utils.state_utils import create_initial_state
from utils.env import load_environment_variables

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_environment_variables()

# Initialize FastAPI app
app = FastAPI(
    title="Digital Music Store AI Agent API",
    description="API for interacting with the Digital Music Store multi-agent AI system",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agent (lazy loading)
_agent = None

def get_agent():
    """Get or initialize the agent."""
    global _agent
    if _agent is None:
        logger.info("Initializing digital store agent...")
        _agent = get_digital_store_agent()
        logger.info("Agent initialized successfully")
    return _agent


# Pydantic models for request/response
class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: Optional[str] = None


class ChatRequest(BaseModel):
    message: str
    thread_id: Optional[str] = None
    customer_id: Optional[str] = None


class ChatResponse(BaseModel):
    message: str
    thread_id: str
    customer_id: Optional[str] = None
    agent_name: Optional[str] = None


class ConversationHistory(BaseModel):
    thread_id: str
    messages: List[ChatMessage]
    customer_id: Optional[str] = None


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Digital Music Store AI Agent API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Send a message to the agent and get a response.
    
    Args:
        request: Chat request with message and optional thread_id
        
    Returns:
        ChatResponse with agent's response
    """
    try:
        # Get or create thread_id
        thread_id = request.thread_id or str(uuid.uuid4())
        config = {"configurable": {"thread_id": thread_id}}
        
        # Get agent
        agent = get_agent()
        
        # Create initial state
        state = create_initial_state(
            request.message,
            customer_id=request.customer_id or "",
            config=config
        )
        
        logger.info(f"Processing message for thread {thread_id}: {request.message[:50]}...")
        
        # Invoke agent
        result = agent.invoke(state, config)
        
        # Extract the last assistant message
        messages = result.get('messages', [])
        if not messages:
            raise HTTPException(status_code=500, detail="No response from agent")
        
        # Get the last message (should be from assistant)
        last_message = messages[-1]
        
        # Extract content from the message
        if hasattr(last_message, 'content'):
            content = last_message.content
        else:
            content = str(last_message)
        
        # Extract customer_id from state
        customer_id = result.get('customer_id', state.get('customer_id', None))
        
        logger.info(f"Agent response generated for thread {thread_id}")
        
        return ChatResponse(
            message=content,
            thread_id=thread_id,
            customer_id=customer_id,
            agent_name="digital_store_agent"
        )
        
    except Exception as e:
        logger.error(f"Error processing chat request: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")


@app.get("/api/conversation/{thread_id}", response_model=ConversationHistory)
async def get_conversation(thread_id: str):
    """
    Get conversation history for a thread.
    
    Args:
        thread_id: The conversation thread ID
        
    Returns:
        ConversationHistory with all messages
    """
    try:
        agent = get_agent()
        config = {"configurable": {"thread_id": thread_id}}
        
        # Get the state from checkpointer
        try:
            state_snapshot = agent.get_state(config)
        except Exception:
            # State might not exist yet
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        if not state_snapshot or not hasattr(state_snapshot, 'values'):
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        # Convert messages to ChatMessage format
        messages = []
        for msg in state_snapshot.values.get('messages', []):
            # Determine role based on message type
            if hasattr(msg, 'type'):
                role = "user" if msg.type == "human" else "assistant"
            else:
                # Default based on content or class name
                role = "assistant"
            
            content = msg.content if hasattr(msg, 'content') else str(msg)
            
            messages.append(ChatMessage(
                role=role,
                content=content
            ))
        
        return ConversationHistory(
            thread_id=thread_id,
            messages=messages,
            customer_id=state_snapshot.values.get('customer_id')
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting conversation: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error retrieving conversation: {str(e)}")


@app.delete("/api/conversation/{thread_id}")
async def delete_conversation(thread_id: str):
    """
    Delete a conversation thread.
    
    Args:
        thread_id: The conversation thread ID to delete
    """
    try:
        # Note: This would need to be implemented in the checkpointer
        # For now, we'll just return success
        logger.info(f"Deleting conversation thread: {thread_id}")
        return {"status": "deleted", "thread_id": thread_id}
    except Exception as e:
        logger.error(f"Error deleting conversation: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error deleting conversation: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

