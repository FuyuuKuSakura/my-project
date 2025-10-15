import matplotlib.pyplot as plt
import numpy as np

def FunctionMode() -> str :
    Mode = input("请输入要操作的对象（方程组/矩阵）:")
    return Mode

def GetFunctionGroup() -> dict:      #to catch the function group and transform it into matrix
    FunctionGroup = {}
    group_num = int(input("请输入方程数"))
    for i in range(1, group_num + 1):
        FunctionGroup[f'function_{i}'] = str(input("请输入方程"+str(i)))
    return FunctionGroup

def GetMatrix() -> np.ndarray :
    row_num = int(input("请输入行数"))
    array = []
    print("请输入矩阵内容，逐行输入")
    for i in range(1, row_num + 1) :
        row = list(map(float, input(f"第{i}行: ").split()))
        array.append(row)
    matrix = np.array(array)
    return matrix

def FindCoefficient(FunctionGroup: dict) -> np.ndarray:   #transform the function group into authentic matrix
    coefficient = []
    for i in range(1, len(FunctionGroup) + 1):
        # 初始化每个方程的系数列表，包含5个位置：[x系数, y系数, z系数, w系数, 常数项]
        coeff_list = [0, 0, 0, 0, 0]
        func_str = FunctionGroup[f'function_{i}']
        
        # 处理每个变量
        variables = ['x', 'y', 'z', 'w', '=']
        left = 0
        
        for right, char in enumerate(func_str):
            if char in variables:
                index = variables.index(char)
                
                # 提取系数
                coeff_str = func_str[left:right].strip()
                if coeff_str == '' or coeff_str == '+':
                    coeff_value = 1
                elif coeff_str == '-':
                    coeff_value = -1
                else:
                    # 处理系数可能包含符号的情况
                    if coeff_str.endswith('+') or coeff_str.endswith('-'):
                        coeff_str = coeff_str[:-1]
                    try:
                        coeff_value = float(coeff_str)
                    except ValueError:
                        coeff_value = 1  # 如果转换失败，默认为1
                
                if char == '=':
                    # 常数项在等号右边，需要改变符号
                    coeff_list[4] = float(func_str[right+1:])
                else:
                    coeff_list[index] = coeff_value
                
                left = right + 1
    
        coefficient.append(coeff_list)
    
    coefficient = np.array(coefficient)
    
    NonZeroColumns = np.any(coefficient != 0, axis=0)
    UltimateMatrix = coefficient[:, NonZeroColumns]
    return UltimateMatrix

def AuthenticResolving(Matrix : np.ndarray) -> np.ndarray :
    A = Matrix[:,:-1]
    b = Matrix[:,-1]    
    return A, b

 #def Elimination(Matrix : np.ndarray) -> np.ndarray :
    
def IsSolvable(Matrix : np.ndarray) -> str :
    m, n = Matrix.shape
    A, b = AuthenticResolving(Matrix)
    RankCoefficient = np.linalg.matrix_rank(A)
    RankMatrix = np.linalg.matrix_rank(Matrix)
    situation = ""
    if RankCoefficient == RankMatrix:
        if RankCoefficient == (n - 1):
            situation = "one solution"
        else:
            situation = "infinite solution"
    else:
        situation = "no solution"
    return situation

def Elimination(Matrix : np.ndarray) :
    m, n = Matrix.shape
    row = 0
    if IsSolvable(Matrix) != "one solution" :
        print(IsSolvable(Matrix))
        return None
    while row < m :
        if row != 0 :
            for i in range(row) :
                Matrix[row] -= Matrix[row][i] * Matrix[i]
                print('row' + str(row + 1)+ ' - ' + str(Matrix[row][i]) + '*' + 'row' + str(i + 1))
                print(Matrix)
        Matrix[row] = Matrix[row] / Matrix[row][row]
        print('row' + str(row + 1) + '/' + str(Matrix[row][row]))
        print(Matrix)
        row += 1
    row = 0
    while row < m :
        if row != m - 1:
            for i in range(row + 1, m) :
                Matrix[row] -= Matrix[row][i] * Matrix[i]
                print('row' + str(row + 1)+ ' - ' + str(Matrix[row][i]) + '*' + 'row' + str(i + 1))
                print(Matrix)
        row += 1

def IsRowEchelonForm(matrix : np.ndarray) -> bool :
    m, n = matrix.shape
    index = 0
    for row in range(m) :
        for column in range(n) :
            if matrix[row][column] != 0 :
                if row == 0 and column == 0 :
                    break
                if column <= index :
                    return False
                else : 
                    index = column
                break
    return True 

def RowEchelonForm(matrix : np.ndarray) -> np.ndarray :
    m, n = matrix.shape
    row = 0
    while row < m :
        if row != 0 :
            for i in range(row) :
                Matrix[row] -= Matrix[row][i] * Matrix[i]
                print('row' + str(row + 1)+ ' - ' + str(Matrix[row][i]) + '*' + 'row' + str(i + 1))
                print(Matrix)
        row += 1

                



def IsReducedRowEchelonForm(matrix : np.ndarray) -> bool :
    m, n = matrix.shape
    if IsRowEchelonForm(matrix) == False :
        print("This is not even a row echelon form")
        return False
    else :
        pivots = []
        for row in range(m) :
            for column in range(n) :
                if matrix[row][column] != 0 :
                    if row == 0 and column != 0 :
                        return False
                    else : 
                        pivots.append((row, column))
                        break
        for row, column in pivots:
            for i in range(m):
                if i != row: 
                    if matrix[i, column] != 0:
                        return False
        return True

#def ReducedRowEchelonForm(matrix : np.ndarray) -> np.ndarray :


if __name__ == "__main__":
    mode = FunctionMode()
    if mode == '方程组' :
        FunctionGroup = GetFunctionGroup()
        Matrix = FindCoefficient(FunctionGroup)
        A, b = AuthenticResolving(Matrix)
        if IsSolvable(Matrix) == 'one solution' :
            solution = np.linalg.solve(A, b)
            print(solution)
        else :
            print(IsSolvable(Matrix))
        Elimination(Matrix)
    elif mode == '矩阵' :
        Matrix = GetMatrix()
        if IsRowEchelonForm(Matrix) == True :
            print("This is a row echelon form")
            if IsReducedRowEchelonForm(Matrix) == True :
                print("This is a reduced row echelon form")
            else :
                print("This is not a reduced row echelon form")
        else :
            print("This is not a echelon form")
        