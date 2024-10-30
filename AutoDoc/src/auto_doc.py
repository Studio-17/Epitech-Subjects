#region Import
import sys
import os
import platform
from tkinter import filedialog
#TODO voir si la qualité n'est pas mieux avec from PyQt6.QtWidgets import QFileDialog

SOURCE_DIR = "AutoDoc/src"
CURRENT_DIR = os.getcwd()
PLATFORM = platform.system()

if(CURRENT_DIR != SOURCE_DIR):
    sys.path.append(os.path.dirname(__file__))

import mrvn_scrapper as mrvn
import writter
import param

#endregion

# Dictionnaire des flags avec un id dans les resultat
VALID_FLAGS = {"-h" : -1, "-b" : 0, '-url' : 1, "-p" : 2, "-t" : 3}
REPO_BASE_LINK = "https://github.com/Studio-17/Epitech-Subjects/"

def main():
    (browser, url, person, time) = param.parse_param(sys.argv, VALID_FLAGS, "auto_doc")
    destination_path = filedialog.askdirectory(initialdir=CURRENT_DIR)
    with open(f"{destination_path}/README.md", "w", encoding="utf-8") as readme:
        doc = writter.writer(readme, REPO_BASE_LINK)
        doc.write_project_details(destination_path, person, time)
        doc.write_break(1)
        doc.write_directory_content(destination_path, 0)
        if (url != " "):
            doc.write_break(1)
            doc.write_unit_tests(browser, url)
        doc.write_break(1)
        doc.write_footer(destination_path)
    print(browser, url)
