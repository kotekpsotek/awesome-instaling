import json

login_data_file = open("config/loginData.json", "r")
login_data_file_text = login_data_file.read()

def add_or_change_login_data(login: str, passwd: str): # function which can create login data file or can change login data
    print("")

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
    

try:
    if login_data_file_text.__len__() > 0: # when in config/loginData.json file is some text content
        json_obj_with_login = json.loads(login_data_file_text) # deserialize json document to python object
        
        login: str = json_obj_with_login['login']
        password: str = json_obj_with_login['pass']
        
        # When fields required to login are empty
        if login.__len__() == 0: # When user login value is empty
            json_obj_with_login = add_or_change_login_data(login="", passwd=password)
        if password.__len__() == 0: # When user passowrd is empty
            json_obj_with_login = add_or_change_login_data(login=login, passwd="")

        # TODO: Things after get or set user login data
    else: # user must add data to login
        add_or_change_login_data(login="", passwd="")
except json.JSONDecodeError:
    print("Format of .json file with login data (config/loginData.json) is bad!!!")
except KeyError as key:
    key_name = key.args[0]
    
    print("In JSON login data file (config/loginData.json) isn't required key: " + key_name)
    
    add_or_change_login_data(login="", passwd="")
finally:
    login_data_file.close()