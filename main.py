import argparse
from get_set_login_data import get_login_data
from instaling import start_instaling
from additional_configs import ALLOWED_ANSWERS # Allowed answers for configuration arguments/commands

def add_arguments_and_commands(arg_parser_inst: argparse.ArgumentParser):
    # Run bot in different manner
    arg_parser_inst.add_argument("--run", help="Run bot. You must attach boolean \"true\" to run bot otherwise bot won't be launch (dichotomous scale = only two available options) (action is equal to don't any argument)", required=False, type=bool)
    
    # Start bot configuration
        # Run configuration
    config_com_params = {
        "help": "Accepted only boolean true to perform designed action. Configure options for bot such as words case type for answers sentences",
        "required": False,
        "type": bool,
    } 
    arg_parser_inst.add_argument("--config", **config_com_params)
    arg_parser_inst.add_argument("-c", **config_com_params)

def main():
    # Configure argument parser
    parser_options = {
        "prog": "Awesome-Instaling the best instaling.pl bot",
        "description": "Bot which helps you in instaling.pl daily sessions",
        "epilog": ":)"
    }
    arg_parser = argparse.ArgumentParser(**parser_options)

    # Add commands and arguments in abbreviate way
    add_arguments_and_commands(arg_parser_inst=arg_parser)
    
    # Parse args and process args depends on recived arg
    parsed_args = arg_parser.parse_args() 

    if len(parsed_args._get_args()) == 0 or ("--run" in parsed_args and parsed_args["--run"]):
        login, password = get_login_data().values() # get login data and quick destructure them
        start_instaling(login, password) # start instaling
        # print("The login is: " + login + "\n" + "The password is: " + password)
    else:
        # TODO:
        print(parsed_args)

if __name__ == "__main__":
    main()