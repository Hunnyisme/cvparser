from cvparser.Enum.filetype import *
from cvparser.Enum.language import *
from cvparser.parser.pdf_parser import Pdfparser
from cvparser.utility.ult import filetype_detect


class ParserFactory:
    @staticmethod
    def get_parser(file,filetype:FileType=None):
        _filetype = filetype_detect(file)
        if filetype is None:
            if _filetype == FileType.PDF.value:
                return Pdfparser(file, _filetype)





