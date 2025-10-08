import os
from pathlib import Path
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.google import Gemini
from agno.os import AgentOS
from agno.tools.mcp import MCPTools
from agno.tools.tavily import TavilyTools

# Load environment variables from .env file (if python-dotenv is installed)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # python-dotenv not installed, environment variables should be set manually
    pass

# Configure database path for production
# Use /code/data for Docker volume mounting, fallback to local for development
db_dir = os.getenv("DB_DIR", "/code/data")
db_path = Path(db_dir)
db_path.mkdir(parents=True, exist_ok=True)
db_file = str(db_path / "agno.db")

# Create the Agent
agno_agent = Agent(
    name="Agno Agent",
    model=Gemini(id="gemini-2.5-flash-lite"),
    # Add a database to the Agent
    db=SqliteDb(db_file=db_file),
    # Add the Agno MCP server to the Agent
    # TavilyTools will automatically use TAVILY_API_KEY environment variable
    tools=[
        MCPTools(transport="streamable-http", url="https://docs.agno.com/mcp"),
        TavilyTools()  # Uses default settings, reads TAVILY_API_KEY from environment
    ],
    # Add the previous session history to the context
    add_history_to_context=True,
    markdown=True,
    enable_session_summaries=True
)

# Create the AgentOS
agent_os = AgentOS(agents=[agno_agent])
# Get the FastAPI app for the AgentOS
app = agent_os.get_app()