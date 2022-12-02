import argparse, typing, re
from get_set_login_data import get_login_data
from instaling import start_instaling
from additional_configs import WordsCaseMode # site to configure additional options

def add_arguments_and_commands(arg_parser_inst: argparse.ArgumentParser):
    # Run bot in different manner
    arg_parser_inst.add_argument("--run", help="Run bot. You must attach boolean \"true\" to run bot otherwise bot won't be launch (dichotomous scale = only two available options) (action is equal to don't any argument)", required=False, type=bool)
    
    # Bot additional options configuration
        # Start bot configuration
    config_com_params = {
        "help": "Accepted only boolean true to perform designed action. Configure options for bot such as words case type for answers sentences",
        "required": False,
        "type": bool,
    } 
    arg_parser_inst.add_argument("--config", **config_com_params)
    arg_parser_inst.add_argument("-c", **config_com_params)
        # Display this configuration
    display_addconfig_argsfor = {
        "help": "Show actual additional options configuration. Required: true to perform action (accept only boolean values)",
        "required": False,
        "type": bool
    }
    arg_parser_inst.add_argument("--adconfshow", **display_addconfig_argsfor)
    arg_parser_inst.add_argument("-ads", **display_addconfig_argsfor)


# Check whether any argument has been passed durning launching the program
# Return (boolean): "True" when argument has been passed or "False" in oposite site
def check_some_argument_hb_passed(arguments: list[tuple[str, typing.Any]]) -> bool:
    find: bool
    for arg in arguments:
        find = (arg[1] != None)
        if find:
            break
    return find

def main():
    # Configure argument parser
    parser_options = {
        "prog": "Awesome-Instaling the best instaling.pl bot",
        "description": "Bot which helps you in instaling.pl daily sessions",
        "epilog": "Use command to configure/do specific action with bot or don't attach any argument to simply run bot :)"
    }
    arg_parser = argparse.ArgumentParser(**parser_options)

    # Add commands and arguments in abbreviate way
    add_arguments_and_commands(arg_parser_inst=arg_parser)
    
    # Parse args and process args depends on recived arg
    parsed_args = arg_parser.parse_args()
    ind_any_arg_passed = check_some_argument_hb_passed(parsed_args._get_kwargs())

    if (not ind_any_arg_passed) or ("run" in parsed_args and parsed_args.run == True):
        # Run bot when all allowed arguments haven't been passed or has been passed "--run" argument with assigned boolean "true" value
        login, password = get_login_data().values() # get login data and quick destructure them
        start_instaling(login, password) # start instaling
    else:
        # Handle other supported arguments/commands
        if ("c" in parsed_args and parsed_args.c) or ("config" in parsed_args and parsed_args.config):
            # Run configuration for additional bot options
            WordsCaseMode.run()
        elif parsed_args.ads or parsed_args.adconfshow:
            # Display actuall additional options configuration
                # Obtain options values
            file_content: dict = WordsCaseMode.get_conf_file_parsed()
            res_for_output = ""
            for (key, value) in file_content.items():
                single_val = f"{key} = {value}\n"
                res_for_output += single_val
            res_for_output = re.split("\n$", res_for_output)[0]
                # Display that values
            print(f"Configured additional bot options are:\n\n{res_for_output}")
        else:
            # Unsupported arguments are handled automaticaly by "argparse" module
            pass 
        

if __name__ == "__main__":
    main()