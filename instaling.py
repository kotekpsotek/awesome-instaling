import os
import re
import time
import random
import googletrans
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

webdriver_path = os.path.abspath("webdriver_path/chromedriver.exe")
browser = webdriver.Chrome(executable_path=webdriver_path)

def put_keys_as_a_user(string: str, in_element): # imitate user in putting letters inside <textarea></textarea>'s and <input>
    for letter in string:
        in_element.send_keys(letter)
        sleep_time = random.uniform(0.180, 0.700) # genereate random float number
        time.sleep(sleep_time)

def translate_word(word: str): # this function translate word from parameter to english (default) and return translated word from her body
    translator_machine = googletrans.Translator()
    translator_word_lang_detect = translator_machine.detect(word).lang
    translated_word = translator_machine.translate(word, dest="en", src=translator_word_lang_detect) # get the translated word text
    
    return translated_word


def start_new_session():
    start_session_button = browser.find_element(By.XPATH, '//*[@id="student_panel"]/p[1]/a')
    if start_session_button.is_displayed(): # when start session button is displayed
        start_session_button.click() # button "Zacznij codzienną sesję/dokończ sesję"
        if browser.current_url.__contains__("https://instaling.pl/ling2/html_app/app.php"):
            # Start/Continue started session (only one page can be displayed in one time)
            start_session_page = browser.find_element(By.ID, "start_session_page")
            start_repeat_page = browser.find_element(By.ID, "start_repeat_page")
            continue_session_page = browser.find_element(By.ID, "continue_session_page")

            button: WebElement
            if start_session_page.is_displayed():
                button = start_session_page.find_element(By.CLASS_NAME, "big_button")
            elif start_repeat_page.is_displayed():
                button = start_repeat_page.find_element(By.CLASS_NAME, "big_button")
            else:
                button = continue_session_page.find_element(By.CLASS_NAME, "big_button")
            button.click()

            #### Session words TODO: !!!!
            learning_page = browser.find_element(By.ID, "learning_page")
            # Section with question and word/words to translate
            learning_page_question_usage_example_text: str = learning_page.find_element(By.XPATH, "//div[@id=\"question\"]/div[@class=\"usage_example\"]").text # question text
            learning_page_question_caption_translations_text: str = learning_page.find_element(By.XPATH, "//div[@id=\"question\"]/div[@class=\"caption\"]/div[@class=\"translations\"]").text # word which should be translated
            # Section with input for answer and submit button
            learning_page_learning_form_check_input: WebElement = learning_page.find_element(By.XPATH, "//div[@class=\"learning_form\"]/table//input[@id=\"answer\"]") # Input Element for the answer
            learning_page_learning_form_check_button: WebElement = learning_page.find_element(By.XPATH, "//div[@class=\"learning_form\"]/div[@id=\"check\"]") # Button to submit translation
            
            # Converted word to translation (the result is the single word)
            word_to_translate: str
            if learning_page_question_caption_translations_text.__contains__(","):
                word_to_translate = learning_page_question_caption_translations_text.split(",")[0].strip()
            elif learning_page_question_caption_translations_text.__contains__(";"):
                word_to_translate = learning_page_question_caption_translations_text.split(";")[0].strip()
            else:
                word_to_translate = learning_page_question_caption_translations_text.strip()

            translated_word = translate_word(word_to_translate)
            # TODO: code must working for multiple words translations so top code should be in infinity loop (while is in python the best for that)
        else:
            print("Something wents wrong!!!")
    else:
        print("Session Button isn't displayed!!!")
        exit(0)

def login(login, passoword):
    # connect with login page
    print("\n\n\n") # some spaces between lines
    print("Page is loading...")
    browser.get("https://instaling.pl/teacher.php?page=login")
    print("Page is loaded!!! -> Start loging")

    login_input = browser.find_element(By.NAME, "log_email")
    passowrd_input = browser.find_element(By.NAME, "log_password")
    login_button = browser.find_element(By.XPATH, '//*[@id="main-container"]/div[3]/form/div/div[3]/button')

    put_keys_as_a_user(string=login, in_element=login_input) # add login to input
    put_keys_as_a_user(string=passoword, in_element=passowrd_input) # add password to input
    
    login_button.click() # try login user via click in sign in button

    if browser.current_url != "https://instaling.pl/teacher.php?page=login": # when user is sing in
        print("You have been signed in!!!")
    else: # when user can't be sing in
        print("Program cound't signed in you!!!")
        exit(0) # exit application whithout error because this is code 0 but no 1..


def start_instaling(user_login: str, user_password: str): # i know, i know i don't have to put types but i love staticly typed languages :)
    login(user_login, user_password) # login user
    start_new_session() # start doing daily session


if __name__ == "__main__":
    start_instaling("test_login_data", "test_password")