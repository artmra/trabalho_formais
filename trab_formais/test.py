from io_utils.ine5421.functions import create_af_from_al, read_pseudocode

rules =  "function_definition; er: def#\n" \
                     "if_token; er: if#\n" \
                     "else_token; er: else#\n" \
                     "function_name; er: name#\n" \
                     "class_definition; er: class#"

af = create_af_from_al(rules)

sample_pseudo_code = "def if class name while"
# sample_pseudo_code = "function_definition; er: def#\n" \
#                      "if_token; er: if#\n" \
#                      "else_token; er: else#\n" \
#                      "function_name; er: name#\n" \
#                      "class_definition; er: class#"

result = read_pseudocode(sample_pseudo_code, af)

print(result)
