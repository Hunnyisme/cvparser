from cvparser.extracter.extractor import Extractor
import spacy
import re

class EnglishExtractor(Extractor):
    def __init__(self, doc):
        super().__init__(doc)


    def extract(self):
        nlp=spacy.load('en_core_web_trf')
        doc=nlp(self.doc.text)
        person_name=self.__get_person_name(doc)
        #print(person_name)
        # for token in doc:
        #     #if token.ent_type_ !="":
        #     if token.ent_type_=="ORG" or token.ent_type_=="DATE":
        #      print( token.text,token.ent_type_)
        #print(self.__get_school_list(doc))

        #print(self.__get_company_list(doc))
        print(self.__get_work_date_company(doc))
        print("----------------------")
        print(self.__get_education_date(doc))


    def __get_person_name(self,doc):
        for token in doc.ents:
            if token.label_ == 'PERSON':
                return token.text

        return None

    def __get_org_name(self, doc):
        orglist=[]
        for token in doc.ents:
            if token.label_ == 'ORG':
                orglist.append(token.text)

        return  orglist

    def __get_address_list(self,doc):
        address_list=[]
        for token in doc.ents:
            if token.label_ == 'GPE' or token.label_ == 'FAC' or token.label_ == 'LOC':
                address_list.append(token.text)

        return address_list

    def __get_school_list(self,doc):
        school_list=[]
        orglist=self.__get_org_name(doc)
        for o in orglist:
            match=re.search(r".+?school|.+?college|.+?university", o,re.IGNORECASE)
            if match is not None:
               school_list.append(match.group())

        return school_list

    def __get_company_list(self,doc):
        company_list=[]
        pattern=r"\b[A-Za-z\s\-\(\)]+(?:Inc\.|Corporation|Limited|Group|Co\.|LLC|PLC|AG|SE|Company|Holdings|LLP)\b"
        orglist = self.__get_org_name(doc)
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


    def __get_work_date_company(self,doc):
        work_date_company={}
        ents = doc.ents
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


    def __get_education_date(self,doc):
        education_date={}
        ents = doc.ents
        ents_list = []
        for ent in ents:
            if ent.label_ == 'DATE' or ent.label_ == 'ORG':
                ents_list.append(ent)

        for i in range(len(ents_list)):
            if self.__is_school(ents_list[i].text) and i+1 < len(ents_list) and ents_list[i+1].label_ == 'DATE':
                education_date.update({ents_list[i].text: ents_list[i+1].text})


        return education_date

    def __get_age(self,doc):
        ents = doc.ents
        ents_list = []




















