from cvparser.parser.parser import parser
from pdfminer.high_level import *

class pdfparser(parser):

    def __init__(self,file,filetype):
        super().__init__(file,filetype)



    def parse(self):
        output_string = StringIO()
        with open(self.file, 'rb') as fin:
            extract_text_to_fp(fin, output_string)

        print(output_string.getvalue().strip())


