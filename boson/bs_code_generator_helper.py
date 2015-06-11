__author__ = 'ict'

from boson.bs_configure import *


def bs_indent(indent_sum):
    return (configure["indent_string"] * configure["indent_number"]) * indent_sum


def bs_code_output(output, code_string, indent_sum=0):
    output.write(bs_indent(indent_sum) + code_string)
