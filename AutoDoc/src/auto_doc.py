#region Import
import sys
import os
from tkinter import filedialog
import pyperclip
from datetime import datetime

SOURCE_DIR = "AutoDoc/src"
CURRENT_DIR = os.getcwd()

if(CURRENT_DIR != SOURCE_DIR):
    sys.path.append(os.path.dirname(__file__))

import type_enum as enum
import writter
import param
#endregion

# Dictionnaire des flags avec un id dans les resultat et un nombre de param
VALID_FLAGS = {"-h" : [-1, 0], "-b" : [0, 1], '-url' : [1, 1], "-p" : [2, 1], "-t" : [3, 1], "-cp" : [4, 0]}
REPO_BASE_LINK = "https://github.com/Studio-17/Epitech-Subjects/"

def main(doc_type : enum.type_enum):
    filename = "README.md"
    (browser, url, person, time, copy) = param.parse_param(sys.argv, VALID_FLAGS, "auto_doc")
    destination_path = filedialog.askdirectory(initialdir=CURRENT_DIR)

    if (os.path.exists(destination_path) == False):
        exit(84)
    if (type(copy) is bool and copy == True):
        filename = "README" + str(datetime.now().timestamp()) + ".md"

    with open(f"{destination_path}/{filename}", "w", encoding="utf-8") as readme:
        doc = None
        match(doc_type.value):
            case enum.type_enum.PROJECT.value:
                doc = writter.project_writer(readme, filename, REPO_BASE_LINK)
            case enum.type_enum.MODULE.value:
                doc = writter.module_writer(readme, filename, REPO_BASE_LINK)
            case enum.type_enum.SEMESTER.value:
                doc = writter.semester_writer(readme, filename, REPO_BASE_LINK)
            case enum.type_enum.GLOBAL.value:
                doc = writter.global_writer(readme, filename, REPO_BASE_LINK)
            case _:
                exit(84)
        doc.write(destination_path, person, time, url, browser)

    if (type(copy) is bool and copy == True):
        with open(f"{destination_path}/{filename}", "r", encoding="utf-8") as readme:
            pyperclip.copy(readme.read())
        print("\nReadme copied to clipboard\n")
        os.remove(f"{destination_path}/{filename}")
