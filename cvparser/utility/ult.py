from langdetect import detect
import os
def filetype_detect(file:str):
    filetype = file.split('.')[-1]
    return filetype


def language_detect(language:str):
    language = detect(language)
    return language


def get_filename(file:str):
    dotindex=file.rfind('.')


    return file[:dotindex]

def get_filesize(file:str):
    file_size = os.path.getsize(file)
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if file_size < 1024.0:
            return f"{file_size:.2f} {unit}"
        file_size /= 1024.0

