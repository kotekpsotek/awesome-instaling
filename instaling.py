import os
import re
import time
import json
import random
import googletrans
from typing import Any, Tuple
from googletrans.models import Translated
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

webdriver_path = os.path.abspath("webdriver_path/chromedriver.exe")
browser = webdriver.Chrome(executable_path=webdriver_path)

# Imitate user in putting letters inside <textarea></textarea>'s and <input>
def put_keys_as_a_user(string: str, in_element):
    for letter in string:
        in_element.send_keys(letter)
        sleep_time = random.uniform(0.180, 0.700) # genereate random float number
        time.sleep(sleep_time)

# Function translate word from parameter to english (default) by use google translator and return translated word from her body
def translate_word_by_use_google_tr(word: str):
    translator_machine = googletrans.Translator()
    translator_word_lang_detect = translator_machine.detect(word).lang
    translated_word = translator_machine.translate(word, dest="en", src=translator_word_lang_detect) # get the translated word text
    
    return translated_word

# Function which saves added changes in .json file (This function is for function which save correct translations and for function which save bad word translations)
def save_changes_in_json_file(content, file_localization):
    serialize_changed_content_to_json_schema_again = json.dumps(content, indent=4, sort_keys=True, ensure_ascii=True)
    file_with_words_translations_write = open(file_localization, "w")
    file_with_words_translations_write.write(serialize_changed_content_to_json_schema_again)
    file_with_words_translations_write.close()

# Function which aim is save word translation in .json file with translations when this word translation doesn't already exist
## Behaviour: Word translation will be save when question_with_word_usage and word_to_translate added for function params isn't empty and when them isn't just as this keys from .json file, or Update Empty Question when in file with translations has been empty question ("question_content": "") and "word_to_translate" and "word_translation" from file is the same as these parameters added for this function 
path_with_words_translation_file: str = "./translations.json"
def save_correct_translation_in_json_file(question_with_word_usage, word_to_translate: str, word_translation: str): # TODO: Add system which checks if saved correct transaltion isn't in file with words which cound't be translated
    # Converted variables to correct form
    word_to_translate = word_to_translate.lower().strip()
    word_translation = word_translation.lower().strip()
    
    # When word translation and word to translate isn't empty
    if word_to_translate != "" and word_translation != "":
        file_with_translations_only_to_read = open(path_with_words_translation_file, "r")
        file_with_translations_content = file_with_translations_only_to_read.read()

        if file_with_translations_content.__len__() > 0: # when transations.json isn't empty then file will be updating
            # Deserialize .json file content to JSON object syntax
            file_content_json = json.loads(file_with_translations_content)

            # Get .json words list for add new words to array
            words_list_from_json_file: list[dict[str, str, str]] = file_content_json["words_list"]

            # Add new word translation to translations file
            ## Check when this word translation doesn't already exists
            key_already_has_been_translated: bool = False
            empty_question_word_translation_detected: bool = False
            for s_dict in words_list_from_json_file:
                local_question_with_word_usage = s_dict["question_content"]
                local_word_to_translate = s_dict["word_to_translate"]


                if local_question_with_word_usage == question_with_word_usage and local_word_to_translate == word_to_translate:
                    key_already_has_been_translated = True
                    break
                elif len(local_question_with_word_usage) == 0 and local_word_to_translate == word_to_translate and not empty_question_word_translation_detected: # Behaviour: Add Question to translated word with no question. When in file has been detected word with the same word to translate but with empty question and this word hasn't be detected in the past iteration
                    empty_question_word_translation_detected = True
            ### When the same key hasn't be found in .json file content with translations then this translation will be saved
            if not key_already_has_been_translated and not empty_question_word_translation_detected: # create word translation
                word_translation_dict = { "question_content": question_with_word_usage, "word_to_translate": word_to_translate, "word_translation": word_translation }
                words_list_from_json_file.append(word_translation_dict)

                # Save new added translated word in .json file with words transation
                save_changes_in_json_file(file_content_json, path_with_words_translation_file)
            elif not key_already_has_been_translated and empty_question_word_translation_detected: # Behaviour: Add Question to word translation where word where qord should be used is empty
                # Update single dict and save changes in file with translations
                for try_update_dict in words_list_from_json_file:
                    local_question_with_word_usage = try_update_dict["question_content"]
                    local_word_to_translate = try_update_dict["word_to_translate"]
                    local_word_translation = try_update_dict["word_translation"]

                    if len(local_question_with_word_usage) == 0 and local_word_to_translate == word_to_translate and local_word_translation == word_translation:
                        # New dict
                        question_updated_word_translation_dict = { "question_content": question_with_word_usage, "word_to_translate": local_word_to_translate, "word_translation": local_word_translation }
                        
                        # CRUD over file
                        words_list_from_json_file.remove(try_update_dict) # remove dict
                        words_list_from_json_file.append(question_updated_word_translation_dict) # add new updated dict
                        break

                # Save new added translated word in .json file with words transation
                save_changes_in_json_file(file_content_json, path_with_words_translation_file)
        else: # when transations.json file is empty then to file will be adding new translated word
            # Create .json file with translations JSON format Schema
            translated_words_file_json_content = { "words_list" : [{ "question_content": question_with_word_usage, "word_to_translate": word_to_translate, "word_translation": word_translation }] }

            # Save new added translated word in .json file with words transation
            save_changes_in_json_file(translated_words_file_json_content, path_with_words_translation_file)

        file_with_translations_only_to_read.close()

