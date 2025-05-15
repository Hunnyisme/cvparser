import re
from pathlib import Path
from cvparser.factories.parserfactory import *
from cvparser.Enum.filetype import *


class loader:
    @staticmethod
    def load(file:str,filetype:FileType=None):
        if "\\" in file or "/" in file:
            file = re.sub(r"[/\\]+", "/", file)
        file_path=Path(file).resolve(strict=False)

        return parserfactory.get_parser(str(file_path),filetype)


