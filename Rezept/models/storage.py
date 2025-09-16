from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, Any

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "rezepte.json"

def save_json(data: Dict[str, Any]) -> bool:
    """Зберегти словник з рецептами у файл JSON"""
    try:
        # створюємо папку data, якщо її ще нема
        DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        # відкриваємо файл для запису (w = write)
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            # записуємо словник у форматі JSON
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Fehler beim Speichern: {e}")
        return False

def load_json() -> Dict[str, Any]:
    """Прочитати словник з рецептами із JSON-файлу"""
    try:
        # відкриваємо файл для читання
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)   # повертаємо дані як словник
    except FileNotFoundError:
        # якщо файлу немає – повертаємо порожній словник
        print("Die Datei rezepte.json wurde nicht gefunden.")
        return {}
    except json.JSONDecodeError:
        # якщо файл пошкоджений – повертаємо порожній словник
        print("Fehler: Die Datei rezepte.json ist beschädigt oder leer.")
        return {}
