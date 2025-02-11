"""Configuration module"""

from pathlib import Path
from dataclasses import dataclass

import toml
import dacite


@dataclass
class ConfigSettings:
    """Dataclass representing the settings loaded from the configuration file"""

    @dataclass
    class ConfigSettingsQuote:
        """Settings related to quote generation"""

        quality: int
        text_color: str
        background_color: str

    @dataclass
    class ConfigSettingsLogging:
        """Settings for logging configuration"""

        level: str

    @dataclass
    class ConfigSettingsServer:
        """Settings for server configuration"""

        port: int

    quote: ConfigSettingsQuote
    logging: ConfigSettingsLogging
    server: ConfigSettingsServer


@dataclass
class ConfigDefaults:
    """Dataclass for default configuration values"""

    templates_path = Path("app/templates")
    colors = [
        "#fb6169",
        "#85de85",
        "#f3bc5c",
        "#65bdf3",
        "#b48bf2",
        "#ff5694",
        "#62d4e3",
        "#faa357"
    ]
    entity_map = {
        "bold": ("<b>", "</b>"),
        "pre": ("<code>", "</code>"),
        "code": ("<code>", "</code>"),
        "italic": ("<i>", "</i>"),
        "underline": ("<u>", "</u>"),
        "strikethrough": ("<del>", "</del>"),
        "strike": ("<del>", "</del>"),
        "url": ("<a>", "</a>")
    }


@dataclass
class Config:
    """Dataclass that combines settings and defaults"""

    settings: ConfigSettings
    defaults = ConfigDefaults()


def parse_config() -> Config:
    """Parses the configuration file and returns a Config object"""
    config_file = Path("config.toml")
    if not config_file.exists():
        raise FileNotFoundError(f"Config file not found: `{config_file}` no such file")

    with config_file.open("r", encoding="utf-8") as file:
        data = toml.load(file)

    return dacite.from_dict(data_class=Config, data=data)