# Function which get translation for added word by searching word to translate in .json file with words translations. If word to translate has been found then function returns his translation or returns empty string when word to translate coudn't be found
def get_word_translation_from_file(question_with_word_usage: str, word_to_translate: str):
    # Get access to File and content from file
    file_with_translations = open(path_with_words_translation_file, "r")
    file_with_translations_content = file_with_translations.read()

    # Check if file content isn't empty
    if file_with_translations_content.__len__() > 0:
        # Deserialize JSON content from readed file to Python Disctionary type
        deserialize_file_content_to_json = json.loads(file_with_translations_content)
        list_with_translations_from_json_file = deserialize_file_content_to_json["words_list"]
        
        # Seach words to translate in words list which is from deserialized JSON file at the top and set this transaltion to variable "word_translation"
        ## Step 1. Check if word to translate is the same and question where word should be used is the same.
        word_translation: str = ""
        get_word_translation: bool = False
        for dict in list_with_translations_from_json_file:
            ## Get word to translate field and word translation from iterated disctionary type
            local_question_with_word_usage = dict["question_content"]
            local_word_to_translate = dict["word_to_translate"]
            local_word_translation = dict["word_translation"]
            
            ## When getted word to translate is just as word to translate added to function param
            if local_question_with_word_usage == question_with_word_usage and local_word_to_translate == word_to_translate:
                get_word_translation = True # When word translation can be found
                word_translation = local_word_translation
                break

        ## Step 2. Check if word_to_translate is just as word_to_translate from file when word translation coudn't be found in "Step 1"
        if not get_word_translation:
            for dict in list_with_translations_from_json_file:
                ## Get word to translate field and word translation from iterated disctionary type
                local_word_to_translate = dict["word_to_translate"]
                local_word_translation = dict["word_translation"]

                ## When getted word to translate is just as word to translate added to function param
                if local_word_to_translate == word_to_translate:
                    word_translation = local_word_translation
                    break
        # Close open file descriptor for secure reasons
        file_with_translations.close()
        
        # Return word translation or empty string when word to translate hasn't been found in JSON file content
        return word_translation
    else:
        # When file content is empty then function returns type None
        return None

