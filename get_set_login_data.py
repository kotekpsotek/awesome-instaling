import json
import os

def add_or_change_login_data(login: str, passwd: str): # function which can create login data file or can change login data
    login_data_disctionary = {"login": login, "pass": passwd} # 1 - login, 2 - passowrd (always only two values or less)

    if login.__len__() == 0: # When login must be changed/added
        result = input("Add your instaling.pl login: ")
        login_data_disctionary['login'] = result

    if passwd.__len__() == 0: # When passowrd must be changed/added
        result = input("Add your instaling.pl password: ")
        login_data_disctionary['pass'] = result

    data_serialized_to_json_ready = json.dumps(login_data_disctionary) # serialized data to JSON format
    open("config/loginData.json", "w").write(data_serialized_to_json_ready) # write data to json file
    
    return login_data_disctionary
    
def get_login_data():
    # Check whether configuration file exists within config folder and when it doesn't exists force user to add required login data
    if os.path.exists("./config/loginData.json"):
        try:
            login_data_file = open("config/loginData.json", "r")
            login_data_file_text = login_data_file.read()

            if login_data_file_text.__len__() > 0: # when in config/loginData.json file is some text content
                json_obj_with_login = json.loads(login_data_file_text) # deserialize json document to python object

                login: str = json_obj_with_login['login']
                password: str = json_obj_with_login['pass']

                # When fields required to login are empty
                add_or_change_login_data(login=login, passwd=password)

                return json_obj_with_login
            else: # user must add data to login
                login_data_return = add_or_change_login_data(login="", passwd="")
        except json.JSONDecodeError:
            print("Format of .json file with login data (config/loginData.json) is bad!!!")

            login_data_return = add_or_change_login_data(login="", passwd="")
            return login_data_return
        except KeyError as key:
            key_name = key.args[0]

            print("In JSON login data file (config/loginData.json) isn't required key: " + key_name)

            login_data_return = add_or_change_login_data(login="", passwd="")
            return login_data_return
    else:
        login_data_return = add_or_change_login_data(login="", passwd="")
        return login_data_return