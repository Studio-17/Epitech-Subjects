import src.auto_doc as doc
import os

REPO_DIR = os.getcwd()


def search_readme(directory :str, depth :int):
    assert os.path.isdir(directory)
    actual_depth = directory.count('\\')
    # Parcours en Bottom up pour que tout les readme soient bien fait
    for path, dirs, files in os.walk(directory, topdown=False):
        print (path)
        if path.find("Semester") == -1:
            continue
        if path.count("\\") > actual_depth + depth:
            continue
        path = path.replace("\\", "/")
        if "README.md" not in files:
            print(path + " is not valid")
            doc.create_readme(path)

def main():
    search_readme(REPO_DIR, 3)

if __name__ == "__main__":
    main()