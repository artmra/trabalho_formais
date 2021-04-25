from io_utils.ine5421.functions import read_pseudocode

sample_pseudo_code = "function_definition; er: def#\n" \
                     "if_token; er: if#" \
                     # "else_token; er: else#\n" \
                     # "function_name; er: name#\n" \
                     # "class_definition; er: class#"

read_pseudocode(sample_pseudo_code)
