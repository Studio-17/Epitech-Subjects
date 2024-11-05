import scrapper
import type_enum  as enum
import os

class writer:
    def __init__(self, readme, repo_base_path :str) -> None:
        self.readme = readme
        self.repo_base = repo_base_path

    def _get_github_path(self, dir_path :str, file :str, isdir : bool = False) ->str:
        rel_path = dir_path.split("Epitech-Subjects/")[1] + "/" + file
        link = self.repo_base + ("tree" if isdir else "blob") + "/main/" + rel_path
        return link

    def _get_gif_relative_path(self, dir_path :str) ->str:
        test = "../" * dir_path.split("Epitech-Subjects")[1].count('/') + "assets/voc17.gif"
        return test
    
    def write(self) -> int:
        """
            Base method to write (is overrided by other writter)
        """
        return 0

    #region Footer
    def _write_footer(self, destination_path :str, type : enum.type_enum):
        github_path = self._get_github_path(destination_path, "README.md", isdir=True)
        module_path = github_path[:github_path.find("/", github_path.find("/B-") + 1)]
        semester_path = github_path[:github_path.find("/", github_path.find("/Semester-") + 1)]
        semester_name = semester_path[github_path.find("/", github_path.find("/Semester-")) + 1: ]
        home_path = self.repo_base[:-1]

        if (type.value >= enum.type_enum.PROJECT.value):
            self.readme.write(f"[↩️ Revenir au module]({module_path})\n\n")
        if (type.value >= enum.type_enum.MODULE.value):
            self.readme.write(f"[↩️ Revenir au {semester_name}]({semester_path})\n\n")
        if (type.value >= enum.type_enum.SEMESTER.value):
            self.readme.write(f"[↩️ Revenir à l'accueil]({home_path})\n")

        self._write_break()

        footer = f'---\n\n<div align="center">\n\n<a href="https://github.com/Studio-17" target="_blank"><img src="{self._get_gif_relative_path(destination_path)}" width="40"></a>\n\n</div>'
        self.readme.write(footer)
    #endregion

    def _write_break(self, amount : int = 1):
        break_lines = '\n<br>\n\n' * amount
        self.readme.write(break_lines)

class project_writer(writer):
    def __init__(self, readme, repo_base_path :str) -> None:
        super().__init__(readme, repo_base_path)
    
    def write(self, destination_path :str, person :str, time :str, url :str, browser :str):
        self.__write_project_details(destination_path, person, time)
        self.__write_directory_content(destination_path, 0)
        if (url != " "):
            self.__write_unit_tests(browser, url)
        self._write_footer(destination_path, enum.type_enum.PROJECT)

    #region Directory Tree
    def __write_directory_content(self, dir_path :str, identation_level : int, max_identation : int = -1):
        is_first_file = identation_level == 0
        files = os.listdir(dir_path)
        for file in files:
            if file == "README.md":
                continue
            file_path = dir_path + "/" + file
            is_dir = os.path.isdir(file_path)
            if (is_first_file):
                self.readme.write(f"📂---")
                is_first_file = False
            else:
                identation = ("ㅤㅤ" * identation_level) + "|\\_\\_\\_"
                self.readme.write(identation)
            self.readme.write(f"[{file}]({self._get_github_path(dir_path, file, isdir=is_dir)})\n\n")
            if is_dir and (identation_level + 1 <= max_identation or max_identation == -1):
                self.__write_directory_content(file_path, identation_level + 1)
        if (identation_level == 0):
            self._write_break()
    #endregion
    
    #region UnitTests
    def __write_table_head(self) -> None:
        self.readme.write("""
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
        self.readme.write('\n\t</tbody>\n</table>\n')

    def __write_one_test_cat(self, test_cat : scrapper.test_category) -> None:
        self.readme.write(f"""
        <tr>
            <td rowspan="{test_cat.test_amount}">{test_cat.name}</td>
            <td rowspan="{test_cat.test_amount}" style="text-align: center;">{test_cat.test_amount}</td>
            <td>{test_cat.test_names[0]}</td>
        </tr>
    """)
        for i in range(1, test_cat.test_amount):
            if (i > 1):
                self.readme.write('\n')
            self.readme.write(f"\t\t<tr>\n\t\t\t<td>{test_cat.test_names[i]}</td>\n\t\t</tr>")
        return 0

    def __write_unit_tests(self, browser :str, url:str):
        test_cats = scrapper.get_mrvn_test(browser, url)
        if test_cats == None or len(test_cats) == 0:
            return
        self.__write_table_head()
        for test_cat in test_cats:
            self.__write_one_test_cat(test_cat)
        self.__write_table_end()
        self._write_break()
    #endregion

    #region Project Details
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
        self.readme.write(f"# {project_name}\n\n")
        self.readme.write(f"> Timeline: {time} semaines\n\n")
        self.readme.write(f"> Nombre de personnes sur le projet: {person}\n")
        self._write_break()
    #endregion

#region Module details
class module_writer(writer):
    def __init__(self, readme, repo_base_path: str) -> None:
        super().__init__(readme, repo_base_path)

    def __write_module_details(self, browser :str, url :str):
        details = scrapper.get_module_details(browser, url)
        self.readme.write(f"# {details.name}  ({details.shortname})\n\n")
        self.readme.write(f"> Crédits disponibles: {details.credits}")
        self._write_break()
        self.readme.write(f"## {details.description}\n\n")
        self.readme.write(f"## {details.competences}")
        self._write_break()

    def __write_head_table(self):
        self.readme.write("""
<table align="center">
    <thead>
        <tr>
            <th>PROJETS</th>
            <th>TIMELINE</th>
        </tr>
    </thead>
    <tbody>""")
        
    def __write_end_table(self):
        self.readme.write("""
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
            self.readme.write(f"""
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
        self.__write_project_list(destination_path)
        self._write_footer(destination_path, enum.type_enum.MODULE)
#endregion