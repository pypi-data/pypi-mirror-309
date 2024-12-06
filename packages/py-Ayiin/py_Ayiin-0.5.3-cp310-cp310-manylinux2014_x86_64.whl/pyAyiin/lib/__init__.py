from .aihelp import OpenAi
from .chrome import Chrome
from .events import Event
from .FastTelethon import download_file, upload_file
from .format import Format
from .paste import Paste
from .pasteBin import PasteBin
from .thumbnail import Thumbnail
from .utils import Utils


class Lib(
    Chrome,
    Event,
    Format,
    OpenAi,
    Paste,
    Thumbnail,
    Utils
):
    pass


__all__ = [
    "Chrome",
    "Event",
    "Format",
    "OpenAi",
    "Paste",
    "PasteBin",
    "Utils",
    "Thumbnail",
    "download_file",
    "upload_file"
]
