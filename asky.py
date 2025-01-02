import sys
import argparse
import os
import asyncio
from typing import Optional, NoReturn
import google.generativeai as genai
from utils.config import ConfigManager

os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "2"


class AskyAI:
    """Класс для работы с Google Gemini AI"""

    MODEL_NAME = 'gemini-2.0-flash-exp'  # Исправлено название модели

    def __init__(self) -> None:
        self.config_manager = ConfigManager()
        self.api_key = self._initialize_api()
        self.model = self._setup_model()

    def _initialize_api(self) -> str:
        """Инициализация API ключа"""
        api_key = self.config_manager.get_api_key()
        if not api_key:
            self._exit_with_error(
                "API key is not configured. Use --set-api-key to set it.")
        genai.configure(api_key=api_key, transport="grpc")
        return api_key

    def _setup_model(self) -> genai.GenerativeModel:
        """Настройка модели Gemini"""
        try:
            return genai.GenerativeModel(self.MODEL_NAME)
        except Exception as e:
            self._exit_with_error(f"Model initialization error: {e}")

    def ask_question(self, question: str) -> str:  # Убран async
        """
        Отправляет вопрос к API Gemini и получает ответ

        Args:
            question: Текст вопроса

        Returns:
            str: Ответ от AI
        """
        try:
            response = self.model.generate_content(question)  # Убран await
            if not response.text:
                return "Received empty response from AI"
            return response.text
        except Exception as e:
            return f"Error receiving response: {str(e)}"

    @staticmethod
    def _exit_with_error(message: str) -> NoReturn:
        """Выход из программы с сообщением об ошибке"""
        print(message, file=sys.stderr)
        sys.exit(1)


class ArgumentParser:
    """Класс для обработки аргументов командной строки"""

    def __init__(self) -> None:
        self.parser = self._create_parser()

    def _create_parser(self) -> argparse.ArgumentParser:
        """Создание и настройка парсера аргументов"""
        parser = argparse.ArgumentParser(
            description="AskY: Your Console AI Assistant",
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
            nargs='?',  # Делаем аргумент опциональным
            help='Question for AI (if not specified --set-api-key)'
        )

        return parser

    def parse_args(self) -> argparse.Namespace:
        """Разбор аргументов командной строки"""
        args = self.parser.parse_args()

        # Проверяем, что указан хотя бы один из аргументов
        if not args.set_api_key and not args.question:
            self.parser.print_help()
            sys.exit(1)

        return args

    def print_help(self) -> None:
        """Вывод справки"""
        self.parser.print_help()


async def main() -> None:
    """Основная функция программы"""
    arg_parser = ArgumentParser()
    args = arg_parser.parse_args()
    config_manager = ConfigManager()

    try:
        if args.set_api_key:
            config_manager.set_api_key(args.set_api_key)
            print("API key saved successfully")
            return

        if not args.question:
            arg_parser.print_help()
            sys.exit(1)

        ai = AskyAI()
        response = ai.ask_question(args.question)  # Убран await
        print(response)

    except KeyboardInterrupt:
        print("\nOperation interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
