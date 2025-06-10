import re

import spacy
from pdfminer.high_level import *
from pathlib import Path
import cvparser.cv_parser
from cvparser.factories.extractor_factory import ExtractorFactory

from cvparser.utility.ult import *
from cvparser.cv_parser import *
if __name__ == '__main__':


    parser=CvParser.load("")

    #print(FileType.PDF.value)
    #print(str(sanitize_path("E:\\onedrivefiles\\OneDrive\\PycharmProjects\\cvparser\\test_data\\resume-de.pdf")))
    doc=parser.parse()
    print(doc.text)
    print("-----------------------")
    the_cv=ExtractorFactory.get_extractor(doc,'Australia').extract()
    print(the_cv)
    # check single
    print(the_cv.skills)
    print(the_cv.name)
    # print(parser.file)

    # print(parser.filetype)
    # print(parser.filesize)
    # print(filetype_detect("asiii.txt.pdf .zip"))
    # print(language_detect("I am your father"))
    # print(get_filename("asiii.zip"))
    # print(get_filesize(r"E:\onedrivefiles\OneDrive\PycharmProjects\cvparser\test_data\resume-de.pdf"))
    # nlp = spacy.load("en_core_web_trf")
    # print(nlp.pipe_names)
    # doc = nlp("Autonomous cars shift insurance liability toward manufacturers.")
    # lem=nlp.get_pipe("lemmatizer")
    #
    #
    # for token in doc:
    #     print(token.text+"-"+"left:")
    #     print([t.text for t in token.lefts])
    #     print(token.text+"-"+"right:")
    #     print([t.text for t in token.rights])
    #
    # print("------------------------------")
    #
    #
    #

    # print(nlp.pipe_names)
    # root = [token for token in doc if token.head == token]
    # subject = list(root[0].lefts)
    # for descendant in subject.subtree:
    #     assert subject is descendant or subject.is_ancestor(descendant)
    #     print(descendant.text, descendant.dep_, descendant.n_lefts,
    #             descendant.n_rights,
    #             [ancestor.text for ancestor in descendant.ancestors])
    # for token in doc:
    #     print(token.text+":")
    #     print([i for i in token.ancestors])
    #     print(token.head.text)

    # print(doc[6].text+"-lefs:")
    # print([i for i in doc[6].lefts])
    # print(doc[4].text+"-lefs:")
    # print([i for i in doc[4].lefts])
    # print(doc[4].text+"-lefsedge:")
    # print(doc[4].left_edge)
    # print(doc[6].text+"-lefsedge:")
    # print(doc[6].left_edge)
    # print(doc[0].text+"-ancestor:")
    # print([i for i in doc[0].ancestors])
    # print(doc[6].text+"-rightsedge:")
    # print([i for i in doc[6].rights])
    # print(doc[6].text+"-rightsedge:")
    # print(doc[6].right_edge)
    # print(doc[doc[6].left_edge.i:doc[6].right_edge.i+1])
    # print(doc[0:2])
    # doc = nlp("Zhengjie is my friend")
    # print(doc)
    # for ent in doc:
    #     print(ent.text,ent.ent_type_,ent.ent_iob_)
    # output_string = StringIO()
    #
    # with open('../test_data/resume-de.pdf', 'rb') as fin:
    #     extract_text_to_fp(fin, output_string)
    #
    # text= pre_clean.clean_text(output_string.getvalue())
    #
    # print(text)
    #print("-----------------------------------------")

    # with open('resume-de.pdf', 'rb') as fin:
    #     extract_text_to_fp(fin, output_string)

    #
    # doc=nlp(output_string.getvalue().strip())
    # for token in doc:
    #      if token.ent_type_=="DATE":
    #          print(token.text.strip())
