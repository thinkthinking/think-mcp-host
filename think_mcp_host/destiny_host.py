import argparse
import asyncio
import os
import platform
import re
import sys
import time
from datetime import datetime
from enum import Enum
from importlib.metadata import version
from pathlib import Path

from dotenv import load_dotenv
from prompt_toolkit.application import get_app
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from rich.align import Align
from rich.panel import Panel
from rich.prompt import Prompt
from think_llm_client.cli import LLMCLIClient
from think_llm_client.utils.display import print_markdown
from think_llm_client.utils.logger import get_log_file_path, logging, setup_logger
from think_llm_client.utils.terminal_config import TABLE_STYLE, console
from think_mcp_client import ClientType, MCPClientManager
from think_mcp_client.mcp_processor import MCPProcessor

from think_mcp_host.utils.poetry_display import Language, PoetryType, display_random_poetry

# Get project-specific logger
logger = logging.getLogger("think-mcp-host")


class DestinyHost:
    def __init__(self, llm_config_path=None, mcp_config_path=None):
        # Specify configuration file paths
        self.llm_config_path = llm_config_path
        self.mcp_config_path = mcp_config_path
        self.llm_client = None
        self.mcp_manager = None
        self.mcp_processor = None
        self.session = self._create_prompt_session()
        self.current_history_file = None  # Add current history file path
        self.language = Language.ENGLISH  # Default to English

    def _create_prompt_session(self):
        """Create prompt session"""
        from prompt_toolkit import PromptSession
        from prompt_toolkit.history import FileHistory
        from prompt_toolkit.styles import Style

        history_dir = Path.home() / ".think-mcp-host" / "command_history"
        history_dir.mkdir(parents=True, exist_ok=True)

        history = FileHistory(str(history_dir / "history.txt"))
        style = Style.from_dict(
            {
                "prompt": "bold #00ff00",
                "rprompt": "italic #888888",
            }
        )

        return PromptSession(history=history, style=style, include_default_pygments_style=False)

    def clear_screen(self):
        """Clear screen, using a cross-platform method"""
        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")

    def init_mcp(self):
        """Synchronously initialize MCP-related components"""
        try:
            # Convert string path to Path object
            config_path = Path(self.mcp_config_path) if self.mcp_config_path else None
            self.mcp_manager = MCPClientManager(config_path=config_path, client_type=ClientType.CLI)
            self.mcp_processor = MCPProcessor(self.mcp_manager)
            logger.info("MCP initialized successfully")
            return True
        except Exception as e:
            logger.error(f"MCP initialization failed: {e}")
            return False

    async def init_clients(self):
        """Initialize all clients"""
        # Initialize LLM client
        try:
            self.llm_client = LLMCLIClient(config_path=self.llm_config_path)
            logger.info("LLM client initialized successfully")
        except Exception as e:
            logger.error(f"LLM client initialization failed: {e}")
            return False

        # Synchronously initialize MCP
        if not self.init_mcp():
            return False
        return True

    def print_header(self):
        """Print program header information"""
        from pyfiglet import figlet_format
        from rich.align import Align
        from rich.panel import Panel

        version = get_version()

        # Generate figlet for each part
        header_ai = figlet_format("AI", font="slant")
        header_zen = figlet_format("ZEN", font="slant")  # Use uppercase for more uniform length
        header_love = figlet_format("LOVE", font="slant")  # Use uppercase for more uniform length

        # Split each part by line
        ai_lines = header_ai.split("\n")
        zen_lines = header_zen.split("\n")
        love_lines = header_love.split("\n")

        # Ensure all parts have the same number of lines (fill with empty lines)
        max_lines = max(len(ai_lines), len(zen_lines), len(love_lines))
        ai_lines = ai_lines + [""] * (max_lines - len(ai_lines))
        zen_lines = zen_lines + [""] * (max_lines - len(zen_lines))
        love_lines = love_lines + [""] * (max_lines - len(love_lines))

        # Add some spaces between lines as spacing
        spacing = " " * 4  # 4 spaces of spacing

        # Merge all lines, add colors
        colored_lines = []
        for i in range(max_lines):
            colored_line = (
                f"[bright_blue]{ai_lines[i]}[/bright_blue]"
                f"{spacing}"
                f"[bright_green]{zen_lines[i]}[/bright_green]"
                f"{spacing}"
                f"[bright_red]{love_lines[i]}[/bright_red]"
            )
            colored_lines.append(colored_line)

        colored_header = "\n".join(colored_lines)
        console.print(Align.center(colored_header, vertical="middle"))

        # Welcome message
        # Default welcome message
        welcome_text = (
            "Welcome to the 'AI·Zen·Love' terminal. It can help you work with AI in a zen-like and loving mindset, "
            "and supports the latest DeepSeek-R1 model and MCP protocol, hoping to bring you inspiration, joy, and peace."
        )
        custom_append_text = " "
        if custom_append_text:
            welcome_text = f"{welcome_text} {custom_append_text}"

        welcome_panel = Panel(
            Align.center(welcome_text),
            style="bright_magenta",
            border_style="bright_magenta",
            title="🌌 AI·Zen·Love | To You Who Shine Like Stars 🌌",
            padding=(2, 4),  # 2 lines top and bottom, 4 characters left and right padding
        )
        console.print(Align.center(welcome_panel))

        # Version number and usage tips
        version_text = f"[{TABLE_STYLE['info']}]Version: {version}[/]"

        # Display random poetry in the selected language
        display_random_poetry(language=self.language)
        console.print(Align.center(version_text))

    async def process_mcp_input(
        self, initial_input: str = "", *, allow_empty: bool = False
    ) -> tuple[str, bool]:
        """Process input containing MCP commands

        Args:
            initial_input: Initial input text, default is empty
            allow_empty: Whether to allow empty input, default is False

        Returns:
            tuple[str, bool]: (Processed input, whether successful)
        """
        user_input = initial_input

        while True:
            if not initial_input:
                try:
                    user_input = await self.session.prompt_async(
                        [("class:prompt", "\nYou: ")],
                        rprompt=[("class:rprompt", " Ctrl+C to exit")],
                    )
                except (EOFError, KeyboardInterrupt):
                    return "", False

            if not user_input.strip() and not allow_empty:
                if not initial_input:
                    continue
                return "", False

            if user_input.lower() in ["exit", "quit"]:
                return "", False

            # Process all ->mcp until there are no more ->mcp
            while True:
                # Check if it contains standalone ->mcp (with spaces before and after)
                mcp_match = re.search(r"(?<=\s)->mcp(?=\s)", user_input)
                if not mcp_match:
                    break

                if not self.mcp_processor:
                    console.print(
                        "\n❌ MCP has not been initialized, cannot process MCP commands",
                        style=TABLE_STYLE["yellow"],
                    )
                    return "", False

                # Get text before and after ->mcp
                start_pos = mcp_match.start()
                end_pos = mcp_match.end()
                prefix = user_input[:start_pos]
                suffix = user_input[end_pos:]

                # Get MCP placeholder
                result = await self.mcp_processor.process_mcp_command()
                if result:
                    # Let the user continue editing the message
                    console.print(
                        "\nPlease continue editing your message, press Enter to send when finished",
                        style=TABLE_STYLE["green"],
                    )
                    try:
                        user_input = await self.session.prompt_async(
                            default=f"{prefix}{result}{suffix}"
                        )
                    except (EOFError, KeyboardInterrupt):
                        return "", False
                else:
                    break

            # Finally process all placeholders
            if self.mcp_processor:
                processed_input = await self.mcp_processor.process_text(user_input)
            else:
                processed_input = user_input

            return processed_input, True

    async def ask_save_with_timeout(self, timeout=5):
        """Ask whether to save the conversation, with timeout functionality"""

        async def get_user_input():
            try:
                return await self.session.prompt_async(
                    f"\nSave conversation? [Y/n] (Automatically selects Y after {timeout}s): "
                )
            except (EOFError, KeyboardInterrupt):
                return "y"  # If the user presses Ctrl+C again, default to save

        try:
            # Create user input task
            user_input_task = asyncio.create_task(get_user_input())
            # Wait for user input or timeout
            done, pending = await asyncio.wait([user_input_task], timeout=timeout)

            # Cancel unfinished tasks
            for task in pending:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass

            # Get user input or use default value
            answer = user_input_task.result() if user_input_task in done else "y"
            return answer.lower() != "n"
        except Exception:
            return True  # For any error, default to save

    async def save_chat_history(self):
        """Save and export conversation history"""
        if self.llm_client:
            try:
                if self.current_history_file:
                    success, new_file = self.llm_client.save_chat_history(self.current_history_file)
                    if success and new_file:
                        self.llm_client.export_chat_history(new_file)
                        logger.info(f"Successfully saved conversation history to: {new_file}")
                else:
                    logger.info("First time saving conversation history")
                    success, new_file = self.llm_client.save_chat_history()
                    if success and new_file:
                        logger.info("Successfully exported conversation history")
                        self.llm_client.export_chat_history(new_file)
            except Exception as e:
                logger.error(f"Error occurred while saving conversation history: {e}")
                console.print("\n❌ Failed to save conversation history", style=TABLE_STYLE["error"])

    async def setup_llm(self):
        """Set up LLM model"""
        models = self.llm_client.display_available_models()
        if not models:
            console.print("No available models", style=TABLE_STYLE["error"])
            return False

        choice = await self.session.prompt_async(
            "\nPlease select model number: ",
            default="1",
            rprompt=[("class:rprompt", " Enter a number to select model")],
        )

        try:
            index = int(choice) - 1
            if 0 <= index < len(models):
                model_type, provider, model = models[index]
                self.llm_client.set_model(model_type, provider, model)
                console.print(f"\n✨ Selected: ", style=TABLE_STYLE["green"], end="")
                console.print(f"[blue]{model_type.upper()}[/blue] - ", end="")
                console.print(f"[green]{provider}[/green] - ", end="")
                console.print(f"[yellow]{model}[/yellow]")
                return True
        except ValueError:
            pass

        console.print("\n❌ Invalid selection", style=TABLE_STYLE["error"])
        return False

    async def setup_system_prompt(self):
        """Set up system prompt"""
        console.print(
            "\nPlease enter system prompt (you can insert MCP resources by typing ->mcp anywhere):",
            style=TABLE_STYLE["cyan"],
        )
        content, success = await self.process_mcp_input(allow_empty=True)
        if not success:
            return False

        if content:
            self.llm_client.system_prompt = content
            console.print("\n✨ Set the above content as system prompt", style=TABLE_STYLE["green"])
            logger.info(f"Set the above content as system prompt: {content}")
        return True

    async def setup_mode(self):
        """Set up running mode"""
        while True:
            console.print("\nPlease select running mode:", style=TABLE_STYLE["cyan"])
            console.print("1. [bold green]Chat mode[/bold green]")
            console.print("2. [bold yellow]Tool mode[/bold yellow]")
            choice = await self.session.prompt_async("Please select [1/2] (1): ", default="1")

            if choice == "2":
                tool_result = await self.setup_tool_mode()
                if tool_result:
                    return tool_result
                continue
            return "chat" if await self.setup_chat_mode() else None

    async def setup_tool_mode(self):
        """Set up tool mode"""
        try:
            if not self.mcp_manager:
                console.print(
                    "\n❌ MCP has not been initialized, please try again later",
                    style=TABLE_STYLE["yellow"],
                )
                return False

            while True:
                # Use select_mcp_client to select client
                client = await self.mcp_manager.select_mcp_client(self.session)
                if not client:
                    return False

                try:
                    # Set prompt_session
                    client.prompt_session = self.session

                    # Get client's tool list
                    tools = await client.list_tools()
                    if not tools:
                        console.print(
                            "\n❌ This client has no available tools", style=TABLE_STYLE["yellow"]
                        )
                        continue

                    # Use client's tool selection and execution functionality
                    result = await client.select_and_run_tool(tools)

                    # Ask whether to continue using tools
                    continue_choice = await self.session.prompt_async(
                        "\nContinue using tools? [y/N]: ", default="n"
                    )
                    if continue_choice.lower() != "y":
                        return False

                except Exception as e:
                    console.print(
                        f"\n❌ Error occurred while executing tool: {e}", style=TABLE_STYLE["error"]
                    )
                    logger.error(f"Error running tool: {e}")
                    continue

        except Exception as e:
            console.print(f"\n❌ Failed to get client list: {e}", style=TABLE_STYLE["error"])
            logger.error(f"Error getting client list: {e}")
            return False

    async def setup_chat_mode(self):
        """Set up chat mode"""
        # First set up LLM
        if not await self.setup_llm():
            return False

        console.print("\nPlease select how to start:", style=TABLE_STYLE["cyan"])
        console.print(
            "1. Set system prompt, then start new conversation", style=TABLE_STYLE["yellow"]
        )
        console.print("2. Start new conversation directly", style=TABLE_STYLE["green"])
        console.print("3. Load conversation history", style=TABLE_STYLE["blue"])
        choice = await self.session.prompt_async("Please select [1/2/3] (1): ", default="2")

        if choice == "3":
            return await self.load_chat_history()
        elif choice == "1":
            return await self.setup_system_prompt()
        return True

    async def load_chat_history(self) -> bool:
        """Load conversation history"""
        histories = self.llm_client.display_available_histories()
        if not histories:
            return False

        choice = await self.session.prompt_async("\nPlease select conversation history to load: ")
        try:
            index = int(choice) - 1
            if 0 <= index < len(histories):
                filepath = histories[index][0]
                if self.llm_client.load_chat_history_from_file(filepath):
                    self.current_history_file = filepath  # Record current history file path
                    return True
        except (ValueError, IndexError):
            pass

        return False

    async def chat_loop(self):
        """Main conversation loop"""

        try:
            while True:
                try:
                    console.print(
                        "\n Tip: If you need to call MCP server resources, you can type ->mcp (must have spaces before and after) anywhere; Press Ctrl+C to save conversation and exit.",
                        style=TABLE_STYLE["info"],
                    )
                    processed_input, success = await self.process_mcp_input()
                    if not success:
                        break

                    # Call LLM
                    logger.info(f"Input Message：{processed_input}")
                    reasoning, response = await self.llm_client.chat_cli(message=processed_input)
                    logger.info(f"Reasoning Result：{reasoning}")
                    logger.info(f"Response Result：{response}")

                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    console.print(f"\nAn error occurred: {e}", style=TABLE_STYLE["error"])
                    import traceback

                    console.print(traceback.format_exc(), style=TABLE_STYLE["error"])
                    continue

        finally:
            try:
                # Ask whether to save conversation
                if await self.ask_save_with_timeout():
                    await self.save_chat_history()

                # Clean up resources
                await self.cleanup_resources()
                console.print("\n👋 Goodbye!", style=TABLE_STYLE["magenta"])
            except Exception as e:
                logger.error(f"Error occurred while cleaning up resources: {e}")
                console.print(
                    f"\n❌ Error occurred while cleaning up resources: {e}",
                    style=TABLE_STYLE["error"],
                )

    async def cleanup_resources(self):
        """Clean up all resources"""
        try:
            # Clean up MCP resources
            if self.mcp_manager:
                try:
                    await self.mcp_manager.cleanup_all_clients()
                except Exception as e:
                    logger.error(f"MCP cleanup failed: {e}")

        except Exception as e:
            logger.error(f"Error occurred during resource cleanup: {e}")

    async def run(self):
        """Run main program"""
        self.clear_screen()
        self.print_header()

        try:
            # Initialize all clients
            await self.init_clients()

            # Set up running mode
            mode = await self.setup_mode()
            if not mode:
                return

            # If in chat mode, start conversation loop
            if mode == "chat":
                await self.chat_loop()

        except Exception as e:
            console.print(f"\nAn error occurred: {e}", style=TABLE_STYLE["error"])

        finally:
            try:
                # Clean up resources
                await self.cleanup_resources()
            except Exception as e:
                console.print(
                    f"\nError occurred while cleaning up resources: {e}", style=TABLE_STYLE["error"]
                )
                raise

    async def _handle_command(self, command):
        """Handle special commands"""
        if command == "/exit" or command == "/quit":
            await self.save_chat_history()
            return True
        elif command == "/clear":
            if self.llm_client:
                self.llm_client.clear_chat_history()
            console.print("[green]Chat history cleared[/green]")
            return False
        elif command == "/save":
            await self.save_chat_history()
            return False
        elif command == "/help":
            self._print_help()
            return False
        elif command.startswith("/lang"):
            # Handle language switching
            parts = command.split()
            if len(parts) > 1:
                lang_code = parts[1].lower()
                if lang_code in ("en", "english"):
                    self.language = Language.ENGLISH
                    console.print("[green]Switched to English language[/green]")
                elif lang_code in ("cn", "chinese"):
                    self.language = Language.CHINESE
                    console.print("[green]Switched to Chinese language[/green]")
                else:
                    console.print(
                        "[yellow]Unknown language code. Available options: en, cn[/yellow]"
                    )
            else:
                console.print(f"[green]Current language: {self.language.value}[/green]")
            return False
        return None

    def _print_help(self):
        """Print help information"""
        help_text = """
        [bold]Available Commands:[/bold]
        
        [green]/exit[/green] or [green]/quit[/green] - Exit the program
        [green]/clear[/green] - Clear chat history
        [green]/save[/green] - Save chat history
        [green]/help[/green] - Show this help message
        [green]/lang [en|cn][/green] - Set language (English or Chinese)
        """
        console.print(help_text)


