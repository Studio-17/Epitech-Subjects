#region Import
import sys
import os
from tkinter import filedialog
from datetime import datetime
import pyperclip

SOURCE_DIR = "AutoDoc/src"
CURRENT_DIR = os.getcwd()

if(CURRENT_DIR != SOURCE_DIR):
    sys.path.append(os.path.dirname(__file__))

import type_enum as enum
import writter
import param
#endregion

# Dictionnaire des flags avec un id dans les resultat et un nombre de param
VALID_FLAGS = {"-h" : [-1, 0], "-b" : [0, 1], '-url' : [1, 1], "-p" : [2, 1], "-t" : [3, 1], "-cp" : [4, 0], "--type" :[5, 1]}
REPO_BASE_LINK = "https://github.com/Studio-17/Epitech-Subjects/"
REPO_NAME = "Epitech-Subjects"
SEMESTER_NAME = "Semester-"

def get_readme_type(path :str, type_param :str) ->enum.type_enum:
    if (type_param != " "):
        match(type_param):
            case "g":
                return enum.type_enum.GLOBAL
            case "s":
                return enum.type_enum.SEMESTER
            case "m":
                return enum.type_enum.MODULE
            case "p":
                return enum.type_enum.PROJECT
            case _:
                print("Invalid --type value passed, normal configuration will be used")
    splitted_path = path.split('/')
    if (splitted_path[-1] == REPO_NAME):
        return enum.type_enum.GLOBAL
    if (splitted_path[-1].startswith(SEMESTER_NAME)):
        return enum.type_enum.SEMESTER
    if (len(splitted_path) >= 2 and splitted_path[-2].startswith(SEMESTER_NAME)):
        return enum.type_enum.MODULE
    return enum.type_enum.PROJECT


def create_readme(path :str = None):
    filename = "README.md"
    (browser, url, person, time, copy, type_param) = param.parse_param(sys.argv, VALID_FLAGS, "auto_doc")
    if (path == None):
        destination_path = filedialog.askdirectory(initialdir=CURRENT_DIR)
    else:
        # On créer uniquement des README par défaut dans ce cas
        copy = False 
        url = " "
        type_param = " "
        destination_path = path
    doc_type = get_readme_type(destination_path, type_param)

    if (os.path.exists(destination_path) == False):
        exit(84)
    if (type(copy) is bool and copy == True):
        filename = "README" + str(datetime.now().timestamp()) + ".md"

    readme_path = f"{destination_path}/{filename}"
    save = ""
    if (os.path.exists(readme_path)):
        with open(readme_path, "r", encoding="utf-8") as readme:
            save = readme.read()

    with open(readme_path, "w", encoding="utf-8") as readme:
        doc = None
        match(doc_type.value):
            case enum.type_enum.PROJECT.value:
                doc = writter.project_writer(readme, filename, REPO_BASE_LINK, save)
            case enum.type_enum.MODULE.value:
                doc = writter.module_writer(readme, filename, REPO_BASE_LINK, save)
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
