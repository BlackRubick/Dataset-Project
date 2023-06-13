import math
import pandas as pd


def limits(min_data, width):
    limit_lower = min_data
    limite_superior = limit_lower + width
    return limit_lower, limite_superior


def width_class(number, range, type):
    width = range / number
    if type == 'float64':
        print(type)
        return width
    else:
        return round(width)


def number_class(column):
    number = 1 + (3.33 * math.log10(column))
    class_num = round(number)
    return class_num


def range(column):
    result = max(column) - min(column)
    return result


def class_mark(limit_lower, limit_superior):
    mark = (limit_lower + limit_superior) / 2
    return mark


def absolute_frecuency(data, limit_lower, limit_superior):
    array_count = []
    array_first = []
    contain = list(zip(limit_lower, limit_superior))
    for v in data:
        if limit_lower[0] <= v <= limit_superior[0]:
            array_first.append(v)
    array_count.append(len(array_first))
    for j, (x, y) in enumerate(contain):
        if j > 0:
            count = sum(x < v <= y for v in data)
            array_count.append(count)
    return array_count


def relative_frecuency(frecuency, all_data):
    relative = (frecuency * 100) / all_data
    return relative
