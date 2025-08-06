import os
import pandas as pd

def cg_in_time(road_of_xslx,sheet_name):
    try:
        cg=pd.read_excel(road_of_xslx,sheet_name)
        
        # 数据探索
        print(f"数据形状: {cg.shape}")
        print(f"列名: {cg.columns.tolist()}")
        print("\n前5行数据:")
        print(cg.head(len(cg)))
        return "success"
    except Exception as e:
        print(f"错误: {e}")
        return 'defeat'

# 提示用户输入文件路径和sheet名称进行测试(先固定路径和sheet名称，后期更改input为固定值)
road_of_xslx = "C:/Users/唐朝/Desktop/12345.xlsx"
sheet_name = "Sheet1"
# 检查文件是否存在
if not os.path.exists(road_of_xslx):
    print(f"错误: 文件 {road_of_xslx} 不存在")
    exit(1)

print(f"正在处理文件: {road_of_xslx}")
print(f"工作表: {sheet_name}")
print("-" * 50)

result = cg_in_time(road_of_xslx, sheet_name)
print(f"\n处理结果: {result}")# 利用现有的pandas + openpyxl
