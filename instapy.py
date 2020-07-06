from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.firefox.options import Options

import time
from time import sleep

import urllib.request

browser = None
wait = None
browser_options = Options()

TIMEOUT = 20

# xpath
URL_INSTAGRAM = "https://www.instagram.com/"
XPATH_LOGIN_USERNAME = "//input[@name='username']"
XPATH_LOGIN_PASSWORD = "//input[@name='password']"
XPATH_LOGIN_SUBMIT = "//button[@type='submit']"

XPATH_LOADED = "//img[@alt='Instagram']"

XPATH_PROFILE_BOX = "//section[@class='zwlfE']"
XPATH_PROFILE_USERNAME = "//div[@class='nZSzR']/h1"
XPATH_PROFILE_USERNAME_2 = "//div[@class='nZSzR']/h2"
XPATH_PROFILE_VERIFIED = "//div[@class='nZSzR']/span"
XPATH_PROFILE_IMAGE = "//header[@class='vtbgv ']/div/div/div/button/img"
XPATH_PROFILE_IMAGE_2 = "//header[@class='vtbgv ']/div/div/span/img"
XPATH_PROFILE_POST_AMOUNT = "//ul[@class='k9GMp ']/li[1]/span/span"
XPATH_PROFILE_SUBSCRIBER_AMOUNT = "//ul[@class='k9GMp ']/li[2]/a/span"
XPATH_PROFILE_SUBSCRIBER_AMOUNT2 = "//ul[@class='k9GMp ']/li[2]/span/span"
XPATH_PROFILE_SUBSCRIBED_TO_AMOUNT = "//ul[@class='k9GMp ']/li[3]/a/span"
XPATH_PROFILE_SUBSCRIBED_TO_AMOUNT2 = "//ul[@class='k9GMp ']/li[3]/span/span"
XPATH_PROFILE_PRIVATE = "//div[@class='QlxVY']"
XPATH_PROFILE_BIO_INFO = "//div[@class='-vDIg']"
XPATH_PROFILE_SUBSCRIBED_TO_CLICK = "//ul[@class='k9GMp ']/li[3]/a"

XPATH_PROFILE_SUBSCRIBED_TO_LIST = "//div[@class='PZuss']"
XPATH_PROFILE_SUBSCRIBED_TO_LIST_ELEMENTS = "li"
XPATH_PROFILE_SUBSCRIBED_TO_LIST_ELEMENTS_NAME = "div/div[1]/div[2]/div/a"

XPATH_PROFILE_FOLLOW = "//div[@class='Y2E37']/button"


# starts the driver and logs in
def start(username, password, headless):
    global browser
    global wait
    if headless:
        browser_options.headless = True
    browser = webdriver.Firefox(options=browser_options)
    wait = WebDriverWait(browser, timeout=TIMEOUT)
    browser.get(URL_INSTAGRAM)
    wait_send_keys(XPATH_LOGIN_USERNAME, username)
    wait_send_keys(XPATH_LOGIN_PASSWORD, password)
    wait_click(XPATH_LOGIN_SUBMIT)
    wait_for_element(XPATH_LOADED)


# navigates to a user by username true if the user exists, false if not
# if the user doesnt exist it returns to the last url
def goto_user(username):
    temp_url = browser.current_url
    browser.get(URL_INSTAGRAM + username + "/")
    wait_for_element(XPATH_LOADED)
    try:
        browser.find_element_by_xpath(XPATH_PROFILE_BOX)
    except NoSuchElementException:
        browser.get(temp_url)
        return False
    return True


# returns the username of the current profile None if no user found
def get_username():
    try:
        username = browser.find_element_by_xpath(XPATH_PROFILE_USERNAME).text
    except NoSuchElementException:
        try:
            username = browser.find_element_by_xpath(XPATH_PROFILE_USERNAME_2).text
        except NoSuchElementException:
            return None
    return username


# true if the user is verified, no if not
def is_verified():
    try:
        browser.find_element_by_xpath(XPATH_PROFILE_VERIFIED).text
        return True
    except NoSuchElementException:
        return False


# waits till element is located and sends keys
def wait_send_keys(xpath, text):
    global wait
    element = wait.until(expected_conditions.presence_of_element_located((By.XPATH, xpath)))
    element.send_keys(text)


