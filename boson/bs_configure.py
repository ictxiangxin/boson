end_symbol = "$"
null_symbol = "~"

literal_template = "literal_%d"

boson_name = "Boson"
boson_package_name = "boson"
boson_version_main = 0
boson_version_sub = 6
boson_title = "%s v%d.%d" % (boson_name, boson_version_main, boson_version_sub)
boson_author = "ict"
boson_author_email = "ictxiangxin@gmail.com"
boson_url = "https://github.com/ictxiangxin/boson"
boson_description = "Grammar analyzer generator"
boson_license = "GPL v3"

boson_template_directory = "templates"
boson_template_postfix = ".template"

invalid_token_class = "boson_invalid_token"

boson_table_sign_error = "e"
boson_table_sign_shift = "s"
boson_table_sign_reduce = "r"
boson_table_sign_accept = "a"

option = {
    "start_symbol":        "start",
    "analyzer_class_name": "BosonGrammarAnalyzer",
    "grammar_class_name":  "BosonGrammar",
}
