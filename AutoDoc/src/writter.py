import scrapper
import type_enum  as enum
import os, io

#region writer
class writer:
    def __init__(self, readme :io.TextIOWrapper, file_name :str, repo_base_path :str) -> None:
        self._readme = readme
        self._file_name = file_name
        self._repo_base = repo_base_path

    def _get_github_path(self, dir_path :str, file :str, isdir : bool = False) ->str:
        try:
            rel_path = dir_path.split("Epitech-Subjects/")[1] + "/" + file
        except IndexError:
            rel_path = file
        link = self._repo_base + ("tree" if isdir else "blob") + "/main/" + rel_path
        return link

    def _get_gif_relative_path(self, dir_path :str) ->str:
        try:
            rel_path = "../" * dir_path.split("Epitech-Subjects")[1].count('/')
        except IndexError:
            rel_path = ""
        test = rel_path + "assets/voc17.gif"
        return test
    
    def write(self) -> int:
        """
            Base method to write (is overrided by other writter)
        """
        return 0

    def _write_footer(self, destination_path :str, type : enum.type_enum):
        github_path = self._get_github_path(destination_path, "README.md", isdir=True)
        module_path = github_path[:github_path.find("/", github_path.find("/B-") + 1)]
        semester_path = github_path[:github_path.find("/", github_path.find("/Semester-") + 1)]
        semester_name = semester_path[github_path.find("/", github_path.find("/Semester-")) + 1: ]
        home_path = self._repo_base[:-1]

        if (type.value >= enum.type_enum.PROJECT.value):
            self._readme.write(f"[↩️ Revenir au module]({module_path})\n\n")
        if (type.value >= enum.type_enum.MODULE.value):
            self._readme.write(f"[↩️ Revenir au {semester_name}]({semester_path})\n\n")
        if (type.value >= enum.type_enum.SEMESTER.value):
            self._readme.write(f"[↩️ Revenir à l'accueil]({home_path})\n")

        self._write_break()

        footer = f'---\n\n<div align="center">\n\n<a href="https://github.com/Studio-17" target="_blank"><img src="{self._get_gif_relative_path(destination_path)}" width="40"></a>\n\n</div>'
        self._readme.write(footer)

    def _write_break(self, amount : int = 1):
        break_lines = '\n<br>\n\n' * amount
        self._readme.write(break_lines)
#endregion

#region Project writer
class project_writer(writer):
    def __init__(self, readme :io.TextIOWrapper, file_name :str, repo_base_path :str, save :str) -> None:
        super().__init__(readme, file_name, repo_base_path)
        self._save = ""
        if (save != ""):
            self.__parse_save(save)

    def write(self, destination_path :str, person :str, time :str, url :str, browser :str):
        self.__write_project_details(destination_path, person, time)
        self.__write_directory_content(destination_path, 0)
        self.__write_unit_tests(browser, url)
        self._write_footer(destination_path, enum.type_enum.PROJECT)

    def __parse_save(self, save :str):
        try:
            splited = save.split("<details>")[1]
            table = splited.split("</details>")[0]
            self._save = table
        except:
            return
        return

    def __write_directory_content(self, dir_path :str, identation_level : int, max_identation : int = -1):
        is_first_file = identation_level == 0
        files = os.listdir(dir_path)
        for file in files:
            if file == self._file_name:
                continue
            file_path = dir_path + "/" + file
            is_dir = os.path.isdir(file_path)
            if (is_first_file):
                self._readme.write(f"📂---")
                is_first_file = False
            else:
                identation = ("ㅤㅤ" * identation_level) + "|\\_\\_\\_"
                self._readme.write(identation)
            self._readme.write(f"[{file}]({self._get_github_path(dir_path, file, isdir=is_dir)})\n\n")
            if is_dir and (identation_level + 1 <= max_identation or max_identation == -1):
                self.__write_directory_content(file_path, identation_level + 1)
        if (identation_level == 0):
            self._write_break()

    def __write_table_head(self) -> None:
        self._readme.write("""
<details>
<summary> Tests de la moulinette </summary>
<table align="center">
    <thead>
        <tr>
            <td colspan="3" align="center"><strong>MOULINETTE</strong></td>
        </tr>
        <tr>
            <th>SOMMAIRE</th>
            <th>NB DE TESTS</th>
            <th>DETAILS</th>
        </tr>
    </thead>
    <tbody>""".rstrip())

    def __write_table_end(self) -> None:
        self._readme.write('\n\t</tbody>\n</table>\n</details>\n')

    def __write_one_test_cat(self, test_cat : scrapper.test_category) -> None:
        self._readme.write(f"""
        <tr>
            <td rowspan="{test_cat.test_amount}">{test_cat.name}</td>
            <td rowspan="{test_cat.test_amount}" style="text-align: center;">{test_cat.test_amount}</td>
            <td>{test_cat.test_names[0]}</td>
        </tr>
    """)
        for i in range(1, test_cat.test_amount):
            if (i > 1):
                self._readme.write('\n')
            self._readme.write(f"\t\t<tr>\n\t\t\t<td>{test_cat.test_names[i]}</td>\n\t\t</tr>")
        return 0

    def __write_test_save(self):
        self._readme.write("<details>")
        self._readme.write(self._save)
        self._readme.write("</details>\n")
        self._write_break()

    def __write_unit_tests(self, browser :str, url:str):
        if url == " ":
            if (self._save != ""):
                self.__write_test_save()
            return
        test_cats = scrapper.get_mrvn_test(browser, url)
        if (test_cats == None or len(test_cats) == 0) and self._save != "":
            self.__write_test_save()
            return
        self.__write_table_head()
        for test_cat in test_cats:
            self.__write_one_test_cat(test_cat)
        self.__write_table_end()
        self._write_break()

    def __write_project_details(self, destination_path :str, person :str, time :str) -> None:
        project_name = destination_path.split("/")[-1]
        try:
            person = str(int(person))
        except:
            person = "?"
        try:
            time = str(int(time))
        except:
            time = "?"
        self._readme.write(f"# {project_name}\n\n")
        self._readme.write(f"> Timeline: {time} semaines\n\n")
        self._readme.write(f"> Nombre de personnes sur le projet: {person}\n")
        self._write_break()
