from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from sys import argv
import param

EPI_DOMAIN_NAME = "@epitech.eu" 
BASE_MRVN_URL = "https://my.epitech.eu"
# Dictionnaire des flags avec un id dans les resultat
VALID_FLAGS = {"-h" : -1, "-b" : 0, '-url' : 1}

#region Scrapper Definition
class mrvn_scrapper:
    def __init__(self, browser : str = "e", destination_url :str = None) -> None:
        if destination_url == None or destination_url.find(BASE_MRVN_URL) == -1:
            raise ValueError("Invalid url passed use -h for help")
        match browser:
            case "e":
                self.driver = webdriver.Edge()
            case "f":
                self.driver = webdriver.Firefox()
            case "c":
                self.driver = webdriver.Chrome()
        self.destination_url = destination_url

    def check_driver(self):
        if (self.driver == None):
            raise ValueError("Invalid driver")

    def search(self):
        if (self.driver != None):
            self.driver.get(self.destination_url)

    def login(self):
        self.check_driver()
        try:
            # Récupération du bouton de login de la page
            login_button = self.driver.find_element(By.XPATH, "/html/body/div/div/a")
            login_button.click()
        except:
            pass
        time.sleep(3)
        # Vérification de la page actuelle
        if (self.driver.current_url.find(BASE_MRVN_URL) == -1):
            try:
                # Récupération de tout les comptes microsoft enregistré
                all_accounts = self.driver.find_elements(By.CSS_SELECTOR, ".table")
                valid_account = next((x for x in all_accounts if x.accessible_name.find(EPI_DOMAIN_NAME) != -1), None)
                if (valid_account == None):
                    exit(1)
                valid_account.click()
            except:
                exit(1)
        time.sleep(3)
        # Vérification de la page actuelle
        if (self.driver.current_url.find(BASE_MRVN_URL) == -1):
            exit(1)

    def get_tests_content(self) -> list[list[str]]:
        test_cells = self.driver.find_elements(By.CSS_SELECTOR, ".skill-cell.mdl-grid")
        test_content = [cell.text.split("\n") for cell in test_cells]
        return test_content
    
    def quit_driver(self):
        time.sleep(3)
        self.driver.quit()
        self.driver = None
#endregion
        
#region Test_Category Definition
class test_category:
    def __init__(self, name :str, amount :int, rest :list[str]) -> None:
        self.name = name
        self.test_amount = amount
        self.rest = rest
        self.test_names = []
        if (self.rest != None):
            self.parse_test()
    
    def parse_test(self) -> None:
        arrow_id = [i for i in range(len(self.rest)) if self.rest[i] == 'keyboard_arrow_right']
        self.test_names = [self.rest[i] for i in range(len(self.rest)) if (i + 1) in arrow_id]
#endregion

#region Parser Definition
class parser:
    def __init__(self, test_content : list[list[str]]) -> None:
        self.content = test_content
        self.test = []

    def parse(self):
        for category in self.content:
            self.test.append(test_category(category[0], (int)(category[3].split(": ")[1]), category[7:]))

#endregion

def get_mrvn_test(browser : str, url : str):
    scrapper = mrvn_scrapper(browser=browser, destination_url=url)
    scrapper.search()
    scrapper.login()
    test_content = scrapper.get_tests_content()
    scrapper.quit_driver()
    content_parser = parser(test_content)
    content_parser.parse()
    return content_parser.test