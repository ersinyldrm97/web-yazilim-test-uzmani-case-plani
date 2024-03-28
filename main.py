from selenium import webdriver
from constants import global_constants
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from constants import global_constants

class Base_Test:
    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.maximize_window()
        self.driver.get(global_constants.URL)
        
        self.languages = {
            "en": "EN",
            "tr": "TR",
        }
        
class Click_Navbar(Base_Test):
    def navbar_elements(self):
      # navbar elementlerini bulma 
      navbar_elements = WebDriverWait(self.driver, 10).until(
          EC.presence_of_all_elements_located((By.XPATH, f'{global_constants.NAVBAR_ELEMENTS}'))
      )
      
      # navbar uzunluğunu alıp hepsini tek tek kontrol edip tıklama.
      for i in range(len(navbar_elements)):
        navbar_elements[i].click()
        print("Successfully clicked on:", navbar_elements[i].text)

        # Açılan navbarlarda sayfanın tamamen gelmesi için bekleme
        WebDriverWait(self.driver, 10).until(
          EC.visibility_of_element_located((By.TAG_NAME, "body")))
          
class Change_Language_And_Verify(Base_Test):
    def switch_language(self, language_code):
      
      if language_code in self.languages:
        # Dil değiştirme butonunu bulma
        language_selector = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f'{global_constants.LANGUAGE_CHANGE_BUTTON}')))
        
        language_selector.click()
        
        print(f"Successfully changed language to: {self.languages[language_code]}")
        sleep(2)  # Dil değişimi için bekleme
      else:
        print(f"Language {language_code} is not supported")

    def verify_language(self, expected_language):
      
      language_selector = WebDriverWait(self.driver, 10).until(
          EC.presence_of_element_located((By.XPATH, f'{global_constants.LANGUAGE_CHANGE_BUTTON}')))
      
      current_language = language_selector.get_attribute("a")
      
      if current_language:
        actual_language = self.languages.get(current_language)
        if actual_language:
            assert actual_language == expected_language, f"Language mismatch. Expected: {expected_language}, Actual: {actual_language}"
            print(f"Current language is: {actual_language}")
        else:
          print(f"Language '{current_language}' is not supported")
    
    def language_switch(self):
      for language_code, language_name in self.languages.items():
          self.switch_language(language_code)
          
          language = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f'{global_constants.FIRST_NAVBAR_ELEMENT_FOR_COMPARE_LANGUAGE}'))
            )
          
          language_txt = language.text  
          print('show a word as an example', language_txt)
          sleep(3)
          self.verify_language(language_name)

class Filter_Positions_And_Units(Base_Test):
    def filter_positions(self, unit, position):
      self.driver.get(global_constants.POSITIONS_URL)
      
      # Birim ve pozisyonları filtreleme
      unit_filter = WebDriverWait(self.driver, 10).until(
          EC.element_to_be_clickable((By.XPATH, f'{global_constants.INPUT_UNIT_SEARCH}'))
      )
      unit_filter.clear()
      unit_filter.send_keys(unit)
      click_filter = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f'{global_constants.FILTER_UNIT_NAME}'))
        )
      click_filter.click()
      
      position_filter = WebDriverWait(self.driver, 10).until(
          EC.element_to_be_clickable((By.XPATH, f'{global_constants.INPUT_POSITION_NAME}'))
      )
      position_filter.clear()
      position_filter.send_keys(position)

      # Filtreleme sonuçlarını kontrol etme
      positions = WebDriverWait(self.driver, 10).until(
          EC.presence_of_all_elements_located((By.XPATH, f'{global_constants.FILTER_POSITION_NAME}'))
      )
      for pos in positions:
          if position.lower() in pos.text.lower():
              print(f"Position '{position}' found in the filtered results.")
              return True
      print(f"Position '{position}' not found in the filtered results.")
      return False
    
    def career_automation(self):
      unit = f"{global_constants.UNIT_NAME}"
      position = f"{global_constants.POSITION_NAME}"
      
      result = self.filter_positions(unit, position)
      
      assert result, "Test failed!"
      print("Test Passed!")


    
test_click = Click_Navbar()
test_click.navbar_elements()

test = Change_Language_And_Verify()
test.language_switch()

test = Filter_Positions_And_Units()
test.career_automation()