#endregion

#region Module writer
class module_writer(writer):
    def __init__(self, readme :io.TextIOWrapper, file_name :str, repo_base_path :str, save :str) -> None:
        super().__init__(readme, file_name, repo_base_path)
        self._save = ""
        if (save != ""):
            self.__parse_save(save)

    def __parse_save(self, save :str):
        try:
            splitted = save.split("<table align=\"center\">")[0]
            self._save = splitted   
        except:
            return

    def __write_module_details(self, browser :str, url :str):
        details = scrapper.get_module_details(browser, url)
        self._readme.write(f"# {details.name}  ({details.shortname})\n\n")
        self._readme.write(f"> Crédits disponibles: {details.credits}")
        self._write_break()
        self._readme.write(f"## {details.description}\n\n")
        self._readme.write(f"## {details.competences}")
        self._write_break()

    def __write_empty_module_details(self, destination_path :str):
        if (self._save != ""):
            self._readme.write(self._save[:-1])
            return
        module_name = destination_path.split('/')[-1]
        self._readme.write(f"# {module_name}\n\n")
        self._readme.write(f"> Crédits disponibles: ?")
        self._write_break()

    def __write_head_table(self):
        self._readme.write("""
<table align="center">
    <thead>
        <tr>
            <th>PROJETS</th>
            <th>TIMELINE</th>
        </tr>
    </thead>
    <tbody>""")
        
    def __write_end_table(self):
        self._readme.write("""
    </tbody>
</table>""")
    
    def __write_one_project(self, project_path):
        files = os.listdir(project_path)
        project_name = None
        project_time = None
        for file in files:
            if file != "README.md":
                continue
            file_path = f"{project_path}/{file}"
            with open (file_path, 'r', encoding='utf-8') as project_readme:
                content = project_readme.read()
            project_name = content[content.find("# ") + 2:content.find("\n")]
            project_time = content[content.find("> Timeline: ") + len("> Timeline: "):].split("\n", 1)[0]
            break
        if (project_name != None and project_time != None):
            self._readme.write(f"""
        <tr>
            <td><a href="{self._get_github_path(project_path, "", True)}">{project_name}</a></td>
            <td align="center">{project_time}</td>
        </tr>""")

    def __write_project_list(self, destination_path):
        self.__write_head_table()
        files = os.listdir(destination_path)
        for file in files:
            file_path = f"{destination_path}/{file}"
            if os.path.isdir(file_path):
                self.__write_one_project(file_path)
        self.__write_end_table()
        self._write_break()

    def write(self, destination_path :str, person :str, time :str, url :str, browser :str):
        if (url != " "):
            self.__write_module_details(browser, url)
        else:
            self.__write_empty_module_details(destination_path)
        self.__write_project_list(destination_path)
        self._write_footer(destination_path, enum.type_enum.MODULE)
#endregion

