from .auth import BricksCMSLoginView
from .dashboard import dashboard
from .single_list import single_list
from .edit_page import edit_page
from .collection_list import collection_list
from .add_collection_entry import add_collection_entry
from .edit_collection_entry import edit_collection_entry
from .settings_page import settings_page

__all__ = [
    "BricksCMSLoginView",
    "dashboard",
    "single_list",
    "edit_page",
    "collection_list",
    "add_collection_entry",
    "edit_collection_entry",
    "settings_page",
]
