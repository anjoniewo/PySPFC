import numpy as np


# Funkton gibt eine Matrix in der Konsole aus
def print_matrix(matrix):
    print('\n')
    print('\n\n'.join([''.join(['{:22}'.format(round(float(item), 2) if item else 0) for item in row])
                       for row in matrix]))
    print('\n')


# Matrix-Vektor-Produkt
def matrix_vector_product(matrix, vector):
    result_vector = np.ndarray(shape=(len(matrix)), dtype=float)

    for row in range(len(matrix)):
        result_i = 0
        for column in range(len(matrix)):
            matrix_entry = matrix[row][column]
            vector_entry = vector[column]
            entry_product = matrix_entry * vector_entry
            result_i += entry_product

        result_vector[row] = result_i

    return result_vector
