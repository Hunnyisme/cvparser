import re


def clean_text(text):

    text = re.sub(r"\f+", "\n", text)


    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)


    text = re.sub(r"\s+", " ", text).strip()



    return text