def get_version():
    """Get package version"""
    try:
        return version("think-mcp-host")
    except Exception:
        return "0.2.1"  # Default version


def get_resource_path(relative_path):
    """Get resource file path, supports PyInstaller packaging"""
    try:
        if getattr(sys, "frozen", False):
            # If it's a packaged exe, need to add think_mcp_host prefix
            base_path = sys._MEIPASS
            if not relative_path.startswith("think_mcp_host"):
                relative_path = os.path.join("think_mcp_host", relative_path)
        else:
            # If it's a development environment, use relative path
            base_path = os.path.dirname(os.path.abspath(__file__))
            if relative_path.startswith("think_mcp_host"):
                # If path starts with think_mcp_host, remove it
                relative_path = relative_path[len("think_mcp_host/") :]

        # Normalize path separators
        relative_path = os.path.normpath(relative_path)
        full_path = os.path.normpath(os.path.join(base_path, relative_path))

        return full_path
    except Exception as e:
        logger.error(f"Error in get_resource_path: {str(e)}")
        raise


def main():
    parser = argparse.ArgumentParser(description="Think MCP Host")
    parser.add_argument("--llm_config", type=str, help="Custom LLM configuration file path")
    parser.add_argument("--mcp_config", type=str, help="Custom MCP server configuration file path")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {get_version()}")
    args = parser.parse_args()
    key_insider = False
    try:
        # Decide configuration file path based on key_insider
        llm_config_path = (
            args.llm_config
            if args.llm_config or not key_insider
            else get_resource_path(os.path.join("config", "llm_config.json"))
        )
        logger.info(f"LLM configuration file path passed in or set in code: {llm_config_path}")
        host = DestinyHost(llm_config_path=llm_config_path, mcp_config_path=args.mcp_config)
        asyncio.run(host.run())
    except KeyboardInterrupt:
        console.print("\nThank you for using, goodbye!", style=TABLE_STYLE["magenta"])
        sys.exit(0)
    except Exception as e:
        error_msg = f"An error occurred: {str(e)}"
        logger.error(error_msg)
        console.print("\nLog file location:", get_log_file_path())
        input("Press Enter to exit...")  # Add this line to let the user see the error message
        sys.exit(1)


if __name__ == "__main__":
    main()
