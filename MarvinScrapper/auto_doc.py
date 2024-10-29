#region Import
import sys
import os
import platform
from tkinter import filedialog
#TODO voir si la qualité n'est pas mieux avec from PyQt6.QtWidgets import QFileDialog

SCRAPPER_DIR = "MarvinScrapper"
CURRENT_DIR = os.getcwd()
PLATFORM = platform.system()

if(CURRENT_DIR != SCRAPPER_DIR):
    sys.path.append(os.path.dirname(__file__))

import mrvn_scrapper as mrvn
#endregion

# Dictionnaire des flags avec un id dans les resultat
VALID_FLAGS = {"-h" : -1, "-b" : 0, '-url' : 1}
REPO_BASE_LINK = "https://github.com/Studio-17/Epitech-Subjects/"

#region Directory Tree
def get_github_path(dir_path :str, file :str, isdir : bool = False) ->str:
    rel_path = dir_path.split("Epitech-Subjects/")[1] + "/" + file
    link = REPO_BASE_LINK + ("tree" if isdir else "blob") + "/main/" + rel_path
    return link

def write_directory_content(dir_path : str, identation_level : int, readme):
    is_first_file = identation_level == 0
    files = os.listdir(dir_path)
    for file in files:
        if file == "README.md":
            continue
        file_path = dir_path + "/" + file
        is_dir = os.path.isdir(file_path)
        if (is_first_file):
            readme.write(f"📂---")
            is_first_file = False
        else:
            identation = ("ㅤㅤ" * identation_level) + "|\\_\\_\\_"
            readme.write(identation)
        readme.write(f"[{file}]({get_github_path(dir_path, file, isdir=is_dir)})\n\n")
        if is_dir:
            write_directory_content(file_path, identation_level + 1, readme)
#endregion

#region Footer
def write_footer(destination_path : str, readme):
    footer = '---\n\n<div align="center">\n\n<a href="https://github.com/Studio-17" target="_blank"><img src="../../../assets/voc17.gif" width="40"></a>\n\n</div>'
    readme.write(footer)
#endregion

def write_break(readme, amount : int):
    break_lines = '\n<br>\n\n' * amount
    readme.write(break_lines)

def main():
    (browser, url) = mrvn.parse_param(sys.argv, VALID_FLAGS, "auto_doc")
    destination_path = filedialog.askdirectory(initialdir=CURRENT_DIR)
    with open(f"{destination_path}/README.md", "w", encoding="utf-8") as readme:
        #TODO Write all the project details (add param if needed)
        write_directory_content(destination_path, 0, readme)
        write_break(readme, 1)
        #TODO Write all the project tests
        write_footer(destination_path, readme)
    print(browser, url)


if __name__ == "__main__":
    main()