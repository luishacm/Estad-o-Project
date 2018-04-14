from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import urllib.request
import re
import requests


#General options for the navigator

profile = webdriver.FirefoxProfile()
profile.set_preference("general.useragent.override", "Mozilla/5.0 (X11;     Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0   Safari/537.36")
driver = webdriver.Firefox(profile)


#making the login at the Estadão website so we can have tha images in high quality

login = [line.rstrip('\n') for line in open("C:/User/PATH TO THE TXT WITH THE LOGIN AND PASSWORD IN EACH LINE/login.txt")]
username = login[0]
password = login[1]
driver.get("https://acesso.estadao.com.br/login")
driver.find_element_by_xpath('//input[@name="emaillog"]').send_keys(username)
driver.find_element_by_xpath('//input[@name="passwordlog"]').send_keys(password)
driver.find_element_by_xpath('//input[@value="Entrar"]').click()
 
#Opening the web navigator and the document where the links of the images will be stored

x = 1
txt = open("C:/User/PATH TO ANY EMPTY TXT /linkdasimagens.txt","w")
driver.get("http://acervo.estadao.com.br/procura/#!/mec/Acervo//spo/1/2010/2010//Primeira") #example of search link of the website
time.sleep(5)

#Finding out how many pages there is in the website

page_number = driver.find_element_by_class_name("page-ultima-qtd").text

#This will get all the selected links of the images from the website so later we can download the images.
#This is a loop. It repeats itself a amount of time, in this case, at the amount of pages there in the search.

for i in range(int(page_number)):
    try:
        links = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.LINK_TEXT, "LEIA ESTA EDIÇÃO")))
        references = [link.get_attribute("href") for link in links]    
        time.sleep(1)              
        x+=1
        txt.write("\n".join(references))
        print("\n".join(references))
        txt.write("\n")        
        driver.find_element_by_class_name("seta-right").click()
        
    except NoSuchElementException:
        pass
    
txt.close()


#This is the second block of the code: after getting all the links of the images we want to download, we will proceed to it.

##Preparing the variables

time.sleep(1) 
lines = [line.rstrip('\n') for line in open("C:/User/ PATH OF THE EMPTY TXT /linkdasimagens.txt")]
x = 0

##Another loop, now with another function. It will get the list of links we made and open in the navigator one by one and download each image.
##Each downloaded image will be placed in a path of the computer to be determined by the user.

while True:
    try:        
        y = lines[x]
        driver.get('http://www.google.com')
        driver.get(y)        
        u = re.sub('[^A-Za-z0-9]+', '', y)
        u = u[:-20]
        img = driver.find_element_by_xpath("//img[@class='BRnoselect']")
        src = img.get_attribute('src')
        with open(("C:/Users/PATH WHERE YOU WANNA SAVE YOUR IMAGES/{}.jpg".format(u)), "wb") as f:
            f.write(requests.get(src).content)
        x += 1
        y=''
        print(x)
        
    except NoSuchElementException:
        pass
