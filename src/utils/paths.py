import os
import sys
from pathlib import Path

def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent

def get_assets_path() -> Path:
    return get_project_root() / "assets"

def get_image_path(filename: str) -> Path:
    return get_assets_path() / "images" / filename

def get_font_path(filename: str) -> Path:
    return get_assets_path() / "fonts" / filename