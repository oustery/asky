from pathlib import Path
import json
from typing import Dict, Optional


class ConfigManager:
    def __init__(self):
        self.config_dir = Path.home() / ".asky"
        self.config_path = self.config_dir / "config.json"
        self.config: Dict[str, str] = {}

        try:
            # Создаем директорию с безопасными правами доступа
            self.config_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
            self.load_config()
        except PermissionError:
            raise PermissionError(
                f"No permission to create directory {self.config_dir}")
        except Exception as e:
            raise RuntimeError(
                f"Error creating configuration directory: {e}")

    def load_config(self) -> None:
        """Загружает конфигурацию из файла"""
        try:
            if self.config_path.exists():
                with self.config_path.open('r', encoding='utf-8') as f:
                    self.config = json.load(f)
        except json.JSONDecodeError:
            raise ValueError("Invalid configuration file format")
        except Exception as e:
            raise RuntimeError(f"Error reading configuration: {e}")

    def save_config(self) -> None:
        """Сохраняет конфигурацию в файл"""
        try:
            with self.config_path.open('w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise RuntimeError(f"Error saving configuration: {e}")

    def set_api_key(self, api_key: str) -> None:
        """Устанавливает ключ API в конфигурационном файле"""
        if not api_key or not isinstance(api_key, str):
            raise ValueError("The API key must be a non-empty string")

        self.config['api_key'] = api_key
        self.save_config()

    def get_api_key(self) -> Optional[str]:
        """Возвращает сохраненный ключ API"""
        return self.config.get('api_key')

    @property
    def config_file(self) -> Path:
        """Возвращает путь к файлу конфигурации"""
        return self.config_path
