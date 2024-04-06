from RandDPredict import *


if __name__ == "__main__":
    read_org_data = None
    read_row_sums = None
    read_column_sums = None
    n = 42
    while True:
        print("主菜单:")
        print(f"当前投入产出表数据规模设定为{n}，投入产出表数据规模为{n}x{n}，求和值处于第{n+1}行/列")
        print("【1】\t 读取数据并计算")
        print("【2】\t 生成数据填写模板")
        print("【3】\t 设置投入产出表数据矩阵规模")
        print("【0】\t 退出程序")
        choose = input()
        if choose == "1":
            read_org_data, read_row_sums, read_column_sums = read_data_from_excel(n)
            T_adu = modified_ras(read_org_data, read_row_sums, read_column_sums)
            accuracy = calculate_accuracy(T_adu, read_row_sums, read_column_sums)
            for key, value in accuracy.items():
                print(f"{key}: {value.mean()}")
            T_adu_df = pd.DataFrame(T_adu)
            T_adu_df.to_excel("output.xlsx",sheet_name="Sheet1",index=False,header=None)
            print("计算完成，结果已保存到output.xlsx")
        elif choose == '2':
            make_template(n)
        elif choose == '3':
            print(f"请输入数据矩阵规模，当前为{n}：")
            _n = input()
            try:
                __n = int(_n)
            except ValueError:
                print("输入错误，请保证输入为整数")
            else:
                n = __n
                print(f"设置成功，已设置为{n}")
        elif choose == '0':
            break
        else:
            print("输入有误，请重新输入")
            
            