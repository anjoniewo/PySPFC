# Funkton gibt eine Matrix in der Konsole aus
def print_matrix(matrix):
    print('\n')
    print('\n\n'.join([''.join(['{:22}'.format(item) for item in row])
                       for row in matrix]))
    print('\n')
