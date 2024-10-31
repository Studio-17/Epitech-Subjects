#region Import
import sys
import os
import platform
from tkinter import filedialog
import pyperclip
from datetime import datetime
#TODO voir si la qualité n'est pas mieux avec from PyQt6.QtWidgets import QFileDialog

SOURCE_DIR = "AutoDoc/src"
CURRENT_DIR = os.getcwd()

if(CURRENT_DIR != SOURCE_DIR):
    sys.path.append(os.path.dirname(__file__))

import src.enum.type_enum as enum
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

    if (type(copy) is bool and copy == True):
        filename = "README" + str(datetime.now().timestamp()) + ".md"

    with open(f"{destination_path}/{filename}", "w", encoding="utf-8") as readme:
        doc = None
        match(doc_type.value):
            case enum.type_enum.PROJECT.value:
                doc = writter.project_writer(readme, REPO_BASE_LINK)
            case enum.type_enum.MODULE.value:
                #TODO write module content
                return 0
            case enum.type_enum.SEMESTER.value:
                #TODO write semester content
                return 0
        doc.write(destination_path, person, time, url, browser)

    if (type(copy) is bool and copy == True):
        with open(f"{destination_path}/{filename}", "r", encoding="utf-8") as readme:
            pyperclip.copy(readme.read())
        print("\nReadme copied to clipboard\n")
        os.remove(f"{destination_path}/{filename}")
