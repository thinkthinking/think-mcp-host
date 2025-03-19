import os
import random
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional

from think_llm_client.utils.display import print_markdown
from think_llm_client.utils.terminal_config import TABLE_STYLE, console


class PoetryType(Enum):
    AI = "ai"
    ZEN = "zen"
    LOVE = "love"


class Language(Enum):
    CHINESE = "cn"
    ENGLISH = "en"


class PoetryDisplay:
    def __init__(self, language: Language = Language.ENGLISH):
        self.base_path = Path(__file__).parent.parent / "resources" / "poetry"
        self.language = language
        self._update_poetry_files()

        self.colors = {
            PoetryType.AI: TABLE_STYLE["blue"],
            PoetryType.ZEN: TABLE_STYLE["green"],
            PoetryType.LOVE: TABLE_STYLE["red"],
        }

    def _update_poetry_files(self):
        """Update poetry file paths based on selected language"""
        suffix = f"_{self.language.value}" if self.language == Language.ENGLISH else ""

        self.poetry_files = {
            PoetryType.AI: self.base_path / f"ai{suffix}.txt",
            PoetryType.ZEN: self.base_path / f"zen{suffix}.txt",
            PoetryType.LOVE: self.base_path / f"love{suffix}.txt",
        }

    def set_language(self, language: Language):
        """Set the language for poetry display"""
        self.language = language
        self._update_poetry_files()

    def _load_poetry(self, poetry_type: PoetryType) -> List[str]:
        """Load the specified type of poetry file"""
        try:
            with open(self.poetry_files[poetry_type], "r", encoding="utf-8") as f:
                lines = f.readlines()
                # Filter empty lines and comment lines, and remove sequence numbers
                processed_lines = []
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        # Remove sequence number (if exists)
                        if ". " in line:
                            line = line.split(". ", 1)[1]
                        processed_lines.append(line)
                return processed_lines
        except Exception as e:
            console.print(
                f"[yellow]Warning: Unable to load {poetry_type.value} type poetry file: {str(e)}[/yellow]"
            )
            # If English file doesn't exist, try to fall back to Chinese
            if self.language == Language.ENGLISH:
                try:
                    fallback_file = self.base_path / f"{poetry_type.value}.txt"
                    with open(fallback_file, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                        processed_lines = []
                        for line in lines:
                            line = line.strip()
                            if line and not line.startswith("#"):
                                if ". " in line:
                                    line = line.split(". ", 1)[1]
                                processed_lines.append(line)
                        console.print(f"[yellow]Falling back to Chinese poetry file[/yellow]")
                        return processed_lines
                except Exception:
                    pass
            return []

    def display_random_poetry(self, poetry_type: Optional[PoetryType] = None) -> None:
        """
        Display random poetry
        Args:
            poetry_type: Optional poetry type, if not specified, a random type will be chosen
        """
        if poetry_type is None:
            poetry_type = random.choice(list(PoetryType))

        poems = self._load_poetry(poetry_type)
        if not poems:
            return

        random_poem = random.choice(poems)
        color = self.colors[poetry_type]

        print_markdown(
            content=random_poem,
            title=poetry_type.value.upper(),
            style=color,
            border_style=color,
            show_time=False,
        )


# Create singleton instance
poetry_display = PoetryDisplay()


def display_random_poetry(
    poetry_type: Optional[PoetryType] = None, language: Optional[Language] = None
) -> None:
    """Convenience function to display random poetry

    Args:
        poetry_type: Optional poetry type, if not specified, a random type will be chosen
        language: Optional language selection, if not specified, current language setting will be used
    """
    if language is not None:
        poetry_display.set_language(language)
    poetry_display.display_random_poetry(poetry_type)
