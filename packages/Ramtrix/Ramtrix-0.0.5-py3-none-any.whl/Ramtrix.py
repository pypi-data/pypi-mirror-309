#all matrices must be rectangular
def row_reduce(matrix1):
    """
    Outputs Matrix in Row Reduced Echelon Format.
    """
    if not check_matrix(matrix1):
        print("Please input a valid matrix")
        return
    inputMatrix = [row[:] for row in matrix1]
    for rownum in range(len(inputMatrix)):
        pivot = 0
        pivot_colnum = "WAIT"
        for colnum in range(len(inputMatrix[rownum])):
            if pivot == 0:
                pivot = inputMatrix[rownum][colnum]
            if pivot != 0:
                if pivot_colnum == "WAIT": pivot_colnum = colnum
                #divide everything by the pivot
                inputMatrix[rownum][colnum] = inputMatrix[rownum][colnum]/pivot
        if pivot_colnum == "WAIT":
            continue
        for nest_rownum in range (len(inputMatrix)):
            #check every row to ensure the pivot alone is the nonzero one(literally)
            if inputMatrix[nest_rownum][pivot_colnum] != 0 and nest_rownum != rownum:
                scalar = inputMatrix[nest_rownum][pivot_colnum]/inputMatrix[rownum][pivot_colnum]
                for nest_colnum in range(len(inputMatrix[nest_rownum])):
                    inputMatrix[nest_rownum][nest_colnum] -= inputMatrix[rownum][nest_colnum]*scalar
    return inputMatrix


def transpose(matrix1):
    """
    Transposes matrix(rows to columns columns to rows)
    """
    if not check_matrix(matrix1):
        print("Please input a valid matrix")
        return
    new_matrix=[([0] * len(matrix1)) for _ in range(len(matrix1[0]))]
    for row in range(len(matrix1)):
        for col in range(len(matrix1[row])):
            new_matrix[col][row] = matrix1[row][col]
    return new_matrix


def cofactor(matrix1):
    """
    Creates a cofactor matrix(checkerboard signs)
    """
    if not check_matrix(matrix1):
        print("Please input a valid matrix")
        return
    result = [[matrix1[row][col] * pow(-1,(row+col)) for col in range(len(matrix1[row]))] for row in range(len(matrix1))]
    return result


def flatten(matrix1):
    """
    Flattens Matrix/Turns N-Dimension Matrix to 1-Dimension Matrix. Does not resort.
    """
    flat_matrix = [matrix1[row][col] for row in range(len(matrix1)) for col in range(len(matrix1[row]))]
    return flat_matrix


def determinant(matrix1):
    """
    Finds Determinant of a matrix. Requires a NxN square Matrix where N>1.
    """
    if not check_matrix(matrix1, check_Square=True):
        print("Please input a valid matrix")
        return
    determ = 0
    if len(matrix1)>2:
        for item in range(len(matrix1[0])):
            relevant_matrix = [row[:] for row in matrix1]
            relevant_matrix.pop(0)
            for row in range(len(relevant_matrix)):
                relevant_matrix[row].pop(item)
            determ+=determinant(relevant_matrix)*matrix1[0][item]*pow(-1,item)
    elif len(matrix1) == 2:
        determ = matrix1[0][0]*matrix1[1][1]-matrix1[0][1]*matrix1[1][0]
    else:
        determ = "Unable to calculate Matrix. Ensure the dimensions of your matrix are greater than 1."
    return determ


def inverse(matrix1, multiplyDet=True):
    """
    Finds the inverse of the provided matrix. Requires a square Matrix.
    """
    if not check_matrix(matrix1, check_Square=True):
        print("Please input a valid matrix")
        return
    determ = determinant(matrix1)
    if determ == 0:
        return("No inverse exists; Determinant is 0")
    result = [row[:] for row in matrix1]

    #Make Matrix of Minors(DONE)
    if len(matrix1)>2:
        for row in range(len(matrix1)):
            for col in range(len(matrix1[row])):
                relevant_matrix = [row[:] for row in matrix1]
                relevant_matrix.pop(row)
                for row_nest in range(len(relevant_matrix)):
                    relevant_matrix[row_nest].pop(col)
                result[row][col] = determinant(relevant_matrix)
    elif len(matrix1)==2:
        result = [[matrix1[(row + 1)%2][(col+1)%2] for col in range(len(matrix1[row]))] for row in range(len(matrix1))]
    else:
        print("bad matrix")
    #Make Cofactors(DONE)
    result = cofactor(result)
    #Make Adjugate(DONE)
    result = transpose(result)
    # Multiply by 1/Determinant(DONE)
    if multiplyDet:
        result = scale(result, 1/determ)
        return result
    else:
        return result, determ

def dot(vector1, vector2):
    """Finds dot product of vectors. Vectors must be the same length."""
    if (len(vector1) != len(vector2)) or (vector1[0] is None) or ((type(vector1[0]) != type(1.02)) and (type(vector1[0]) != type(1))) or ((type(vector2[0]) != type(1.02)) and (type(vector2[0]) != type(1))):
        
        print("Please input valid vectors")
        return
    result=[vector1[item]*vector2[item] for item in range(len(vector1))]
    return sum(result)


def add(matrix1, matrix2):
    """Adds Matrices. Matrices must have the same dimensions"""
    if not(check_matrix(matrix1) and check_matrix(matrix2) and len(matrix1) == len(matrix2) and len(matrix1) == len(matrix2)):
        print("Please input valid matrices")
        return
    result = [[matrix1[row][col] + matrix2[row][col] for col in range(len(matrix1[row]))] for row in range(len(matrix1))]
    return result


def subtract(matrix1, matrix2):
    """Subtracts Matrices. Matrices must have the same dimensions."""
    if not(check_matrix(matrix1) and check_matrix(matrix2) and len(matrix1) == len(matrix2) and len(matrix1) == len(matrix2)):
        print("Please input valid matrices")
        return
    result = [[matrix1[row][col] - matrix2[row][col] for col in range(len(matrix1[row]))] for row in range(len(matrix1))]
    return result


def scale(matrix1, scalar):
    """Multiplies Matrix by a scalar. (Works on any 2d array even non-rectangular ones so long as every entry is a number)"""
    result = [[matrix1[row][col]*scalar for col in range(len(matrix1[row]))] for row in range(len(matrix1))]
    return result


def matrix_multiply(matrix1,matrix2):
    """Multiplies two matrices. Matrix1 must be an MxN matrix and Matrix2 must be an NxO matrix. Resulting Matrix will be MxO."""
    if not (check_matrix(matrix1) and check_matrix(matrix2) and (len(matrix1[0]) == len(matrix2))):
        print("Please input valid matrices") 
        return
    matrix2_adjust = transpose(matrix2)
    result = [[dot(matrix1[row],matrix2_adjust[row2]) for row2 in range(len(matrix2_adjust))] for row in range(len(matrix1))]
    return result


def print_matrix(matrix1):
    """Prints Matrices more legibly"""
    for row in matrix1:
        print(row)


def check_matrix(matrix1, check_Square = False):
    if type(matrix1[0]) != type([1,1,1]) or len(matrix1) < 1:
        return False
    col_len = len(matrix1[0])
    for row in range(1, len(matrix1)):
        if col_len != len(matrix1[row]):
            return False
    if check_Square == True:
        return (col_len==len(matrix1))
    return True

def tell_version():
    print("v0.0.5")