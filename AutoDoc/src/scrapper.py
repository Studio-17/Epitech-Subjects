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
class scrapper:
    def __init__(self, browser :str = "e", destination_url :str = None) -> None:
        if destination_url == None:
            raise ValueError("Invalid url passed use -h for help")
        match browser:
            case "e":
                self.driver = webdriver.Edge()
            case "f":
                self.driver = webdriver.Firefox()
            case "c":
                self.driver = webdriver.Chrome()
        self.destination_url = destination_url

    def scrape(self):
        self._search()
        self._login()
        content = self._get_desired_content()
        self._quit_driver()
        return self._parse_content(content)

    def _login(self):
        """
            Overrided by other scrapper
        """
        raise NotImplementedError()

    def _check_driver(self):
        if (self.driver == None):
            raise ValueError("Invalid driver")

    def _parse_content(self, content):
        """
            Overrided by other scrapper
        """
        raise NotImplementedError()

    def _get_desired_content(self):
        """
            Overrided by other scrapper
        """
        raise NotImplementedError()

    def _search(self):
        self._check_driver()
        self.driver.get(self.destination_url)

    def _quit_driver(self):
        time.sleep(3)
        self.driver.quit()
        self.driver = None

class mrvn_scrapper(scrapper):
    def __init__(self, browser :str = "e", destination_url :str = None) -> None:
        if destination_url == None or destination_url.find(BASE_MRVN_URL) == -1:
            raise ValueError("Invalid url passed use -h for help")
        super().__init__(browser, destination_url)

    def _login(self):
        self._check_driver()
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

    def _get_desired_content(self) -> list[list[str]]:
        test_cells = self.driver.find_elements(By.CSS_SELECTOR, ".skill-cell.mdl-grid")
        test_content = [cell.text.split("\n") for cell in test_cells]
        return test_content
    
    def _parse_content(self, content):
        tests = []
        for category in content:
            tests.append(test_category(category[0], (int)(category[3].split(": ")[1]), category[7:]))
        return tests
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

def get_mrvn_test(browser :str, url :str):
    scrapper = mrvn_scrapper(browser=browser, destination_url=url)
    return scrapper.scrape()