# waits till element is located and clicks it
def wait_click(xpath):
    global wait
    element = wait.until(expected_conditions.presence_of_element_located((By.XPATH, xpath)))
    element.click()


# waits till element is located and returns it
def wait_for_element(xpath):
    global wait
    return wait.until(expected_conditions.presence_of_element_located((By.XPATH, xpath)))


# downloads the profile image
def download_profile_image(output_file):
    sleep(3)
    try:
        image_url = browser.find_element_by_xpath(XPATH_PROFILE_IMAGE).get_attribute("src")
    except NoSuchElementException as ex:
        try:
            image_url = browser.find_element_by_xpath(XPATH_PROFILE_IMAGE_2).get_attribute("src")
        except NoSuchElementException as ex:
            return False

    urllib.request.urlretrieve(image_url, output_file)
    return True


# gets the post amount
def get_post_amount():
    try:
        amount = int(browser.find_element_by_xpath(XPATH_PROFILE_POST_AMOUNT).text.replace(".", "").replace(",", ""))
        return amount
    except NoSuchElementException as ex:
        return -1


# gets the post amount
def get_subscriber_amount():
    try:
        amount_str = browser.find_element_by_xpath(XPATH_PROFILE_SUBSCRIBER_AMOUNT).get_attribute("title")
        amount = int(amount_str.replace(".", "").replace(",", ""))
        return amount
    except NoSuchElementException as ex:
        try:
            amount_str = browser.find_element_by_xpath(XPATH_PROFILE_SUBSCRIBER_AMOUNT2).get_attribute("title")
            amount = int(amount_str.replace(".", "").replace(",", ""))
            return amount
        except NoSuchElementException as ex:
            return -1


# gets the subscribed to amount
def get_subscribed_to_amount():
    try:
        amount = int(browser.find_element_by_xpath(XPATH_PROFILE_SUBSCRIBED_TO_AMOUNT).text.replace(".", "").replace(",", ""))
        return amount
    except NoSuchElementException as ex:
        try:
            amount = int(browser.find_element_by_xpath(XPATH_PROFILE_SUBSCRIBED_TO_AMOUNT2).text.replace(".", "").replace(",", ""))
            return amount
        except NoSuchElementException as ex:
            return -1


# checks if private element exists
def is_profile_private():
    try:
        browser.find_element_by_xpath(XPATH_PROFILE_PRIVATE)
        return True
    except NoSuchElementException as ex:
        return False


# get bio and info
def get_profile_bio_info():
    try:
        info = browser.find_element_by_xpath(XPATH_PROFILE_BIO_INFO).text
        return info
    except NoSuchElementException:
        return ""


# returns a list of the names of the following
def get_following_list():
    username_list = []
    try:
        browser.find_element_by_xpath(XPATH_PROFILE_SUBSCRIBED_TO_CLICK).click()
        list_parent = wait_for_element(XPATH_PROFILE_SUBSCRIBED_TO_LIST)
        last_list = list_parent.find_elements_by_xpath(XPATH_PROFILE_SUBSCRIBED_TO_LIST_ELEMENTS)
        browser.execute_script("arguments[0].scrollIntoView();", last_list[-1])
        new_list = list_parent.find_elements_by_xpath(XPATH_PROFILE_SUBSCRIBED_TO_LIST_ELEMENTS)
        time_out = time.time() + TIMEOUT
        while len(new_list) == len(last_list) and time.time() < time_out:
            new_list = list_parent.find_elements_by_xpath(XPATH_PROFILE_SUBSCRIBED_TO_LIST_ELEMENTS)
        for element in new_list:
            for i in range(0, 5):
                try:
                    username = element.find_element_by_xpath(XPATH_PROFILE_SUBSCRIBED_TO_LIST_ELEMENTS_NAME).text
                    print(username)
                    if len(username) > 0 and username != " ":
                        username_list.append(username)
                    break
                except StaleElementReferenceException:
                    None
                except NoSuchElementException:
                    None
        return username_list
    except NoSuchElementException as ex:
        return username_list
    except TimeoutException:
        return username_list


def follow_profile():
    browser.find_element_by_xpath(XPATH_PROFILE_FOLLOW).click()