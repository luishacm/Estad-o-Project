#Packages to be used in the script

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
import re
import requests

#General options for the navigator

profile = webdriver.FirefoxProfile()
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
chrome_driver = os.getcwd() +"\\chromedriver.exe"
#profile.set_preference("general.useragent.override", "Mozilla/5.0 (X11;     Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0   Safari/537.36")
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
#driver = webdriver.Firefox(profile)


#making the login on the Estadão website so we can have the images in high quality

login = [line.rstrip('\n') for line in open("C:/Users/ PATH TO THE FOLDER /arquivos/login.txt")] #You need to create a folder called "arquivos" and one called "Imagens"
username = login[0]
password = login[1]
driver.get("https://acesso.estadao.com.br/login")
driver.find_element_by_xpath('//input[@name="emaillog"]').send_keys(username)
driver.find_element_by_xpath('//input[@name="passwordlog"]').send_keys(password)
driver.find_element_by_xpath('//input[@value="Entrar"]').click()
print("Fez login!")
 
#Opening the web navigator, opening the document where the links of the images will be stored
# and creating a function so it can be activated with the right variables

m = 0

def block ():
    search = [line.rstrip('\n') for line in open("C:/Users/ PATH TO THE FOLDER /arquivos/pesquisas.txt")]
    txt = open("C:/Users/ PATH TO THE FOLDER /arquivos/linkdasimagens.txt","w")
    driver.get(search[m])
    time.sleep(3)

    #Finding out how many pages there is in the website search page

    if driver.find_elements_by_class_name("page-ultima-qtd"):
        try:
            page_number = driver.find_element_by_class_name("page-ultima-qtd").text
        except NoSuchElementException:
            pass
    else:
        page_number = 1

    if driver.find_elements_by_xpath("//label[contains(text(),'Veja o jornal do dia:')]") != None:
        try:
            driver.find_element_by_xpath("//label[contains(text(),'Veja o jornal do dia:')]").click
        except NoSuchElementException:
            pass
    print("Pop-up foi fechado")
    time.sleep(10)

    #This will store all the selected links of the images from the website in a TXT so later we can download the images.

    for i in range(int(page_number)):
        try:
            links = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.LINK_TEXT, "LEIA ESTA EDIÇÃO")))
            references = [link.get_attribute("href") for link in links]    
            time.sleep(1)              
            txt.write("\n".join(references))
            print("\n".join(references))
            txt.write("\n")        
            driver.find_element_by_class_name("seta-right").click()            
        except NoSuchElementException:
            pass
        
    print("Links foram Adquiridos")    
    txt.close()

    #This is the second block of the code: after we got all the links, we will download them now.
    ##Preparing the variables

    time.sleep(1) 
    lines = [line.rstrip('\n') for line in open("C:/Users/ PATH TO THE FOLDER /arquivos/linkdasimagens.txt")]
    x = 0
    with open('C:/Users/ PATH TO THE FOLDER /arquivos/linkdasimagens.txt') as f:
        line_count = 0
        for line in f:
            line_count += 1

    ##It will get the list of links we made and open in the navigator one by one and download each image.
    ##Each downloaded image will be placed in a path of the computer to be determined by the user.
    ##We inserted the Google website to loop too because the Javascript of the site stops the script, this fix the problem partially. 

    for i in range(int(line_count)):
        try:        
            y = lines[x]
            driver.get('http://www.google.com')
            driver.get(y)        
            img = driver.find_element_by_xpath("//img[@class='BRnoselect']")
            src = img.get_attribute('src')
            title = driver.find_element_by_xpath("//h1[@class='edicao-data']").text
            u = re.sub('[^A-Za-z0-9]+', '', title)
            u = u[:-4]
            z = u[-4:]
            with open(("C:/Users/ PATH TO THE FOLDER Imagens/{}/{}.jpg".format(z, u)), "wb") as f:   #you need to create several folders inside the path with the years that you are downloading the images from (2010, 2011, 2012).
                f.write(requests.get(src).content)
            x += 1
            print(x)            
        except NoSuchElementException:
            pass

#Running the code according to the variables we want to change. Choose to loop for the amount of search links you decided to put in your txt called (pesquisas.txt).
#In the example bellow it will loop 3 times, then loop for more 4x7 (28 times), in a total of 31 times. That can be changed for the amount of links you want.

block()
        
for i in range(3):
    try:
        block()
        m+=1
    except:
        print(("Bloco de {} deu erro").format(z))
        pass
    
for b in range(7):
    for n in range(4):
        try:
            block()
            m+=1
        except:
             print(("Bloco de {} deu erro").format(z))
             pass
