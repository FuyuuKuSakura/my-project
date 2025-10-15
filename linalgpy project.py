import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class linalgpy:
    def __init__(self, root):
        self.root = root
        self.root.title("linalgpy project")
        self.root.geometry("800x600")
        
        # To build the main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # To choose the mode
        self.mode_var = tk.StringVar(value="function_group")
        self.create_mode_selection()
        
        # input area
        self.create_input_area()
        
        # result_area
        self.create_result_area()
        
        # button_area
        self.create_button_area()
        
    def create_mode_selection(self):
        mode_frame = ttk.LabelFrame(self.main_frame, text="Mode", padding="5")
        mode_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Radiobutton(mode_frame, text="function group", variable=self.mode_var, 
                       value="function_group", command=self.on_mode_change).grid(row=0, column=0, padx=10)
        ttk.Radiobutton(mode_frame, text="matrix", variable=self.mode_var, 
                       value="matrix", command=self.on_mode_change).grid(row=0, column=1, padx=10)
    
    def create_input_area(self):
        self.input_frame = ttk.LabelFrame(self.main_frame, text="输入区域", padding="5")
        self.input_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # To input the function group
        self.equation_frame = ttk.Frame(self.input_frame)
        self.equation_label = ttk.Label(self.equation_frame, text="方程数量:")
        self.equation_label.grid(row=0, column=0, padx=5)
        self.equation_num = tk.StringVar(value="2")
        self.equation_spinbox = ttk.Spinbox(self.equation_frame, from_=1, to=10, 
                                           textvariable=self.equation_num, width=5,
                                           command=self.create_equation_inputs)
        self.equation_spinbox.grid(row=0, column=1, padx=5)
        self.equation_inputs_frame = ttk.Frame(self.equation_frame)
        self.equation_inputs_frame.grid(row=1, column=0, columnspan=2, pady=5)
        
        # 矩阵输入
        self.matrix_frame = ttk.Frame(self.input_frame)
        self.matrix_label = ttk.Label(self.matrix_frame, text="shape(row, column):")
        self.matrix_label.grid(row=0, column=0, padx=5)
        self.rows_var = tk.StringVar(value="2")
        self.cols_var = tk.StringVar(value="2")
        self.rows_spinbox = ttk.Spinbox(self.matrix_frame, from_=1, to=10, 
                                       textvariable=self.rows_var, width=3)
        self.rows_spinbox.grid(row=0, column=1, padx=2)
        self.cols_spinbox = ttk.Spinbox(self.matrix_frame, from_=1, to=10, 
                                       textvariable=self.cols_var, width=3)
        self.cols_spinbox.grid(row=0, column=2, padx=2)
        ttk.Button(self.matrix_frame, text="create the matrix", 
                  command=self.create_matrix_inputs).grid(row=0, column=3, padx=5)
        self.matrix_inputs_frame = ttk.Frame(self.matrix_frame)
        self.matrix_inputs_frame.grid(row=1, column=0, columnspan=4, pady=5)
        self.equation_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        self.matrix_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        self.on_mode_change()
    
    def create_equation_inputs(self):
        # erase the present entry
        for widget in self.equation_inputs_frame.winfo_children():
            widget.destroy()
        
        try:
            num_eq = int(self.equation_num.get())
            self.equation_entries = []
            
            for i in range(num_eq):
                ttk.Label(self.equation_inputs_frame, text=f"function {i+1}:").grid(row=i, column=0, padx=5, pady=2)
                entry = ttk.Entry(self.equation_inputs_frame, width=40)
                entry.grid(row=i, column=1, padx=5, pady=2)
                entry.insert(0, self.get_example_equation(i, num_eq))
                self.equation_entries.append(entry)
        except ValueError:
            pass
    
    def get_example_equation(self, idx, total):
        examples = [
            "2x + 3y = 7",
            "x - y = 1",
            "x + y + z = 6",
            "2x - y + z = 3",
            "x + 2y - z = 4"
        ]
        return examples[idx] if idx < len(examples) else "x = 1"
    
    def create_matrix_inputs(self):
        # erase the present entry
        for widget in self.matrix_inputs_frame.winfo_children():
            widget.destroy()
        
        try:
            rows = int(self.rows_var.get())
            cols = int(self.cols_var.get())
            self.matrix_entries = []
            
            for i in range(rows):
                row_entries = []
                for j in range(cols):
                    entry = ttk.Entry(self.matrix_inputs_frame, width=8)
                    entry.grid(row=i, column=j, padx=2, pady=2)
                    entry.insert(0, "0")
                    row_entries.append(entry)
                self.matrix_entries.append(row_entries)
        except ValueError:
            messagebox.showerror("error", "please entre a correct matrix")
    
    def on_mode_change(self):
        mode = self.mode_var.get()
        if mode == "function_group":
            self.equation_frame.grid()
            self.matrix_frame.grid_remove()
            self.create_equation_inputs()
        else:
            self.equation_frame.grid_remove()
            self.matrix_frame.grid()
            self.create_matrix_inputs()
    
    def create_button_area(self):
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="compute", command=self.calculate).grid(row=0, column=0, padx=10)
        ttk.Button(button_frame, text="erase", command=self.clear).grid(row=0, column=1, padx=10)
        ttk.Button(button_frame, text="help", command=self.show_help).grid(row=0, column=2, padx=10)
    
    def create_result_area(self):
        self.result_frame = ttk.LabelFrame(self.main_frame, text="result", padding="5")
        self.result_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.result_text = scrolledtext.ScrolledText(self.result_frame, width=70, height=15)
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # To extend result ares
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(3, weight=1)
        self.result_frame.columnconfigure(0, weight=1)
        self.result_frame.rowconfigure(0, weight=1)
    
    def calculate(self):
        try:
            mode = self.mode_var.get()
            self.result_text.delete(1.0, tk.END)
            
            if mode == "function_group":
                self.solve_equations()
            else:
                self.analyze_matrix()
                
        except Exception as e:
            messagebox.showerror("error", f"error in: {str(e)}")
    
    def solve_equations(self):
        # catch the function group
        FunctionGroup = {}
        for i, entry in enumerate(self.equation_entries):
            equation = entry.get().strip()
            if equation:
                FunctionGroup[f'function_{i+1}'] = equation
        
        if not FunctionGroup:
            messagebox.showwarning("warning", "please entre an equation at least")
            return
        
        # transform into matrix
        Matrix = self.FindCoefficient(FunctionGroup)
        
        # show the authentic matrix
        self.result_text.insert(tk.END, "authentic matrix:\n")
        self.result_text.insert(tk.END, f"{Matrix}\n\n")
        
        # solvable?
        solution_type = self.IsSolvable(Matrix)
        self.result_text.insert(tk.END, f"is_solvable: {solution_type}\n\n")
        
        if solution_type == "one solution":
            A, b = self.AuthenticResolving(Matrix)
            try:
                solution = np.linalg.solve(A, b)
                self.result_text.insert(tk.END, "solution of the function group:\n")
                variables = ['x', 'y', 'z', 'w'][:len(solution)]
                for var, val in zip(variables, solution):
                    self.result_text.insert(tk.END, f"{var} = {val:.4f}\n")
            except np.linalg.LinAlgError:
                self.result_text.insert(tk.END, "miscalculated\n")
        
        # excute pocess of elimination
        self.result_text.insert(tk.END, "\nprocess of gaussian-elimination:\n")
        self.Elimination(Matrix.copy())
    
    def analyze_matrix(self):
        try:
            # catch the matrix
            rows = len(self.matrix_entries)
            cols = len(self.matrix_entries[0])
            matrix_data = []
            
            for i in range(rows):
                row_data = []
                for j in range(cols):
                    value = float(self.matrix_entries[i][j].get())
                    row_data.append(value)
                matrix_data.append(row_data)
            
            Matrix = np.array(matrix_data)
            
            # show the matrix
            self.result_text.insert(tk.END, "plz entre the matrix:\n")
            self.result_text.insert(tk.END, f"{Matrix}\n\n")
            
            # anlyze the matrix
            if self.IsRowEchelonForm(Matrix):
                self.result_text.insert(tk.END, "this is a row echelon form\n")
                if self.IsReducedRowEchelonForm(Matrix):
                    self.result_text.insert(tk.END, "this is a reduced row echelon form\n")
                else:
                    self.result_text.insert(tk.END, "this is not a reduced row echelon form\n")
            else:
                self.result_text.insert(tk.END, "this is not a row echelon form\n")
            
            # 显示矩阵的秩
            rank = np.linalg.matrix_rank(Matrix)
            self.result_text.insert(tk.END, f"\nrank of the matrix: {rank}\n")
            
        except ValueError:
            messagebox.showerror("error", "plz entre correct numbers")
    
    def clear(self):
        self.result_text.delete(1.0, tk.END)
        if self.mode_var.get() == "function_group":
            for entry in self.equation_entries:
                entry.delete(0, tk.END)
        else:
            for row in self.matrix_entries:
                for entry in row:
                    entry.delete(0, tk.END)
                    entry.insert(0, "0")
    
    def show_help(self):
        help_text = """
Introduction:

Function Group Mode:
- Entre functions ,such as "2x + 3y = 7"
- only variables: x , y, z, w
- This program would solve it automatically via authentic matrix

For instance:
  "2x + 3y = 7"
  "x - y = 1"
  "x + y + z = 6"

Matrix Mode:
- Entre a matrix
- This program would fin out if it is a ref/rref, and return the rank of matrix

        """
        messagebox.showinfo("help", help_text)
    
    def FindCoefficient(self, FunctionGroup: dict) -> np.ndarray:
        coefficient = []
        for i in range(1, len(FunctionGroup) + 1):
            coeff_list = [0, 0, 0, 0, 0]
            func_str = FunctionGroup[f'function_{i}']
            
            variables = ['x', 'y', 'z', 'w', '=']
            left = 0
            
            for right, char in enumerate(func_str):
                if char in variables:
                    index = variables.index(char)
                    
                    coeff_str = func_str[left:right].strip()
                    if coeff_str == '' or coeff_str == '+':
                        coeff_value = 1
                    elif coeff_str == '-':
                        coeff_value = -1
                    else:
                        if coeff_str.endswith('+') or coeff_str.endswith('-'):
                            coeff_str = coeff_str[:-1]
                        try:
                            coeff_value = float(coeff_str)
                        except ValueError:
                            coeff_value = 1
                    
                    if char == '=':
                        coeff_list[4] = float(func_str[right+1:])
                    else:
                        coeff_list[index] = coeff_value
                    
                    left = right + 1
        
            coefficient.append(coeff_list)
        
        coefficient = np.array(coefficient)
        
        NonZeroColumns = np.any(coefficient != 0, axis=0)
        UltimateMatrix = coefficient[:, NonZeroColumns]
        return UltimateMatrix

    def AuthenticResolving(self, Matrix: np.ndarray):
        A = Matrix[:,:-1]
        b = Matrix[:,-1]    
        return A, b

    def IsSolvable(self, Matrix: np.ndarray) -> str:
        m, n = Matrix.shape
        A, b = self.AuthenticResolving(Matrix)
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

    def Elimination(self, Matrix: np.ndarray):
        m, n = Matrix.shape
        row = 0
        if self.IsSolvable(Matrix) != "one solution":
            self.result_text.insert(tk.END, f"{self.IsSolvable(Matrix)}\n")
            return None
        
        self.result_text.insert(tk.END, "elimination:\n")
        while row < m:
            if row != 0:
                for i in range(row):
                    Matrix[row] -= Matrix[row][i] * Matrix[i]
                    self.result_text.insert(tk.END, f'row{row + 1} - {Matrix[row][i]:.2f} * row{i + 1}\n')
                    self.result_text.insert(tk.END, f"{Matrix}\n\n")
            
            if Matrix[row][row] != 0:  # invold 0 mistakes
                Matrix[row] = Matrix[row] / Matrix[row][row]
                self.result_text.insert(tk.END, f'row{row + 1} / {Matrix[row][row]:.2f}\n')
                self.result_text.insert(tk.END, f"{Matrix}\n\n")
            row += 1
        
        self.result_text.insert(tk.END, "substitute:\n")
        row = 0
        while row < m:
            if row != m - 1:
                for i in range(row + 1, m):
                    Matrix[row] -= Matrix[row][i] * Matrix[i]
                    self.result_text.insert(tk.END, f'row{row + 1} - {Matrix[row][i]:.2f} * row{i + 1}\n')
                    self.result_text.insert(tk.END, f"{Matrix}\n\n")
            row += 1

    def IsRowEchelonForm(self, matrix: np.ndarray) -> bool:
        m, n = matrix.shape
        index = -1
        for row in range(m):
            for column in range(n):
                if not np.isclose(matrix[row][column], 0):
                    if column <= index:
                        return False
                    else: 
                        index = column
                    break
        return True

    def IsReducedRowEchelonForm(self, matrix: np.ndarray) -> bool:
        m, n = matrix.shape
        if not self.IsRowEchelonForm(matrix):
            return False
        else:
            pivots = []
            for row in range(m):
                for column in range(n):
                    if not np.isclose(matrix[row][column], 0):
                        pivots.append((row, column))
                        # To check if the pivots are 1
                        if not np.isclose(matrix[row, column], 1):
                            return False
                        break
            
            for row, column in pivots:
                for i in range(m):
                    if i != row: 
                        if not np.isclose(matrix[i, column], 0):
                            return False
            return True

def main():
    root = tk.Tk()
    app = linalgpy(root)
    root.mainloop()

if __name__ == "__main__":
    main()






    