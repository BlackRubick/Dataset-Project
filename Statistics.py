import random
import scipy.stats as stats
import statistics as sc
import pandas as pd


def mode(data):
    mode_all = sc.mode(data)
    return mode_all


def median(data):
    median_all = sc.median(data)
    return median_all


def mean(data):
    mean_all = sc.mean(data)
    return mean_all


def bias(data):
    bias_all = stats.skew(data)
    return bias_all


def truncated_mean(data):
    truncated = stats.trim_mean(data, 0.2)
    return truncated


def geometry(data):
    geometry_all = sc.geometric_mean(data)
    return geometry_all


def variance(data):
    variance_all = sc.variance(data)
    return variance_all


def variance_p(data, mean):
    variance_all = sc.pvariance(data, mean)
    return variance_all


def temporal(data, window_size):
    mean_time = []
    num_data = len(data)

    for i in range(num_data):
        window = []

        inicio = max(0, i - window_size + 1)
        fin = i + 1
        window = data[inicio:fin]

        if len(window) >= window_size:
            media = sum(window) / window_size
            mean_time.append(media)

    print(len(mean_time))
    return mean_time


def standard_deviation(data):
    stde = sc.stdev(data)
    return stde


def get_conglomerates(data, cong_size):
    num_cong = len(data) // cong_size

    conglomerates = []

    for i in range(num_cong):
        start_index = i * cong_size
        end_index = start_index + cong_size

        cluster = data[start_index:end_index]

        conglomerates.append(cluster)

    return random.choice(conglomerates)


def moda(frecuency, marks):
    index_max_value = frecuency.index(max(frecuency))
    return marks[index_max_value]


def promedio(array1, array2, tamaño_total):
    multiplicacion = [a * b for a, b in zip(array1, array2)]

    suma = sum(multiplicacion)

    promed = suma / tamaño_total

    return promed

def variance_all(mark, absolute, total, promedio):
    resultado1 = [(x ** 2) * y for x, y in zip(mark, absolute)]
    resultado = (sum(resultado1) - total * (promedio ** 2)) / (total - 1)
    return resultado