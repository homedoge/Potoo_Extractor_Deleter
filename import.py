from selenium import webdriver
from cryptography.fernet import Fernet
import time
import sys

file=open('key.key','rb')
key=file.read()
file.close()
cipher_suite = Fernet(key)
with open('bytes.bin', 'rb') as file_object:
    for line in file_object:
        encryptedpwd = line
uncipher_text = (cipher_suite.decrypt(encryptedpwd))
import_password = bytes(uncipher_text).decode("utf-8") #convert to string

class passwords_usernames:
    import_user=''
    import_pass = import_password
def importLogin(driver):
    driver.set_page_load_timeout(300)
    driver.get('https://import.io/login')
    driver.implicitly_wait(1)
    while True:
        try:
            usr=driver.find_element_by_id('usernameControl')
            break
        except:
            time.sleep(.2)
    usr.send_keys(passwords_usernames.import_user)
    driver.find_element_by_id('passwordControl').send_keys(passwords_usernames.import_pass)
    logins=driver.find_elements_by_tag_name('button')
    nofound=1
    for el in logins:
        try:
            if "login" in el.text.lower() or "log in" in el.text.lower():
                el.click()
                nofound=0
                break
        except:
            continue
    if nofound==1:
        print("No login Button found. Edit program")
        sys.exit()
def importDeleter(driver,IDs):
    print(IDs)
    for ID in IDs:
        url='https://app.import.io/dash/extractors/'+ID
        driver.get(url)
        while(driver.current_url==url):
            time.sleep(.5)
        if driver.current_url!=url+'/history':
            print("ID: "+ID+" DOES NOT EXIST, moving on...")
            continue
        else:
            try:
                deleteButton=driver.find_element_by_xpath('//*[@id="lightning"]/div/div/div/div[2]/section/div/section/div[2]/div/div/header/div[2]/div[2]/span[3]/button')
            except:
                print("ID "+ID+" IS DOES NOT EXIST, moving on...")
                continue
            if "delete" not in deleteButton.text.lower():
                print("PROGRAM NEEDS TO UPDATED. XPATH OF DELETE BUTTON SEEMS TO HAVE MOVED")
                break
            else:
                deleteButton.click()
                confirm=driver.find_element_by_xpath('/html/body/div[7]/div[2]/div/div/div[3]/div/button[2]')
                if 'delete' not in confirm.text:
                    print('Check program to see if xpath of "Confirm Delete" button has changed!')
                    break
                else:
                    confirm.click()
                    while (driver.current_url == url):
                        time.sleep(.5)

print("Make an excel sheet and type a column of your IDs. Copy that column and paste it here now.\nThen, press enter twice to continue!\n>> ")
IDs=[]
while True:
    IDs.append(input())
    if IDs[-1]=='':
        IDs.pop(-1)
        break
driver = webdriver.Chrome('chromedriver')
importLogin(driver)
importDeleter(driver,IDs)
driver.close()
