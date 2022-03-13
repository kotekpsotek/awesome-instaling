import os
import time
import json
import random
from typing import Any, Tuple
import googletrans
from googletrans.models import Translated
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

def translate_word_by_use_google_tr(word: str): # this function translate word from parameter to english (default) by use google translator and return translated word from her body
    translator_machine = googletrans.Translator()
    translator_word_lang_detect = translator_machine.detect(word).lang
    translated_word = translator_machine.translate(word, dest="en", src=translator_word_lang_detect) # get the translated word text
    
    return translated_word

path_with_words_translation_file: str = "./translations.json"
def save_translation_in_json_file(word_to_translate, word_translation): # Function which aim is save word translation in .json file with translations when this word translation doesn't already exist
    # Function which saves added changes in .json file
    def save_changes_in_json_file(content):
        serialize_changed_content_to_json_schema_again = json.dumps(content, indent=4, sort_keys=True)
        file_with_words_translations_write = open(path_with_words_translation_file, "w")
        file_with_words_translations_write.write(serialize_changed_content_to_json_schema_again)
        file_with_words_translations_write.close()
    
    file_with_translations_only_to_read = open(path_with_words_translation_file, "r")
    file_with_translations_content = file_with_translations_only_to_read.read()

    if file_with_translations_content.__len__() > 0: # when transations.json isn't empty then file will be updating
        # Deserialize .json file content to JSON object syntax
        file_content_json = json.loads(file_with_translations_content)
        
        # Get .json words list for add new words to array
        words_list_from_json_file: list[dict[str, str]] = file_content_json["words_list"]
        
        # Add new word translation to translations file
        ## Check when this word translation doesn't already exists
        key_already_has_been_translated: bool = False
        for s_dict in words_list_from_json_file:
            if s_dict["word_question"] == word_to_translate:
                key_already_has_been_translated = True
                break
        ### When the same key hasn't be found in .json file content with translations then this translation will be saved
        if not key_already_has_been_translated:
            word_translation_dict = { "word_question": word_to_translate, "word_translation": word_translation }
            words_list_from_json_file.append(word_translation_dict)
            
            # Save new added translated word in .json file with words transation
            save_changes_in_json_file(file_content_json)
    else: # when transations.json file is empty then to file will be adding new translated word
        # Create .json file with translations JSON format Schema
        translated_words_file_json_content = { "words_list" : [{ "word_question": word_to_translate, "word_translation": word_translation }] }
        
        # Save new added translated word in .json file with words transation
        save_changes_in_json_file(translated_words_file_json_content)

    file_with_translations_only_to_read.close()

