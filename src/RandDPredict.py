import pandas as pd
import numpy as np
import os 

def read_data_from_excel(n=42) -> tuple:
    """
    从Excel文件中读取数据，并返回原始数据矩阵、行和列的和。
    - n: 数据矩阵规模
    返回:
    - unpredict_a: 原始数据矩阵。
    - row_sums: 行和。
    - column_sums: 列和。
    """
    # org_data = pd.read_excel("2017-ZHU.xlsx",sheet_name='Sheet1')
    # predict_data = pd.read_excel("2017-ZHU.xlsx",sheet_name="Sheet2")
    org_data = pd.read_excel("input.xlsx",sheet_name="Sheet1",header=None)
    predict_data = pd.read_excel("input.xlsx",sheet_name='Sheet2',header=None)
    unpredict_a  = np.array(org_data.loc[0:n-1,0:n-1])     # 原始数据矩阵
    row_sums = np.array(predict_data.loc[0:n-1,n])       # 42个列和
    column_sums = np.array(predict_data.loc[n,0:n-1])    # 42个行和
    if unpredict_a.shape[0] != n or unpredict_a.shape[1] != n:
        raise ValueError("原始数据矩阵大小不正确！")
    elif np.sum(unpredict_a) == 0:
        raise ValueError("输入原始数据不合规")
    return unpredict_a, row_sums, column_sums



def modified_ras(T_initial, row_totals, col_totals,
                 max_iterations=10000, tolerance=1e-10000)->np.array:
    """
    使用修正RAS方法调整矩阵T_initial，使其行和列的和分别接近row_totals和col_totals。
    
    参数:
    - T_initial: 初始矩阵。
    - row_totals: 目标行总和。
    - col_totals: 目标列总和。
    - max_iterations: 最大迭代次数。
    - tolerance: 收敛容忍度。
    
    返回:
    - T_adjusted: 调整后的矩阵。
    """
    # 初始化
    rows, cols = T_initial.shape
    R = np.ones(rows)
    S = np.ones(cols)
    T_adjusted = np.copy(T_initial)
    
    for iteration in range(max_iterations):
        # 行调整
        row_sums = T_adjusted.sum(axis=1)
        R = row_totals / row_sums
        for i in range(rows):
            T_adjusted[i, :] *= R[i]
        
        # 列调整
        col_sums = T_adjusted.sum(axis=0)
        S = col_totals / col_sums
        for j in range(cols):
            T_adjusted[:, j] *= S[j]
        
        # 检查收敛
        if np.allclose(row_totals, T_adjusted.sum(axis=1), atol=tolerance) and \
           np.allclose(col_totals, T_adjusted.sum(axis=0), atol=tolerance):
            print(f"Converged in {iteration+1} iterations.")
            return T_adjusted
    
    raise TimeoutError("计算未收敛")


def calculate_accuracy(T_adjusted, row_totals, col_totals):
    """
    计算调整后矩阵的精度，包括绝对误差和相对误差。
    
    参数:
    - T_adjusted: 调整后的矩阵。
    - row_totals: 目标行总和。
    - col_totals: 目标列总和。
    
    返回:
    - 绝对误差和相对误差的字典。
    """
    adjusted_row_sums = T_adjusted.sum(axis=1)
    adjusted_col_sums = T_adjusted.sum(axis=0)
    
    # 绝对误差
    absolute_error_rows = np.abs(adjusted_row_sums - row_totals)
    absolute_error_cols = np.abs(adjusted_col_sums - col_totals)
    
    # 相对误差
    relative_error_rows = absolute_error_rows / row_totals
    relative_error_cols = absolute_error_cols / col_totals
    
    accuracy = {
        'Absolute Error (Rows)': absolute_error_rows,
        'Relative Error (Rows)': relative_error_rows,
        'Absolute Error (Cols)': absolute_error_cols,
        'Relative Error (Cols)': relative_error_cols,
    }
    
    return accuracy


def make_template(n=42) -> None:
    """
    生成数据填写模板。
    """
    current_dir = os.curdir   # 获取当前位置
    print(current_dir)
    current_files = os.listdir()
    if "input.xlsx" in current_files:
        print("当前目录下已经有input.xlsx，是否覆盖创建？")
        while True:
            _input = input("确认覆盖请输入1，否则输入0，不输入默认为0:\n")
            if len(_input) == 0 or _input.lower() == '0':
                return
            elif _input == '1':
                os.remove("input.xlsx")
                break
        
            else:
                print("输入有误。")
    
    target_input_one = np.array([[0.0 for _ in range(n)] for _ in range(n)])  #  投入产出表输入
    target_input_two = np.array([[0.0 if x == n or y == n else np.NaN for x in range(n+1)]for y in range(n+1)])
    out_one = pd.DataFrame(target_input_one)
    out_two = pd.DataFrame(target_input_two)
    # writer = pd.ExcelWriter("input.xlsx")
    with pd.ExcelWriter("input.xlsx") as writer:
        out_one.to_excel(writer,sheet_name="Sheet1", index=False,header=None)
        out_two.to_excel(writer,sheet_name="Sheet2",index=False,header=None)
    print(f"已创建模板；请将投入产出表参考值直接粘贴到Sheet1，只粘贴{n}x{n}（或者包含求和，即{n+1}x{n+1})数据，不要粘贴表头")
    print(f"在Sheet2中粘贴投入产出表的猜测依据数据，只粘贴行和列的求和值，即在第{n+1}行和第{n+1}列分别粘贴求和值。")
    


            