# Function which save bad word translation with all added keys in function parameters in .json file (incorrect_translations.json) when this word translation isn't already exists
path_with_bad_words_translations_file: str = "./incorrect_translations.json"
def save_bad_word_translation(question_with_word_usage, word_to_translate: str, word_translation: str, type):
    """ Function params introduce:
        question_with_word_usage - this is question placed at the top of container with word to translate and this question looks like: They sell it at an __________ price,
        word_to_translate - this is world which is bad translated
        word_translation - this is bad world translation
        type - this is type of bad translation and it can be: "synonim" when word translation is synonim or "totally bad translation" when for word is added bad translation

        To save bad translation must be added 4 parameters but for verification if word translation isn't bad translated are needed only 3 params: question_with_word_usage, word_to_translate, word_translation and this process is made by function \"word_translation_is_bad()\" which returns logical value
    """
    # Converted variables to correct form
    word_to_translate = word_to_translate.lower().strip()
    word_translation = word_translation.lower().strip()

    # When word translation and word to translate isn't empty
    if word_to_translate != "" and word_translation != "":
        # Read content of file with bad word translations
        file_with_bad_translations_only_to_read = open(path_with_bad_words_translations_file, "r")
        file_with_bad_translations_content = file_with_bad_translations_only_to_read.read()

        if file_with_bad_translations_content.__len__() > 0: # when transations.json isn't empty then file will be updating
            # Deserialize .json file content to JSON object syntax
            file_content_json = json.loads(file_with_bad_translations_content)

            # Get .json bad translated words list for add new bad word translation to array
            bad_words_translation_list_from_json_file: list[dict[str, str, str]] = file_content_json["incorrect_list"]

            # Add new bad word translation to file with bad words translations
            ## Check when this bad word translation hasn't be already added
            bad_word_translation_already_has_been_added: bool = False
            for sing_bad_word_translation_dict in bad_words_translation_list_from_json_file:
                local_bad_translation_type = sing_bad_word_translation_dict["type"]
                local_word_usage_question = sing_bad_word_translation_dict["question_content"]
                local_word_to_translate = sing_bad_word_translation_dict["word_to_translate"]
                local_word_translation = sing_bad_word_translation_dict["word_translation"]

                if local_bad_translation_type == type and local_word_usage_question == question_with_word_usage and local_word_to_translate == word_to_translate and local_word_translation == word_translation:
                    bad_word_translation_already_has_been_added = True
                    break

            ### When the same bad word translation hasn't be found in .json file content with bad word translations then this bad word translation will be saved
            if not bad_word_translation_already_has_been_added:
                instance_bad_word_translation_src = { "type": type, "question_content": question_with_word_usage, "word_to_translate": word_to_translate, "word_translation": word_translation }
                bad_words_translation_list_from_json_file.append(instance_bad_word_translation_src)

                # Save new added translated word in .json file with words transation
                save_changes_in_json_file(file_content_json, path_with_bad_words_translations_file)
        else: # when incorrect_translations.json file is empty then to file will be adding new translated word
            # Create .json file with translations JSON format Schema
            bad_translated_words_file_json_content = { "incorrect_list" : [ {
                "type": type,
                "question_content": question_with_word_usage,
                "word_to_translate": word_to_translate,
                "word_translation": word_translation
            }] }

            # Save bad word translation in json file (incorrect_translations.json)
            save_changes_in_json_file(bad_translated_words_file_json_content, path_with_bad_words_translations_file)

        file_with_bad_translations_only_to_read.close()

