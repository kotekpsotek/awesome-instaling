from get_set_login_data import get_login_data

def main():
    login, password = get_login_data().values() # get login data and quick destructure them
    print("The login is: " + login + "\n" + "The password is: " + password)

if __name__ == "__main__":
    main()