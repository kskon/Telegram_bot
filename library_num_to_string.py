# -*- python3 -*-
# -*- coding: utf-8-*-
# author: github.com/seriyps
# code adaptation: kskonovalov100@gmail.com
# copyright

""" 
This is library to converting numbers to string: 123 one hundred twenty three.
WARNING: this is limited converter maximum rank hundreds of trillions.
"""

import re

units = (
    'ноль',
    ('один', 'одна'),
    ('два', 'две'),

    'три', 'четыре', 'пять',
    'шесть', 'семь', 'восемь', 'девять'
)

teens = (
    'десять', 'одиннадцать',
    'двенадцать', 'тринадцать',
    'четырнадцать', 'пятнадцать',
    'шестнадцать', 'семнадцать',
    'восемнадцать', 'девятнадцать'
)

tens = (
    teens,
    'двадцать', 'тридцать',
    'сорок', 'пятьдесят',
    'шестьдесят', 'семьдесят',
    'восемьдесят', 'девяносто'
)

hundreds = (
    'сто', 'двести',
    'триста', 'четыреста',
    'пятьсот', 'шестьсот',
    'семьсот', 'восемьсот',
    'девятьсот'
)

orders = (
    (('тысяча', 'тысячи', 'тысяч'), 'f'),
    (('миллион', 'миллиона', 'миллионов'), 'm'),
    (('миллиард', 'миллиарда', 'миллиардов'), 'm'),
    (('триллион', 'триллиона', 'триллонов'), 'm'),
)

minus = 'минус'

whole = ('целая', 'целых')

fractional = (
    ('десятая', 'десятых'),
    ('сотая', 'сотых'),
    ('тысячная', 'тысячных'),
    ('десятитысячная', 'десятитысячных'),
    ('стотысячная', 'стотысячных'),
    ('миллионная', 'миллионных'),
    ('десятимиллионная', 'десятимиллионных'),
    ('стомиллионная', 'стомиллионных'),
    ('миллиардная', 'миллиардных'),
    ('десятимиллиардная', 'десятимиллиардных'),
    ('стомиллиардная', 'стомиллиардных'),
    ('триллиардная', 'триллиардных'),
    ('десятитриллиардная', 'десятитриллиардных'),
    ('стотриллиардная', 'стотриллиардных'),
)


def number_validator(num):
    """
    Function to check input number. If user insert string or mixing string
    validator return exception message.
    """
    new_number = num
    num = False

    new_number = re.sub(r',', '.', str(new_number))
    find_int = re.search(r'^-?\d+$', new_number)
    find_float = re.search(r'^-?\d+\.\d+$', new_number)

    if find_int and len(new_number) < 16:
        num = [int(new_number)]

    elif find_float:
        point_position = new_number.index('.')

        if len(new_number[:point_position]) < 16 and \
           len(new_number[point_position+1:]) < 16:
            num = [new_number[:point_position], new_number[point_position+1:]]
    return num


def thousand(rest, sex, flag):
    """Converts numbers from 19 to 999."""

    prev = 0
    plural = 2
    name = []
    use_teens = 10 <= rest % 100 <= 19

    if not use_teens:
        data = ((units, 10), (tens, 100), (hundreds, 1000))
    else:
        data = ((teens, 10), (hundreds, 1000))
    for names, x in data:
        cur = int(((rest - prev) % x) * 10 / x)
        prev = rest % x
        if x == 10 and use_teens:
            plural = 2
            name.append(teens[cur])
        elif cur == 0:
            continue
        elif x == 10:
            name_ = names[cur]
            if isinstance(name_, tuple):
                name_ = name_[0 if sex == 'm' and not flag else 1]
            name.append(name_)
            if 2 <= cur <= 4:
                plural = 1
            elif cur == 1:
                plural = 0
            else:
                plural = 2
        else:
            name.append(names[cur-1])
    return plural, name


def numbers_to_text_converter(num, main_units=(('', '', ''), 'm')):
    """
    Main function fo convert numbers to string.
    """

    final_name = []
    flag = False
    fraction_flag = 0

    num = number_validator(num)

    if not num:
        return 'Sorry you insert not valid date'

    # To throw flag for
    if len(num) == 2:
        flag = True

    for number in num:
        rest = abs(float(number))
        float_nuber = float(number)
        name = []
        ords = 0

        if float_nuber == 0:
            if number == '-0':
                final_name.extend((minus, units[0], whole[1]))
            else:
                final_name.extend((units[0], ))
            fraction_flag = 1
            continue

        _orders = (main_units,) + orders
        while rest > 0:
            plural, nme = thousand(rest % 1000, _orders[ords][1], flag)
            if nme or ords == 0:
                name.append(_orders[ords][0][plural])
            name += nme
            rest = int(rest / 1000)
            ords += 1
        # To delete one more space
        name.pop(0)

        if float_nuber < 0:
            name.append(minus)

        # adding value of whole and fractional
        if name[0][-1] == 'а' and flag:
            if fraction_flag == 0:
                name.insert(0, whole[0])
            elif fraction_flag == 1:
                name.insert(0, fractional[len(name) - 1][0])
        elif fraction_flag == 0 and flag:
            name.insert(0, whole[1])
        elif fraction_flag == 1:
            name.insert(0, fractional[len(name) - 1][1])

        fraction_flag = 1

        name.reverse()
        final_name.extend(name)
    return ' '.join(final_name).strip()