# Function checks if added translated word isn't in bad words translation file
## Behaviour: Function returns False when word translation is correct or True when word translation is incorrect
def word_translation_is_bad(question_with_word_usage, word_to_translate, word_translation):
    file_with_bad_words_translations = open(path_with_bad_words_translations_file, "r")
    file_with_bad_words_translation_content = file_with_bad_words_translations.read()

    if len(file_with_bad_words_translation_content) > 0:
        # Answer for question "If word translation is bad?"
        local_word_translation_is_bad: bool = False
        
        # Data from json file with bad translations ("incorrect_translations.json")
        file_with_bad_words_translation_content_json = json.loads(file_with_bad_words_translation_content)
        bad_translations_list = file_with_bad_words_translation_content_json["incorrect_list"]

        # Iterate over all translations and check if this translation is bad
        for bad_translation in bad_translations_list:
            local_word_usage_question = bad_translation["question_content"]
            local_word_to_translate = bad_translation["word_to_translate"]
            local_word_translation = bad_translation["word_translation"]

            # When this word translation is bad because it is in the bad translations list
            if local_word_usage_question == question_with_word_usage and local_word_to_translate == word_to_translate and local_word_translation == word_translation:
                local_word_translation_is_bad = True
                break

        # Return check result
        return local_word_translation_is_bad
    else:
        return False

