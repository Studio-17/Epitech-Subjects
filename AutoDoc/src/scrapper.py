from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from sys import argv

EPI_DOMAIN_NAME = "@epitech.eu" 
BASE_MRVN_URL = "https://my.epitech.eu"
BASE_INTRA_URL = "https://intra.epitech.eu"
BASE_MICROSOFT_LOGIN_URL = "https://login.microsoftonline.com"

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
                self.driver = webdriver.ChromiumEdge()
        self.destination_url = destination_url

    def _click_button(self, by : By, value :str, max_iteration :int = 10):
        iteration = 0
        clicked = False
        while(iteration < max_iteration and clicked == False):
            iteration += 1
            try:
                button = self.driver.find_element(by, value)
                button.click()
                clicked = True
            except:
                time.sleep(0.5)
        if clicked == False:
            exit(1)

    def _get_content(self, by : By, value :str, max_iteration :int = 10) -> str:
        iteration = 0
        clicked = False
        while(iteration < max_iteration and clicked == False):
            iteration += 1
            try:
                button = self.driver.find_element(by, value)
                return button.text
            except:
                time.sleep(0.5)
        exit(1)
        
    def _check_url(self, destination_url: str):
        iteration = 0
        # Vérification du changement de page
        while (self.driver.current_url.find(destination_url) == -1 and iteration < 20):
            time.sleep(0.5)
            iteration += 1
        if (self.driver.current_url.find(destination_url) == -1):
            exit(1)

    def scrape(self):
        self._search()
        self._login()
        time.sleep(1)
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
    
    def _select_epi_account(self, base_url : str):
        # On attends d'être sur la page de login
        self._check_url(BASE_MICROSOFT_LOGIN_URL)
        iteration = 0
        clicked = False

        # Récupération du bouton une fois la page chargée
        while (clicked == False and iteration < 20):
            iteration += 1
            try:
                # Récupération de tout les comptes microsoft enregistré
                all_accounts = self.driver.find_elements(By.CSS_SELECTOR, ".table")
                valid_account = next((x for x in all_accounts if x.accessible_name.find(EPI_DOMAIN_NAME) != -1), None)
                if (valid_account == None):
                    time.sleep(0.5)
                    continue
                valid_account.click()
                clicked = True
            except:
                time.sleep(0.5)
        if (clicked == False):
            exit(1)

        # Vérification du retour à l'url de base
        self._check_url(base_url)

    def _search(self):
        self._check_driver()
        self.driver.get(self.destination_url)

    def _quit_driver(self):
        time.sleep(3)
        self.driver.quit()
        self.driver = None
#endregion

#region Marvin Scrapper
class mrvn_scrapper(scrapper):
    def __init__(self, browser :str = "e", destination_url :str = None) -> None:
        if destination_url == None or destination_url.find(BASE_MRVN_URL) == -1:
            raise ValueError("Invalid url passed use -h for help")
        super().__init__(browser, destination_url)

    def _login(self):
        self._check_driver()
        self._click_button(By.XPATH, "/html/body/div/div/a")
        # Vérification de la page actuelle
        self._select_epi_account(BASE_MRVN_URL)

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

#region Intra Scrapper
class intra_scraped(scrapper):
    def __init__(self, browser: str = "e", destination_url: str = None) -> None:
        if destination_url == None or destination_url.find(BASE_INTRA_URL) == -1:
            raise ValueError("Invalid url passed use -h for help")
        super().__init__(browser, destination_url)

    def _login(self):
        self._check_driver()
        self._click_button(By.CSS_SELECTOR, ".login-student", max_iteration=20) # Longer because of DDOS security
        self._select_epi_account(BASE_INTRA_URL)
    
    def _get_desired_content(self):
        details = self._get_content(By.CSS_SELECTOR, ".item.title")
        self._click_button(By.CSS_SELECTOR, ".button.hide.module")
        time.sleep(0.5)
        description = self._get_content(By.CSS_SELECTOR, ".item.desc")
        competences = self._get_content(By.CSS_SELECTOR, ".item.competences")
        return [details, description, competences]
    
    def _parse_content(self, content):
        module = module_intra(content[0])
        #TODO Voir pour faire de la traduction avec googletrans
        module.description = content[1]
        module.competences = content[2]
        return module
#endregion

#region Intra module
class module_intra:
    def __init__(self, module_details :str) -> None:
        splitted = module_details.split(' (')
        self.name = splitted[0]
        self.shortname = splitted[1].split(')')[0]
        self.instace = splitted[2].split(')')[0]
        self.credits = splitted[3].split(')')[0]
        self.description = ""
        self.competences = ""
#endregion

def get_mrvn_test(browser :str, url :str):
    scrapper = mrvn_scrapper(browser=browser, destination_url=url)
    return scrapper.scrape()

def get_module_details(browser :str, url :str):
    scrapper = intra_scraped(browser=browser, destination_url=url)
    return scrapper.scrape()
