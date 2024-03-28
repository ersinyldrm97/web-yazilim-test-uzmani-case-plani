from selenium import webdriver
from constants import global_constants
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from constants import global_constants
from secret import secret_information

class Base_Test:
    def __init__(self):
      self.driver = webdriver.Chrome(ChromeDriverManager().install())
      self.driver.maximize_window()
      self.driver.get(global_constants.URL)

class Login(Base_Test):
  def login(self):
    # Anasayfadaki giriş butonuna basma
    button = WebDriverWait(self.driver, 10).until(
      EC.presence_of_element_located((By.XPATH, f'{global_constants.LOGIN_BUTTON_FROM_HOMEPAGE}'))
    )
    button.click()
    
    # Email input alanı
    email_input = WebDriverWait(self.driver, 10).until (
      EC.element_to_be_clickable((By.NAME, 'login'))
    )
    
    # Password input alanı
    password_input = WebDriverWait(self.driver, 10).until (
      EC.element_to_be_clickable((By.NAME, 'password'))
    )
    
    # Recaptchayi görünür yapma
    recaptcha_frame = WebDriverWait(self.driver, 10).until(
      EC.presence_of_element_located((By.XPATH, f'{global_constants.FRAME_XPATH}'))
    )
    self.driver.switch_to.frame(recaptcha_frame)
    
    recaptcha_body = WebDriverWait(self.driver, 10).until(
      EC.presence_of_element_located((By.XPATH, f'{global_constants.CHECBOX_CONTAINER}'))
      )
    
    WebDriverWait(self.driver, 10).until(
      EC.element_to_be_clickable((By.XPATH, '//span[@aria-checked="false"]'))
      )
    
    recaptcha_body.click()
    self.driver.switch_to.default_content()
    
    
    login_button = WebDriverWait(self.driver, 10).until(
      EC.element_to_be_clickable((By.ID, f'{global_constants.LOGIN_BUTTON}'))
    )
    
    # Email girişi
    email_input.clear()
    email_input.send_keys(secret_information.email)
    
    # Password girişi
    password_input.clear()
    password_input.send_keys(secret_information.password)
    
    # 8 saniyelik bekleyiş recaptcha resim çıkarırsa manuel olarak resimlere tıklama
    sleep(8)
    login_button.click()
    
    information_close_button = WebDriverWait(self.driver, 10).until(
      EC.element_to_be_clickable((By.XPATH, f'{global_constants.CLOSE_BUTTON_AFTER_LOGIN_FROM_DASHBOARD}'))
      )
    information_close_button.click()
  
  def click_visit_profile(self):
    # Profile giriş yapmak için İsim ve Soyisim kısaltmasına tıklama
    button = WebDriverWait(self.driver, 10).until(
      EC.element_to_be_clickable((By.ID, f'{global_constants.PROFILE_BUTTON}'))
    )
    button.click()
    
    # Profilim seçeneğine tıklama
    click_on_profile_button = WebDriverWait(self.driver, 10).until(
      EC.element_to_be_clickable((By.XPATH, f'{global_constants.VISIT_PROFILE_BUTTON}'))
    )
    click_on_profile_button.click()

  def change_hometown(self):
    input = WebDriverWait(self.driver, 10).until(
      EC.element_to_be_clickable((By.ID, f'{global_constants.HOMETOWN_ID}'))
    )
    
    input.clear()
    input.send_keys(f'{global_constants.HOMETOWN}')
  
  def change_birthday_place(self):
    input = WebDriverWait(self.driver, 10).until(
      EC.element_to_be_clickable((By.ID, f'{global_constants.BIRTHDAY_PLACE_ID}'))
    )
    
    input.clear()
    input.send_keys(f'{global_constants.BIRTHDAY_PLACE}')
    
  def military_status(self):
    # Askerlik Durum listesini gösterme
    select = WebDriverWait(self.driver, 10).until(
      EC.element_to_be_clickable((By.ID, global_constants.MILITARY_STATUS_ID))
    )
    select.click()
    
    # Askerlik durumuna tıklama
    option = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//li[text()='{global_constants.MILITARY_STATUS}']"))
    )
    
    print(option.text)
    option.click()
    sleep(1)
    
    save_button = WebDriverWait(self.driver, 10).until(
      EC.element_to_be_clickable((By.ID, global_constants.SAVE_BUTTON))
    )
    
    
    if select.text == 'Tecilli':
      self.select_postponement_date(global_constants.MILITARY_POSTPONEMENT_YEAR, global_constants.MILITARY_POSTPONEMENT_MONTH, global_constants.MILITARY_POSTPONEMENT_DAY)
      save_button.click()
      
    if select.text == "Muaf":
      input = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.ID, global_constants.MILITARY_STATUS_EXPLANATION))
      )
      input.clear()
      input.send_keys(global_constants.EXPLANATION)
      save_button.click()
      
    else:
      save_button.click()
      
  def select_postponement_date(self, year, month, day):
     # Takvimi açmak için takvim elementine tıklama
    select_calendar = WebDriverWait(self.driver,10).until(
      EC.element_to_be_clickable((By.ID, global_constants.MILITARY_POSTPONEMENT_DATE_ID))
     )
    select_calendar.click()
    
    sleep(1)
    # Yıl girme  
    year_input = WebDriverWait(self.driver, 10).until(
      EC.element_to_be_clickable((By.CLASS_NAME, "cur-year"))
    )
    year_input.clear()
    year_input.send_keys(year)
    sleep(0.5)
    
    # Ay seçimini bulma ve ayı seçme
    month_option = WebDriverWait(self.driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '.flatpickr-monthDropdown-months'))
    )
    
    month_option.click()
#     
    # # Belirtilen ayı seçme
    month_option = WebDriverWait(self.driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, f"//option[text()='{month}']"))
    )
    month_option.click()

    sleep(0.5)
    # Gün seçimini bulma ve günü seçme
    day_container = WebDriverWait(self.driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'dayContainer'))
    )
    
    sleep(0.5)
    day_to_select = day_container.find_element(By.XPATH, f".//span[text()='{day}']")
    day_to_select.click()
  
      
test = Login()
test.login()
test.click_visit_profile()
test.change_hometown()
test.change_birthday_place()
test.military_status()
