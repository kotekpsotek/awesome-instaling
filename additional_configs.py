import json as j
import os

INSTANCE_CONFIG_PATH: str = os.path.join(os.getcwd(), "config", "ad_config.json")
ALLOWED_ANSWERS: list[str] = ["bg", "ev", "lw"]

# Determing How sentence words should looks
class WordsCaseMode():
    # Run whole mechanism
    def run() -> bool:
        # To chanage configuration old config file spcific in path "INSTANCE_CONFIG_PATH" must not exists
        WordsCaseMode.process_input_result()

    # Put to stdout all question required for this feature (defined in class) and obtain answers from stdin
    def _get_input_result() -> str:
        return input("Determine how answers words should looks\n(bg - Begin sentence with upper case letter/ev - Each sentence word begin with uppercase/lw (default) - every sentence word begin with lower case letter): ")

    def _check_conf_file_schema():
        pass

    # Return parsed from json to dict configuration file content
    def get_conf_file_parsed() -> dict:
        file = open(INSTANCE_CONFIG_PATH, "r").read()
        file = j.loads(file)
        return file

    # Change existsing config to new or re-save config with new configuration datas
    def _retain_or_save_config(answer_sen_case_type: str):
        # Enter to stdout message about incorrect structure of config file
        def inc_stdout():
            print(f"Couldn't save configuration file \"{INSTANCE_CONFIG_PATH}\"!")

        try:
            # Set configuration
            conf_f_c: dict[str, str] = { "words_case_type": "" }

            #! Correct structure of config file must be maintained to swear working 
            # Setup word case type for answer sentences
            if len(answer_sen_case_type) > 0:
                # Configure letter case type for each/begining word from answered sentence
                conf_f_c["words_case_type"] = answer_sen_case_type
                
                # Save changed config datas to file
                conf_f_c = j.dumps(conf_f_c, sort_keys=True, indent=4)
                open(INSTANCE_CONFIG_PATH, "w").write(conf_f_c)

                # Save configuration information for user
                print("Configuration has been successfull saved!")
            else:
                # send incorrect message to stdout
                inc_stdout()
        except:
            # send incorrect message to stdout
            inc_stdout()


    # Conjusction in order to get user answers for questions (using: _get_input_result()) and save it or update it in file (using: _retain_or_save_config(_))
    def process_input_result():
        # To Save/Re-save settings all setting file must not exists
        if os.path.exists(INSTANCE_CONFIG_PATH):
            default_answer = "lw"
            answer = WordsCaseMode._get_input_result()
            
            # Check recived answer
            if answer in ALLOWED_ANSWERS:
                # When user put allowed answer
                WordsCaseMode._retain_or_save_config(answer)
            elif len(answer) == 0:
                # Use dafault answer when user skip this answer
                WordsCaseMode._retain_or_save_config(default_answer)
            else:
                # Invalid answer: Try again to obtain duly answer
                WordsCaseMode.process_input_result()
        else:
            print(f"Configuration file \"{INSTANCE_CONFIG_PATH}\" doesn't exists!. Create it with appropriate schema")

# Run primitive test/tests
if __name__ == "__main__":
    WordsCaseMode.run()
