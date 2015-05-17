__author__ = 'Fule Liu'


from boson.bs_grammmar_analysis import bs_token_list as bs_token_list


if __name__ == "__main__":
    token_list = bs_token_list("not_slr_grammar.txt")
    print(token_list)
