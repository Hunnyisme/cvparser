from cvparser.Enum.filetype import *
from cvparser.Enum.language import *
from cvparser.parser.pdfparser import pdfparser
from cvparser.utility.ult import filetype_detect


class parserfactory:
    @staticmethod
    def get_parser(file,filetype:FileType=None):
        _filetype = filetype_detect(file)
        if filetype is None:
            if _filetype == FileType.PDF.value:
                return pdfparser(file,_filetype)





