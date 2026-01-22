# core/context_processors.py
from .menu import menu_registry


def menu_items(request):
    return {
        "main_menu": menu_registry.get_items("main"),
        "user_menu": menu_registry.get_items("user"),
    }
