from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common import exceptions as Excep
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

browserDriver = Service("D:\local-repoes\python-workspace\hackeru-scrapper\geckodriver.exe")
browserOptions=Options()
browserOptions.headless = False 
browserOptions.add_argument("--start-maximized")
browserOptions.add_argument("--kiosk")
browser = webdriver.Firefox(service=browserDriver,options=browserOptions)
browser.get("https://www.hackampus.com/sign")
print("[PROCCESS STARTED]")

#USER CREDENTIALS

#email = input("ENTER YOUR EMAIL: ")
#password = input("ENTER YOUR PASSWORD: ")
email = ""
password = ""
#path = input("ENTER SAVE DIRECTORY (full path): ")

#AUTHENTICATION

#WebDriverWait(browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"div.mt-4:nth-child(2)")))
browser.find_element(By.CSS_SELECTOR,'div.mt-4:nth-child(2)').click()
browser.find_element(By.CSS_SELECTOR, '#language > option:nth-child(2)').click()
browser.find_element(By.CSS_SELECTOR,"#login-form > div:nth-child(1) > input:nth-child(2)").send_keys(email)
browser.find_element(By.CSS_SELECTOR,"div.form-group:nth-child(2) > input:nth-child(2)").send_keys(password)
browser.find_element(By.CSS_SELECTOR,"div.d-flex:nth-child(5) > button:nth-child(1)").click()
print("[LOGGED IN]")

#BOOKS

print("[SETTING UP DIRECTORIES AND LINKS]")
WebDriverWait(browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,".main-menu > div:nth-child(1) > ul:nth-child(1) > li:nth-child(3)")))
browser.find_element(By.CSS_SELECTOR,".main-menu > div:nth-child(1) > ul:nth-child(1) > li:nth-child(3)").click()
books = []
flag = True
cnt=1
while(flag):
    try:
        name = browser.find_element(By.CSS_SELECTOR,f".sub-menu > div:nth-child(1) > ul:nth-child(1) > li:nth-child({cnt}) > a:nth-child(1)").get_attribute('innerHTML')
        link = browser.find_element(By.CSS_SELECTOR,f".sub-menu > div:nth-child(1) > ul:nth-child(1) > li:nth-child({cnt}) > a:nth-child(1)").get_attribute('href')
        books.append([name,link])
        cnt+=1
    except Excep.NoSuchElementException:
        flag=False
print("[BOOKS NAMES COLLECTED]")


#CHAPTERS + SUBCHAPTERS

for book in books:

    browser.get(book[1])
    flag=True
    chapCnt=1

    print(f"[{book[0]}]")
    while(flag):
        try:
            chapter=browser.find_element(By.CSS_SELECTOR,f".sub-menu > div:nth-child(1) > ul:nth-child(1) > li:nth-child({chapCnt}) > a:nth-child(1) > span:nth-child(2)")
            print(chapter.get_attribute('innerHTML').replace("&nbsp;"," ").replace("amp;",""))
            WebDriverWait(browser,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,f".sub-menu > div:nth-child(1) > ul:nth-child(1) > li:nth-child({chapCnt}) > a:nth-child(1)"))).click()
            #The driver wont collect the element, because it is not on the screen
            #In this case it's like that because after opening chapters, the rest of the chapters
            #goes down
            chapCnt+=1
        except EC.NoSuchElementException:
            flag=False
            chapCnt=1
    sleep(2)

browser.close()
print("[FINISHED]")