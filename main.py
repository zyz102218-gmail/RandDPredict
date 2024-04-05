from RandDPredict import *


if __name__ == "__main__":
    read_org_data = None
    read_row_sums = None
    read_column_sums = None
    while True:
        print("主菜单:")
        print("【1】\t 读取数据并计算")
        print("【2】\t 生成数据填写模板")
        print("【0】\t 退出程序")
        choose = input()
        if choose == "1":
            read_org_data, read_row_sums, read_column_sums = read_data_from_excel()
            T_adu = modified_ras(read_org_data, read_row_sums, read_column_sums)
            accuracy = calculate_accuracy(T_adu, read_row_sums, read_column_sums)
            for key, value in accuracy.items():
                print(f"{key}: {value.mean()}")
            T_adu_df = pd.DataFrame(T_adu)
            T_adu_df.to_excel("output.xlsx",sheet_name="Sheet1",index=False,header=None)
            print("计算完成，结果已保存到output.xlsx")
        elif choose == '2':
            make_template()
        elif choose == '0':
            break
        else:
            print("输入有误，请重新输入")