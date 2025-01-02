import sys
import argparse
import os
import asyncio
from typing import Optional, NoReturn
import google.generativeai as genai
from rich.console import Console
from rich.markdown import Markdown
from rich.theme import Theme
from utils.config import ConfigManager

os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "2"

class AskyAI:
    MODEL_NAME = 'gemini-2.0-flash-exp'

    def __init__(self) -> None:
        self.config_manager = ConfigManager()
        self.api_key = self._initialize_api()
        self.model = self._setup_model()
        self.console = Console(theme=Theme({
            "info": "cyan",
            "warning": "yellow",
            "error": "red"
        }))

    def _initialize_api(self) -> str:
        api_key = self.config_manager.get_api_key()
        if not api_key:
            self._exit_with_error("API key is not configured. Use --set-api-key to set it.")
        genai.configure(api_key=api_key, transport="grpc")
        return api_key

    def _setup_model(self) -> genai.GenerativeModel:
        try:
            return genai.GenerativeModel(self.MODEL_NAME)
        except Exception as e:
            self._exit_with_error(f"Model initialization error: {e}")

    def ask_question(self, question: str) -> str:
        try:
            response = self.model.generate_content(question)
            if not response.text:
                return "Received empty response from AI"
            return response.text
        except Exception as e:
            return f"Error receiving response: {str(e)}"

    def display_response(self, response: str) -> None:
        """Отображает ответ с поддержкой Markdown"""
        try:
            markdown = Markdown(response, code_theme="monokai")
            self.console.print(markdown)
        except Exception as e:
            self.console.print(f"Error formatting response: {e}", style="error")

    @staticmethod
    def _exit_with_error(message: str) -> NoReturn:
        console = Console(stderr=True)
        console.print(f"[error]{message}[/error]")
        sys.exit(1)


class ArgumentParser:
    def __init__(self) -> None:
        self.parser = self._create_parser()
        self.console = Console()

    def _create_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            description="[bold cyan]AskY: Your Console AI Assistant[/bold cyan]",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="Example usage:\n"
                   "  %(prog)s --set-api-key YOUR_API_KEY\n"
                   "  %(prog)s 'How does a quantum computer work'"
        )

        parser.add_argument(
            '--set-api-key',
            help='Set API key for Google Gemini',
            metavar='KEY'
        )

        parser.add_argument(
            'question',
            nargs='?',
            help='Question for AI (if not specified --set-api-key)'
        )

        return parser

    def parse_args(self) -> argparse.Namespace:
        args = self.parser.parse_args()
        if not args.set_api_key and not args.question:
            self.print_help()
            sys.exit(1)
        return args

    def print_help(self) -> None:
        help_text = self.parser.format_help()
        self.console.print(Markdown(help_text))


async def main() -> None:
    arg_parser = ArgumentParser()
    args = arg_parser.parse_args()
    config_manager = ConfigManager()
    console = Console()

    try:
        if args.set_api_key:
            config_manager.set_api_key(args.set_api_key)
            console.print("[green]API key saved successfully[/green]")
            return

        if not args.question:
            arg_parser.print_help()
            sys.exit(1)

        ai = AskyAI()
        response = ai.ask_question(args.question)
        ai.display_response(response)

    except KeyboardInterrupt:
        console.print("\n[yellow]Operation interrupted by user[/yellow]")
        sys.exit(130)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]", stderr=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())