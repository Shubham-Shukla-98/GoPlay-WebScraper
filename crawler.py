from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import subprocess
import time

#####################################################################

# no spaces in name
name = 'Youth_Of_May'
# url of series home page or any episode on goplay streaming
url = 'https://goplay.anontpp.com/562d333537393938/r2/Youth-of-May/'
# reddit credentials
user = 'user'
passwd = 'pass'

#####################################################################

# webdriver location in same folder
chrome = "chromedriver.exe"
# launch chrome webdriver
options = webdriver.ChromeOptions()
# adding ublock origin to block ads
options.add_extension('ublock.crx')
# adding Https everywhere for better access, some sites don't work without this
options.add_extension('https.crx')
# adding tunnelbear vpn
options.add_extension('bear.crx')
# adding experimental features trying to hide selenium
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

options.add_argument('--profile-directory=Default')
options.add_argument("--disable-plugins-discovery");
options.add_argument("--start-maximized")

#open chrome with these extension loaded
driver = webdriver.Chrome(options=options, executable_path=chrome)

# open website
driver.get("https://goplay.anontpp.com/?ref=Reddit");
# open token generator site
driver.find_element_by_xpath("/html/body/center/font[2]/b/a").click();
# open reddit
driver.find_element_by_link_text('Visit the site using an automatically generated Access Token.').click();
# Fill login credentials
driver.find_element_by_xpath("""//*[@id="form"]/center/a""").click();
driver.find_element_by_id("loginUsername").send_keys(user);
driver.find_element_by_id("loginPassword").send_keys(passwd);

try:
    # submit form
    driver.find_element_by_xpath("""/html/body/div/main/div[1]/div/div[2]/form/fieldset[5]/button""").click();
    # wait for reddit to open authorization page
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.presence_of_element_located((By.XPATH, """/html/body/div[3]/div/div[2]/form/div/input[1]""")))
    # allow access
    time.sleep(5)
    element.click();
    # now main site can be accessed - move to requested series now
    driver.get(url);
except:
    print("failed in authorizing")


# fetch all episodes    
links = driver.find_elements_by_xpath("//a[@href]")
eps = []
for epi in links:
    link = epi.get_attribute("href")
    if 'Episode' in link:
        if link not in eps:
            eps.append(link)
    else:
        continue

for ep in eps:
    print(ep)
    driver.get(ep)
    title = driver.find_element_by_id('infotitle').text;
    # formatting title no spaces allowed
    title = title.replace("\n",":")
    title = title.replace(' - ','_')
    title = title.replace(' ','_')
    print("Downloading : " + title)

    links = driver.find_elements_by_xpath("//a[@href]")
    for epi in links:
        link = epi.get_attribute("href")
        if 'downloadcode' in link:
            try:
                driver.get(link)
                time.sleep(2)
                driver.find_element_by_class_name('g-recaptcha').click()
                # wait for user to pass re-captcha
                wait = WebDriverWait(driver, 200)
                code = wait.until(EC.presence_of_element_located((By.ID, "dcopy"))).get_attribute("value")
                print(code)
                cs1 = 'dc.bat '+title+' '+code;
                print(repr(cs1))
                subprocess.Popen(['cmd','/K',cs1])
                episode = episode + 1
                time.sleep(2)
            except:
                print("failed in downloading")
            break
