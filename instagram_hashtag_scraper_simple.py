from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def login(username, password):
    driver.get('https://www.instagram.com/accounts/login/')
    time.sleep(3)
    
    driver.find_element(By.NAME, 'username').send_keys(username)
    driver.find_element(By.NAME, 'password').send_keys(password)
    
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    time.sleep(5)  

username = input("Entrez votre nom d'utilisateur Instagram : ")
password = input("Entrez votre mot de passe Instagram : ")
login(username, password)

hashtag = input("Entrez le hashtag (sans le #) : ")

url = f'https://www.instagram.com/explore/tags/{hashtag}/'
driver.get(url)
time.sleep(5)

scroll_pause_time = 2
for _ in range(3):  
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause_time)

post_links = []
links = driver.find_elements(By.TAG_NAME, 'a')
for link in links:
    post_url = link.get_attribute('href')
    if post_url and '/p/' in post_url:
        post_links.append(post_url)

print("Liens de publications trouvés :")
for post_link in post_links:
    print(post_link)

usernames = set()
for post_link in post_links:
    driver.get(post_link)
    time.sleep(2)  
    
    try:
        username_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a._a6hd')) 
        )
        username = username_element.text
        usernames.add(username)
    except Exception as e:
        print(f"Erreur lors de la récupération du nom d'utilisateur : {e}")

print("Les comptes ayant publié avec ce hashtag sont :")
for username in usernames:
    print(username)

driver.quit()

