from io_utils.ine5421.functions import create_af_from_al

sample_pseudo_code = "function_definition; er: def#\n" \
                     "if_token; er: if#\n" \
                     "else_token; er: else#\n" \
                     "function_name; er: name#\n" \
                     "class_definition; er: class#"

create_af_from_al(sample_pseudo_code)