def get_word_translation_from_file(word_question: str): # function which get translation for added word by searching word to translate in .json file with words translations. If word to translate has been found then function returns his translation or returns empty string when word to translate coudn't be found
    # Get access to File and content from file
    file_with_translations = open(path_with_words_translation_file, "r")
    file_with_translations_content = file_with_translations.read()

    # Check if file content isn't empty
    if file_with_translations_content.__len__() > 0:
        # Deserialize JSON content from readed file to Python Disctionary type
        deserialize_file_content_to_json = json.loads(file_with_translations_content)
        list_with_translations_from_json_file = deserialize_file_content_to_json["words_list"]
        
        # Seach words to translate in words list which is from deserialized JSON file at the top and set this transaltion to variable "word_translation"
        word_translation: str = ""
        for dict in list_with_translations_from_json_file:
            ## Get word to translate field and word translation from iterated disctionary type
            local_word_question = dict["word_question"]
            local_word_translation = dict["word_translation"]
            
            ## When getted word to translate is just as word to translate added to function param
            if local_word_question == word_question:
                word_translation = local_word_translation
                break
        # Close open file descriptor for secure reasons
        file_with_translations.close()
        
        # Return word translation or empty string when word to translate hasn't been found in JSON file content
        return word_translation
    else:
        # When file content is empty then function returns type None
        return None

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

            # Function which gets translation for added word to tranlsate or TODO: words list when first word to translate is bad translation for question word
            def translate_this_word(word_to_translate: Any):
                """ Params:
                    word_to_translate - this can be str type with single word to translate when in question with to translate are only one word or list with words when word can have many translations
                """
                return_word_translation: Tuple[str, str] # in tuple should be: 0 - word_to_translate, 1 - word_translation

                if isinstance(word_to_translate, list):
                    for single_word_to_translate in word_to_translate:
                        ######## This manner is only temprary TODO: Check word is correct to translate (this file is correct when it isn't on files translations blacklist)
                        ## Translate getted word -> in the first stage this translation has been set from file with translations then from google translator
                        local_translation = get_word_translation_from_file(single_word_to_translate)
                        ## Get translation word translation from Google Translator when word translation coudn't be found in JSON file
                        if len(local_translation) == 0 or local_translation == None:
                            local_translation = translate_word_by_use_google_tr(single_word_to_translate).text
                        ## Set Returned variable correct value
                        return_word_translation = (single_word_to_translate, local_translation)
                        ## Stops loop 
                        break
                elif isinstance(word_to_translate, str):
                    ## Translate getted word -> in the first stage this translation has been set from file with translations then from google translator
                    local_translation = get_word_translation_from_file(word_to_translate)
                    ## Get translation word translation from Google Translator when word translation coudn't be found in JSON file
                    if len(local_translation) == 0 or local_translation == None:
                        local_translation = translate_word_by_use_google_tr(word_to_translate).text
                    ## Set Returned variable correct value
                    return_word_translation = (word_to_translate, local_translation)

                return return_word_translation

            # Converted word to translation (the result is the single word)
            word_to_translate: str # this is the word which is translating
            translated_word: str # this is the translated word

            # Get and set word to translate and this word translation
            if learning_page_question_caption_translations_text.__contains__(","):
                ## Get word which must be translated
                word_to_translate_list = learning_page_question_caption_translations_text.split(",")
                ## Get word translation
                translation_result = translate_this_word(word_to_translate=word_to_translate_list)
                ## Set values for outside variables
                word_to_translate = translation_result[0] # word which is translating
                translated_word = translation_result[1] # translated word

            elif learning_page_question_caption_translations_text.__contains__(";"):
                ## Get word which must be translated
                word_to_translate_list = learning_page_question_caption_translations_text.split(";")
                ## Get word translation
                translation_result = translate_this_word(word_to_translate=word_to_translate_list)
                ## Set values for outside variables
                word_to_translate = translation_result[0] # word which is translating
                translated_word = translation_result[1] # translated word
            else:
                ## Get word which must be translated
                word_to_translate = learning_page_question_caption_translations_text.strip()
                ## Get word translation
                translated_word = translate_this_word(word_to_translate=word_to_translate)[1]

            # Put answer to input and accept by click in accept answer button
            put_keys_as_a_user(translated_word, learning_page_learning_form_check_input) # Put translated word to input for answer
            learning_page_learning_form_check_button.click() # Accept putted value in input

            # Check if answer is correct
            time.sleep(0.5) # wait 0.5 sec before search answer result
            answer_result_page: WebElement = browser.find_element(By.ID, "answer_page") # page with all answer containers from answer section
            answer_result_from_answer_page: WebElement = browser.find_element(By.XPATH, "//div[@id=\"answer_page\"]//h4[@id=\"answer_result\"]/div") # answer result
            answer_result_type = answer_result_from_answer_page.get_attribute("class") # value of answer result
            
            print("Word: " + word_to_translate + " has been translated as a: " + translated_word)
            if answer_result_type == "green": # answer is correct
                # Save word transation in .json file when this word translation isn't already exist
                save_translation_in_json_file(word_to_translate, translated_word)

                # print answer color
                print("green")
            elif answer_result_type == "blue": # answer is incorrect because putted word is synonim or in word has been detected typo error
                ### TODO: Save incorrect word into specific file and form for "blue"
                # print answer color
                print("blue")
            elif answer_result_type == "red": # answer is totally incorrect
                ### TODO: Save incorrect word into specific file and form for "red"
                # print answer color
                print("red")
            else:
                raise ValueError("Unexpected answer result!!! Program has handled only: red, green and blue answer result")

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