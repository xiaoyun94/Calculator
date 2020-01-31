# -*- coding: utf-8 -*-

from math import *
from subprocess import run
import re
import os

class IntPrint:
    def __init__(self, radix, name): 
        self.radix = radix
        self.name = name

    def format(self, num):
        if self.radix == 16:
            return "0x" + hex(num)[2:].upper()
        elif self.radix == 2:
            return bin(num)
        else:
            return str(num)

try:
    from scipy.special import *
    from builtins import *
    import numpy as np

    c = binom
except Exception as e:
    pass

sqr = lambda x: x ** 2


def json_wox(title, subtitle, icon, action=None, action_params=None, action_keep=None):
    json = {
        'Title': title,
        'SubTitle': subtitle,
        'IcoPath': icon
    }
    if action and action_params and action_keep:
        json.update({
            'JsonRPCAction': {
                'method': action,
                'parameters': action_params,
                'dontHideAfterAction': action_keep
            }
        })
    return json

def copy_to_clipboard(text):
    cmd = 'echo ' + text.strip() + '| clip'
    #os.system(cmd)
    run(cmd, shell=True)

def format_result(result):
    if hasattr(result, '__call__'):
        # show docstring for other similar methods
        raise NameError
    if isinstance(result, str):
        return result
    if isinstance(result, int) or isinstance(result, float):
        if int(result) == float(result):
            return '{:,}'.format(int(result)).replace(',', ' ')
        else:
            return '{:,}'.format(round(float(result), 5)).replace(',', ' ')
    elif hasattr(result, '__iter__'):
        try:
            return '[' + ', '.join(list(map(format_result, list(result)))) + ']'
        except TypeError:
            # check if ndarray
            result = result.flatten()
            if len(result) > 1:
                return '[' + ', '.join(list(map(format_result, result.flatten()))) + ']'
            else:
                return format_result(np.asscalar(result))
    else:
        return str(result)


int_prints = [ IntPrint(10, "DEC"), IntPrint(16, "HEX"), IntPrint(2, "BIN") ]

def append_result(results, title, query, ret):
    results.append(json_wox(title,
                   '{} = {}'.format(query, ret),
                   'icons/2333.jpg',
                   'change_query',
                   [ret.replace(" ", "")],
                   True))

def calculate(query): 
    results = []
    # filter any special characters at start or end
    query = re.sub(r'(^[*/=])|([+\-*/=(]$)', '', query)
    try:
        result = eval(query)
        
        if isinstance(result, float) and result == int(result): # convert to type int, avoid using integer oper forcelly
            result = int(result)
                
        if isinstance(result, int):
            for int_print in int_prints:
                formatted = int_print.format(result)
                append_result(results, '[{}] {}'.format(int_print.name, formatted), query, formatted)
        else:
            formatted = format_result(result)
            append_result(results, '[{}] {}'.format('DEC', formatted), query, formatted)
            if isinstance(result, float):
                results.extend(calculate("ceil({})".format(query)));
                results.extend(calculate("floor({})".format(query)));

    except SyntaxError:
        # try to close parentheses
        opening_par = query.count('(')
        closing_par = query.count(')')
        if opening_par > closing_par:
            return calculate(query + ')'*(opening_par-closing_par))
        else:
            # let Wox keep previous result
            raise SyntaxError
    except NameError:
        # try to find docstrings for methods similar to query
        glob = set(filter(lambda x: 'Error' not in x and 'Warning' not in x and '_' not in x, globals()))
        help = list(sorted(filter(lambda x: query in x, glob)))[:6]
        for method in help:
            method_eval = eval(method)
            method_help = method_eval.__doc__.split('\n')[0] if method_eval.__doc__ else ''
            results.append(json_wox(method,
                                    method_help,
                                    'icons/2333.jpg',
                                    'change_query_method',
                                    [str(method)],
                                    True))
        if not help:
            # let Wox keep previous result
            raise NameError
    return results

from wox import Wox, WoxAPI


class Calculator(Wox):
    def query(self, query):
        return calculate(query)

    def change_query(self, query):
        # change query and copy to clipboard after pressing enter
        #WoxAPI.change_query(query + "=")
        copy_to_clipboard(query)

    def change_query_method(self, query):
        WoxAPI.change_query(query + '(')


if __name__ == '__main__':
    Calculator()
