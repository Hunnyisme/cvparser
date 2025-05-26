from cvparser.extracter.extractor import Extractor
import spacy
import re

class EnglishExtractor(Extractor):
    def __init__(self, doc):
        super().__init__(doc)


    def extract(self):
        nlp=spacy.load('en_core_web_trf')
        nlp_doc=nlp(self.doc.text)
        person_name=self.__get_person_name(nlp_doc)
        #print(person_name)
        # for token in nlp_doc:
        #     #if token.ent_type_ !="":
        #     if token.ent_type_=="ORG" or token.ent_type_=="DATE":
        #      print( token.text,token.ent_type_)
        #print(self.__get_school_list(nlp_doc))

        #print(self.__get_company_list(nlp_doc))
        print(self.__get_work_date_company(nlp_doc))
        print("----------------------")
        print(self.__get_education_date(nlp_doc))
        print("----------------------")
        self.__get_age(nlp_doc)
        #print("----------------------")


    def __get_person_name(self, nlp_doc):
        for token in nlp_doc.ents:
            if token.label_ == 'PERSON':
                return token.text

        return None

    def __get_org_name(self, nlp_doc):
        orglist=[]
        for token in nlp_doc.ents:
            if token.label_ == 'ORG':
                orglist.append(token.text)

        return  orglist

    def __get_address_list(self, nlp_doc):
        address_list=[]
        for token in nlp_doc.ents:
            if token.label_ == 'GPE' or token.label_ == 'FAC' or token.label_ == 'LOC':
                address_list.append(token.text)

        return address_list

    def __get_school_list(self, nlp_doc):
        school_list=[]
        orglist=self.__get_org_name(nlp_doc)
        for o in orglist:
            match=re.search(r".+?school|.+?college|.+?university", o,re.IGNORECASE)
            if match is not None:
               school_list.append(match.group())

        return school_list

    def __get_company_list(self, nlp_doc):
        company_list=[]
        pattern=r"\b[A-Za-z\s\-\(\)]+(?:Inc\.|Corporation|Limited|Group|Co\.|LLC|PLC|AG|SE|Company|Holdings|LLP)\b"
        orglist = self.__get_org_name(nlp_doc)
        for o in orglist:
            match=re.search(pattern, o, re.IGNORECASE)
            if match is not None:
                company_list.append(match.group())

        return company_list

    def __is_company(self,text):
        pattern = r"\b[A-Za-z\s\-\(\)]+(?:Inc\.|Corporation|Limited|Group|Co\.|LLC|PLC|AG|SE|Company|Holdings|LLP)\b"
        if re.search(pattern, text, re.IGNORECASE):
            return True
        return False


    def __get_work_date_company(self, nlp_doc):
        work_date_company={}
        ents = nlp_doc.ents
        ents_list=[]
        for ent in ents:
            if ent.label_ == 'DATE' or ent.label_ == 'ORG':
                ents_list.append(ent)
        for i in range(len(ents_list)):
            if self.__is_company(ents_list[i].text) and i+1 < len(ents_list) and ents_list[i+1].label_ == 'DATE':
                work_date_company.update({ents_list[i].text: ents_list[i+1].text})

        return work_date_company

    def __is_school(self,text):
        pattern=r".+?school|.+?college|.+?university"
        if re.search(pattern, text, re.IGNORECASE):
            return True
        return False


    def __get_education_date(self, nlp_doc):
        education_date={}
        ents = nlp_doc.ents
        ents_list = []
        for ent in ents:
            if ent.label_ == 'DATE' or ent.label_ == 'ORG':
                ents_list.append(ent)

        for i in range(len(ents_list)):
            if self.__is_school(ents_list[i].text) and i+1 < len(ents_list) and ents_list[i+1].label_ == 'DATE':
                education_date.update({ents_list[i].text: ents_list[i+1].text})


        return education_date

    def __get_age(self,nlp_doc):
        #ents = doc.ents
        #ents_list = []

        pattern=r"(?:Birth Year|Year of Birth|Born in|Graduated in|from|Birth Date)\s*[:\-]?[ \t]*(?:19|20)\d{2}"
        # for ent in ents:
        #     # if ent.label_ == 'QUANTITY' or ent.label_ == 'CARDINAL'  :
        #     #     ents_list.append(ent)
        #     print(ent.text, ent.label_)
        age_res=re.search(pattern, self.doc.text, re.IGNORECASE).group()
             # if re.search(pattern, token.text, re.IGNORECASE):
             #     age_list.append(token.text)
        res=re.search(r"\w*(\d+)",age_res,re.IGNORECASE).group()

        return res




