#region Semester writer
class semester_writer(writer):
    def __init__(self, readme :io.TextIOWrapper, file_name :str, repo_base_path :str) -> None:
        super().__init__(readme, file_name, repo_base_path)

    def __write_header(self, destination_path :str):
        semester_nb = destination_path.split("/")[-1].split("-")[1]
        self._readme.write(f"# Semestre {semester_nb}")
        self._readme.write(f"\n\n>  Sur ce répertoire sont réunis tout les sujets et les fichiers qui sont valables durant le semestre {semester_nb}")
        self._write_break()
    
    def __write_table_head(self):
        self._readme.write("""
<table align="center">
    <thead>
        <tr>
            <th>MODULE</th>
            <th>CREDITS</th>
            <th>PROJETS</th>
        </tr>
    </thead>
    <tbody>""")
        
    def _write_table_end(self):
        self._readme.write("""
    </tbody>
</table>""")
        self._write_break()

    def _write_one_module(self, module_path :str, module_name :str):
        projects = os.listdir(module_path)
        projects = [project for project in projects if os.path.isdir(module_path + '/' + project)]
        if (len(projects) == 0):
            projects = [module_name]
        nb_projects = len(projects)
        credits = "?"
        try:
            with open(module_path + "/README.md", 'r', encoding="utf-8") as module_readme:
                content = module_readme.read()
                credits = content.split("> Crédits disponibles: ")[1].split("\n")[0]
        except:
            pass
        self._readme.write(f"""
        <tr>
            <td rowspan="{nb_projects}" style="text-align: center;"><a href="{self._get_github_path(module_path, "", isdir=True)}">{module_name}</a></td>
            <td rowspan="{nb_projects}">{credits}</td>
            <td><a href="{self._get_github_path(module_path, projects[0], isdir=True)}">{projects[0]}</a></td>
        </tr>""")
        projects = projects[1:]
        for project in projects:
            self._readme.write(f"""
        <tr>
            <td><a href="{self._get_github_path(module_path, project, isdir=True)}">{project}</a></td>
        </tr>""")

    def __write_modules(self, destination_path :str):
        files = os.listdir(destination_path)
        for module in files:
            module_path = destination_path + "/" + module
            if os.path.isdir(module_path):
                self._write_one_module(module_path, module)

    def write(self, destination_path :str, person :str, time :str, url :str, browser :str):
        self.__write_header(destination_path)
        self.__write_table_head()
        self.__write_modules(destination_path)
        self._write_table_end()
        self._write_footer(destination_path, enum.type_enum.SEMESTER)
#endregion

#region Global writer
class global_writer(semester_writer):
    def __init__(self, readme :io.TextIOWrapper, file_name :str, repo_base_path :str) -> None:
        super().__init__(readme, file_name, repo_base_path)

    def __write_intro(self):
        self._readme.write(
"""<img src="./assets/bar.png">

<!-- markdown-link-check-disable -->
<div align="center">

<img src="https://img.shields.io/badge/Github-Studio--17-06DFF9"> ![visitor badge](https://visitor-badge.glitch.me/badge?page_id=Studio-17.Epitech-Subjects)

</div>
<!-- markdown-link-check-enable -->

**This directory contains all the subjects and files related to Epitech**

#### :star: Please star the repo if you found it useful!

### If you see a problem, have some new subjects or requests, feel free to open an [issue](https://github.com/Studio-17/Epitech-Subjects/issues) or a [pull request](https://github.com/Studio-17/Epitech-Subjects/pulls).

> **Go checkout the [website for Epitech Subjects](https://clement-fernandes.github.io/epitech-subjects-website/) with some cool features in it!**""")

    def __write_table_head(self):
        self._readme.write("""
<table align="center">
    <thead>
        <tr>
            <th>MODULES</th>
            <th>CREDITS</th>
            <th>PROJECTS</th>
        </tr>
    </thead>
    <tbody>""")
    
    def __write_semester(self, semester_path :str, semester_name :str):
        semester_details = semester_name.split('-')
        self._readme.write(f"""
        <tr>
            <td colspan="3" align="center"><strong>{semester_details[0].upper()} {semester_details[1]}</strong></td>
        </tr>""")
        modules = os.listdir(semester_path)
        for module in modules:
            module_path = f"{semester_path}/{module}"
            if os.path.isdir(module_path):
                self._write_one_module(module_path, module)
        
    def __write_semesters(self, destination_path :str):
        folders = os.listdir(destination_path)
        semesters = [folder for folder in folders if os.path.isdir(folder) and folder.startswith("Semester-")]
        for semester in semesters:
            self.__write_semester(f"{destination_path}/{semester}", semester)


    def write(self, destination_path :str, person :str, time :str, url :str, browser :str):
        self.__write_intro()
        self._write_break()
        self.__write_table_head()
        self.__write_semesters(destination_path)
        self._write_table_end()
        self._write_footer(destination_path, enum.type_enum.GLOBAL)
#endregion