def start_new_session():
    start_session_button = browser.find_element(By.XPATH, '//*[@id="student_panel"]/p[1]/a')
    if start_session_button.is_displayed(): # when start session button is displayed
        start_session_button.click() # button "Zacznij codzienną sesję/dokończ sesję"
        if browser.current_url.__contains__("https://instaling.pl/ling2/html_app/app.php"):
            # Environment configuration variables
            timeout_between_answers_for_questions: float = 1.5 # delay between answers for questions // in seconds
            timeout_between_pass_word_and_check_it: float = 0.3 # delay between pass translated word and send it for check // in seconds
            
            # Loop which allow program to do all questions from single session
            iteration_count: int = 0
            while True:
                iteration_count += 1

                # Handle finish page after when the bot pass answers for all questions
                finish_page = browser.find_element(By.ID, "finish_page")
                if finish_page.is_displayed(): # when sessions ends
                    # Go to main instaling.pl user panel after end the session
                    go_to_main_instaling_page = browser.find_element(By.XPATH, "/html/body/div/div[12]/div[2]/h4")
                    go_to_main_instaling_page.click()
                    
                    # Stop session loop and so stop answering for session questions by program
                    print("Session ends!!!")
                    break

                # Start/Continue started session (only one page can be displayed in one time)
                start_session_page = browser.find_element(By.ID, "start_session_page")
                start_repeat_page = browser.find_element(By.ID, "start_repeat_page")
                continue_session_page = browser.find_element(By.ID, "continue_session_page")

                # This is do only when program starts session
                if iteration_count == 1:
                    button: WebElement
                    if start_session_page.is_displayed():
                        button = start_session_page.find_element(By.CLASS_NAME, "big_button")
                    elif start_repeat_page.is_displayed():
                        button = start_repeat_page.find_element(By.CLASS_NAME, "big_button")
                    elif continue_session_page.is_displayed():
                        button = continue_session_page.find_element(By.CLASS_NAME, "big_button")
                    button.click()

                #### Session words!!!!
                time.sleep(0.5) # wait 0.5 sec before starts doing asnwer action
                learning_page = browser.find_element(By.ID, "learning_page")
                
                # Handle question about "If you know this word __? If you know these word next word will be harder -> so i think you shoudn't know this word when you are bot heheheh :)"
                learning_page_question_if_you_know_new_word: WebElement = learning_page.find_element(By.XPATH, "//div[@id=\"new_word_form\"]")
                if learning_page_question_if_you_know_new_word.is_displayed():
                    # Step 1 click "No"
                    dont_know_button: WebElement = learning_page_question_if_you_know_new_word.find_element(By.XPATH, "//div[@id=\"dont_know_new\"]")
                    dont_know_button.click()

                    # Step 2 skip advice about
                    possible_word_page = browser.find_element(By.ID, "possible_word_page")

                    if possible_word_page.is_displayed():
                        # Click on "Skip" button
                        skip_button: WebElement = possible_word_page.find_element(By.ID, "skip")
                        skip_button.click()
                    continue # go to next loop iteration
                
                ## Get Data of Normal Question
                # Section with question and word/words to translate
                learning_page_question_usage_example_text: str = learning_page.find_element(By.XPATH, "//div[@id=\"question\"]/div[@class=\"usage_example\"]").text # question text
                learning_page_question_caption_translations_text: str = learning_page.find_element(By.XPATH, "//div[@id=\"question\"]/div[@class=\"caption\"]/div[@class=\"translations\"]").text # word which should be translated
                # Section with input for answer and submit button
                learning_page_learning_form_check_input: WebElement = learning_page.find_element(By.XPATH, "//div[@class=\"learning_form\"]/table//input[@id=\"answer\"]") # Input Element for the answer
                learning_page_learning_form_check_button: WebElement = learning_page.find_element(By.XPATH, "//div[@class=\"learning_form\"]/div[@id=\"check\"]") # Button to submit translation

                # Function which gets translation for added word to tranlsate or words list when first word to translate is bad translation for question word
                def translate_this_word(word_to_translate: Any):
                    """ Params:
                        word_to_translate - this can be str type with single word to translate when in question with to translate are only one word or list with words when word can have many translations
                    """
                    return_word_translation: Tuple[str, str] # in tuple should be: 0 - word_to_translate, 1 - word_translation
                    communication_word_translate: str # this is word to translate which is use only in "communication alert" when transaltion for word coundn't be getted

                    if isinstance(word_to_translate, list): # When to translate has been added list with words, with simlar meaning
                        return_word_translation = ("", "") # Set default value for tuple when this values won't be set from loop
                        communication_word_translate = word_to_translate[0] # Set default translated word

                        # Iterate over all words from list
                        for single_word_to_translate in word_to_translate:
                            local_translation = get_word_translation_from_file(learning_page_question_usage_example_text, single_word_to_translate) ## Translate getted word -> in the first stage this translation has been set from file  with translations then from google translator

                            ## Get translation word translation from Google Translator when word translation coudn't be found in JSON file
                            if len(local_translation) == 0 or local_translation == None:
                                local_translation = translate_word_by_use_google_tr(single_word_to_translate).text

                            ### Check if word translation is good or go to next iteration -> check action has been doed in "incorrect_translatrions.json" file
                            if not word_translation_is_bad(question_with_word_usage=learning_page_question_usage_example_text, word_to_translate=single_word_to_translate, word_translation=local_translation):
                                return_word_translation = (single_word_to_translate, local_translation) ## Set Returned variable correct value
                                break ## Stops loop 
                    elif isinstance(word_to_translate, str): # When to translate has been added single world
                        return_word_translation = ("", "") # Set default value for tuple when this values won't be set from loop
                        communication_word_translate = word_to_translate # Set default translated word

                        local_translation = get_word_translation_from_file(learning_page_question_usage_example_text, word_to_translate) ## Translate getted word -> in the first stage this translation has been set from file with    translations then from google translator

                        ## Get translation word translation from Google Translator when word translation coudn't be found in JSON file
                        if len(local_translation) == 0 or local_translation == None:
                            local_translation = translate_word_by_use_google_tr(word_to_translate).text

                        ### Check if word translation is good or go to next iteration -> check action has been doed in "incorrect_translatrions.json" file
                        if not word_translation_is_bad(question_with_word_usage=learning_page_question_usage_example_text, word_to_translate=word_to_translate, word_translation=local_translation):
                            return_word_translation = (word_to_translate, local_translation) ## Set Returned variable correct value

                    # When translation for word coudn't be getted from some reason and function return empty string and transaltion shoudn't be save in file with translations
                    if len(return_word_translation[0]) == 0 and len(return_word_translation[1]) == 0:
                        print("You should in future add transaltion for word: \"" + communication_word_translate + "\" because program coudn't get correct translation for it using access to added word translations by you (in file   \"translations.json\") and google transaltor")
                        print("The transaltion for this word coudn't be known, so it has been set as a empty value \"\"")

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
                put_keys_as_a_user(translated_word.lower().strip(), learning_page_learning_form_check_input) # Put translated word to input for answer
                time.sleep(timeout_between_pass_word_and_check_it)
                learning_page_learning_form_check_button.click() # Accept putted value in input

                # Check if answer is correct
                time.sleep(0.5) # wait 0.5 sec before search answer result
                answer_result_page: WebElement = browser.find_element(By.ID, "answer_page") # page with all answer containers from answer section
                answer_result_from_answer_page: WebElement = browser.find_element(By.XPATH, "//div[@id=\"answer_page\"]//h4[@id=\"answer_result\"]/div") # answer result
                answer_result_type = answer_result_from_answer_page.get_attribute("class") # value of answer result

                # Function which saves correct answer in file with correct answers when bot answered wrong
                def save_correct_answer_after_bad_answering():
                    local_word_to_translate = browser.find_element(By.XPATH, "/html/body/div/div[9]/div[1]/div[3]/div[2]") # get element with word to translate
                    local_translated_word = browser.find_element(By.XPATH, "/html/body/div/div[9]/div[1]/div[2]") # get element with word translation

                    # When "answer page" is displayed but no "finish page"
                    if local_word_to_translate.is_displayed() and local_translated_word.is_displayed():
                        # Get and extract word to translate from getted value from webpage
                        local_word_to_translate_txt = local_word_to_translate.text
                        converted_word_to_translate = re.split(";|,", local_word_to_translate_txt)[0].lower().strip()
                        # Get translated word
                        local_translated_word_txt = local_translated_word.text
                        # Save correct translation in json file
                        save_correct_translation_in_json_file(learning_page_question_usage_example_text, word_to_translate=converted_word_to_translate, word_translation=local_translated_word_txt)

                ## Source of checking if word translation is correct
                if answer_result_type == "green": # answer is correct
                    # Save word transation in .json file when this word translation isn't already exist
                    save_correct_translation_in_json_file(learning_page_question_usage_example_text, word_to_translate, translated_word)
                    # print answer color
                    print("green")
                elif answer_result_type == "blue": # answer is incorrect because putted word is synonim or in word has been detected typo error
                    # Save incorrect word into specific file and form for "blue"
                    save_bad_word_translation(learning_page_question_usage_example_text, word_to_translate, translated_word, "synonim")
                    # Save correct word translation after bad answer
                    save_correct_answer_after_bad_answering()
                    # print answer color
                    print("blue")
                elif answer_result_type == "red": # answer is totally incorrect
                    # Save incorrect word into specific file and form for "red"
                    save_bad_word_translation(learning_page_question_usage_example_text, word_to_translate, translated_word, "totally bad translation")
                    # Save correct word translation after bad answer
                    save_correct_answer_after_bad_answering()
                    # print answer color
                    print("red")
                else:
                    raise ValueError("Unexpected answer result!!! Program has handled only: red, green and blue answer result")

                # Go to next question or cancel session when last answer has been pass
                check_answer_page = browser.find_element(By.XPATH, "/html/body/div/div[9]")

                if check_answer_page.is_displayed(): # when next question is availeble
                    # Go to next Question via click in "Następne" button after end previous question
                    go_to_next_question_button = browser.find_element(By.XPATH, "/html/body/div/div[9]/div[4]/h4")
                    go_to_next_question_button.click()

                    # Timeout between answers for questions
                    time.sleep(timeout_between_answers_for_questions)

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
    save_correct_translation_in_json_file("Question where word whould be used v4.0", "pizza", "Test")
    # print(word_translation_is_bad(question_with_word_usage="Tina always tries to support _____ ___________.", word_to_translate="lokalne rzemiosło artystyczne", word_translation="local handicratfs"))
    # start_instaling("test_login_data", "test_password")