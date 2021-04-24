from io_utils.ine5421.functions import read_pseudocode

sample_pseudo_code = "function_definition; er: def#\n" \
                     "function_name; er: name#\n" \
                     "if_token; er: if#\n" \
                     "else_token; er: else#\n" \
                     "class_definition; er: class#"

read_pseudocode(sample_pseudo_code)
