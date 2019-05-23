# Funkton gibt eine Matrix in der Konsole aus
def print_matrix(matrix):
    print('\n')
    print('\n\n'.join([''.join(['{:22}'.format(round(float(item), 2) if item else 0) for item in row])
                       for row in matrix]))
    print('\n')
