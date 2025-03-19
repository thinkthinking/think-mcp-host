from think_llm_client.utils.logger import setup_logger

from .destiny_host import main

# Initialize project-specific logging configuration
setup_logger("think-mcp-host")

__all__ = ["main"]
