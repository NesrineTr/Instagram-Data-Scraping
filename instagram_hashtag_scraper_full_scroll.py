from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configurer Selenium avec ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Se connecter à Instagram
def login(username, password):
    driver.get('https://www.instagram.com/accounts/login/')
    time.sleep(3)
    
    # Remplir le nom d'utilisateur et le mot de passe
    driver.find_element(By.NAME, 'username').send_keys(username)
    driver.find_element(By.NAME, 'password').send_keys(password)
    
    # Soumettre le formulaire
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    time.sleep(5)  # Attendre que la page se charge

# Entrée des identifiants de connexion
username = input("Entrez votre nom d'utilisateur Instagram : ")
password = input("Entrez votre mot de passe Instagram : ")
login(username, password)

# Entrée de l'utilisateur pour le hashtag
hashtag = input("Entrez le hashtag (sans le #) : ")

# Accéder à la page du hashtag sur Instagram
url = f'https://www.instagram.com/explore/tags/{hashtag}/'
driver.get(url)
time.sleep(5)  # Attendre que la page se charge

# Scroller la page plusieurs fois pour charger plus de publications
scroll_pause_time = 2
scrolls = 1000  # Nombre de fois à scroller
for _ in range(scrolls):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause_time)

# Récupérer les liens vers les publications
post_links = []
usernames = set()

try:
    # Attendre que les publications soient visibles
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, 'a'))
    )
    
    # Récupérer tous les liens dans la page
    links = driver.find_elements(By.TAG_NAME, 'a')
    for link in links:
        post_url = link.get_attribute('href')
        if post_url and '/p/' in post_url and post_url not in post_links:
            post_links.append(post_url)

    # Afficher les liens de publications trouvés pour débogage
    print("Liens de publications trouvés :")
    for post_link in post_links:
        print(post_link)

    # Visiter chaque publication rapidement pour récupérer le profil de l'utilisateur
    for post_link in post_links:
        driver.get(post_link)
        time.sleep(1)  # Délai réduit pour charger la page

        try:
            # Attendre que le nom d'utilisateur soit présent et récupérer le nom
            username_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'a._a6hd'))  # Mettez à jour le sélecteur ici
            )
            username = username_element.text
            usernames.add(username)
        except Exception as e:
            print(f"Erreur lors de la récupération du nom d'utilisateur : {e}")

finally:
    # Afficher les noms d'utilisateurs récupérés
    print("Les comptes ayant publié avec ce hashtag sont :")
    for username in usernames:
        print(username)

    # Fermer le driver
    driver.quit()
