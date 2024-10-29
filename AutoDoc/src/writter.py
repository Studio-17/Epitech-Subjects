import mrvn_scrapper as mrvn
import os

class writer:
    def __init__(self, readme, repo_base_path : str) -> None:
        self.readme = readme
        self.repo_base = repo_base_path

    #region Project Details
    def write_project_details(self, destination_path : str, person : str, time : str) -> None:
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
    #endregion

    #region Directory Tree
    def get_github_path(self, dir_path :str, file :str, isdir : bool = False) ->str:
        rel_path = dir_path.split("Epitech-Subjects/")[1] + "/" + file
        link = self.repo_base + ("tree" if isdir else "blob") + "/main/" + rel_path
        return link

    def write_directory_content(self, dir_path : str, identation_level : int):
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
            self.readme.write(f"[{file}]({self.get_github_path(dir_path, file, isdir=is_dir)})\n\n")
            if is_dir:
                self.write_directory_content(file_path, identation_level + 1)
    #endregion

    #region Footer
    def write_footer(self, destination_path : str):
        github_path = self.get_github_path(destination_path, "self.README.md")
        module_path = github_path[:github_path.find("/", github_path.find("/B-") + 1)]
        semester_path = github_path[:github_path.find("/", github_path.find("/Semester-") + 1)]
        semester_name = semester_path[github_path.find("/", github_path.find("/Semester-")) + 1: ]
        home_path = self.repo_base

        self.readme.write(f"[↩️ Revenir au module]({module_path})\n\n")
        self.readme.write(f"[↩️ Revenir au {semester_name}]({semester_path})\n\n")
        self.readme.write(f"[↩️ Revenir à l'accueil]({home_path})\n")

        self.write_break(1)

        footer = '---\n\n<div align="center">\n\n<a href="https://github.com/Studio-17" target="_blank"><img src="../../../assets/voc17.gif" width="40"></a>\n\n</div>'
        self.readme.write(footer)
    #endregion

    #region UnitTests
    def write_table_head(self) -> None:
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

    def write_table_end(self) -> None:
        self.readme.write('\n\t</tbody>\n</table>\n')

    def write_one_test_cat(self, test_cat : mrvn.test_category) -> None:
        self.readme.write(f"""
        <tr>
            <td rowspan="{test_cat.test_amount}">{test_cat.name}</td>
            <td rowspan="{test_cat.test_amount}" style="text-align: center;">{test_cat.test_amount}</td>
            <td>{test_cat.test_names[0]}
        </tr>
    """)
        for i in range(1, test_cat.test_amount):
            if (i > 1):
                self.readme.write('\n')
            self.readme.write(f"\t\t<tr>\n\t\t\t<td>{test_cat.test_names[i]}</td>\n\t\t</tr>")
        return 0

    def write_unit_tests(self, browser :str, url: str):
        test_cats = mrvn.get_mrvn_test(browser, url)
        if test_cats == None or len(test_cats) == 0:
            return
        self.write_table_head()
        for test_cat in test_cats:
            self.write_one_test_cat(test_cat)
        self.write_table_end()
    #endregion

    def write_break(self, amount : int):
        break_lines = '\n<br>\n\n' * amount
        self.readme.write(break_lines)