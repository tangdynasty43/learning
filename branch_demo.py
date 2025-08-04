# 分支演示文件
# 这个文件是在 feature/learning-demo 分支上创建的

def branch_demo():
    """
    演示Git分支功能
    """
    print("这是在功能分支上开发的新功能！")
    print("分支名称: feature/learning-demo")
    
    # 模拟一个新功能
    features = [
        "独立开发环境",
        "不影响主分支",
        "可以安全实验",
        "完成后合并到主分支"
    ]
    
    print("\n分支的优势:")
    for i, feature in enumerate(features, 1):
        print(f"{i}. {feature}")

if __name__ == "__main__":
    branch_demo()