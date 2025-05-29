from cvparser.extracter.extractor import Extractor
import spacy
import re
import phonenumbers
from phonenumbers import PhoneNumberFormat

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
        #print("----------------------")
        #self.__get_age(nlp_doc)
        print("----------------------")
        print(self.get_personal_information())
        print("----------------------")
        print(self.extract_email_addresses())


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

        pattern=r"(?:Birth Year|Year of Birth|Born in|Graduated in|from|Birth Date)\s*[:\-]?[ \t]*(?:19|20)\d{2}"

        age_res=re.search(pattern, self.doc.text, re.IGNORECASE).group()

        res=re.search(r"\w*(\d+)",age_res,re.IGNORECASE).group()

        return res

    def __get_company_discription(nlp_doc):
          raise NotImplementedError



    def get_personal_information(self):

        return self.__extract_phone_numbers()

    def __extract_phone_numbers(self):
        found_numbers = set()  # 使用 set 去重

        phone_pattern = re.compile(
            r'(?:(?:\+\d{1,3}[-.\s]*)?  (e.g., +1, +86)(?:(?:\(\d{1,4}\)|\d{1,4})[-.\s]*)? \d{2,4}[-.\s]* ){2,}\d{2,4} | \b\d{7,15}\b ',
            re.VERBOSE)

        # 遍历所有可能的电话号码匹配项
        for match in phone_pattern.finditer(self.doc.text):
            potential_number_str = match.group(0)

            try:
                # 尝试使用 phonenumbers 库解析号码
                # default_region 参数很重要，当号码没有国家代码时，它会尝试根据该地区解析
                parsed_number = phonenumbers.parse(potential_number_str,'AU')

                # 检查号码是否有效且可能
                if phonenumbers.is_valid_number(parsed_number) and phonenumbers.is_possible_number(parsed_number):
                    # 将有效号码格式化为 E.164 国际标准格式（例如 +61412345678）
                    # 也可以选择 PhoneNumberFormat.NATIONAL (例如 (04) 1234 5678)
                    formatted_number = phonenumbers.format_number(parsed_number, PhoneNumberFormat.E164)
                    found_numbers.add(formatted_number)
                # else:
                # print(f"Skipping invalid/impossible number: {potential_number_str}")
            except phonenumbers.NumberParseException:
                # 如果解析失败，则跳过此匹配项
                # print(f"Failed to parse: {potential_number_str}")
                pass

            return list(found_numbers)

    def extract_email_addresses(self):
        """
        从文本中提取邮箱地址。
        匹配标准的邮箱地址格式。
        """
        email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
        return list(set(email_pattern.findall(self.doc.text)))  # 使用 set 去重


















