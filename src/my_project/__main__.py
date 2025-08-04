"""项目主入口模块。"""

import os
import sys
from typing import List, Dict, Any

from .llm_basics import demonstrate_llm_usage
from .exercises import list_exercises
from .resources import show_resources

# 尝试导入示例模块
try:
    from .examples.text_summarization import demonstrate_summarization
    from .examples.question_answering import demonstrate_qa_system
    EXAMPLES_AVAILABLE = True
except ImportError:
    EXAMPLES_AVAILABLE = False


def show_menu() -> List[Dict[str, Any]]:
    """显示主菜单并返回菜单项。

    Returns:
        菜单项列表
    """
    menu_items = [
        {"id": 1, "name": "LLM基础演示", "func": demonstrate_llm_usage},
        {"id": 2, "name": "查看学习资源", "func": show_resources},
        {"id": 3, "name": "查看练习列表", "func": list_exercises},
    ]
    
    # 如果示例模块可用，添加示例菜单项
    if EXAMPLES_AVAILABLE:
        menu_items.extend([
            {"id": 4, "name": "文本摘要示例", "func": demonstrate_summarization},
            {"id": 5, "name": "问答系统示例", "func": demonstrate_qa_system},
        ])
    
    print("\n" + "=" * 50)
    print("LLM学习项目 - 主菜单")
    print("=" * 50)
    
    for item in menu_items:
        print(f"{item['id']}. {item['name']}")
    
    print("0. 退出")
    print("=" * 50)
    
    return menu_items


def main() -> None:
    """主函数，显示菜单并处理用户选择。"""
    print("欢迎使用LLM学习项目！")
    print("这是一个为新手设计的LLM学习项目，帮助你了解大型语言模型的基础知识。")
    
    while True:
        menu_items = show_menu()
        
        try:
            choice = input("\n请选择一个选项 (0-{0}): ".format(len(menu_items)))
            choice = int(choice.strip())
            
            if choice == 0:
                print("\n感谢使用LLM学习项目！祝你学习愉快！\n")
                break
            
            # 查找并执行选择的功能
            for item in menu_items:
                if item["id"] == choice:
                    print("\n" + "=" * 50)
                    print(f"执行: {item['name']}")
                    print("=" * 50 + "\n")
                    item["func"]()
                    input("\n按Enter键继续...")
                    break
            else:
                print(f"\n无效的选择，请输入0-{len(menu_items)}之间的数字")
                
        except ValueError:
            print("\n请输入有效的数字")
        except KeyboardInterrupt:
            print("\n\n操作已取消。")
            break
        except Exception as e:
            print(f"\n发生错误: {str(e)}")


def print_learning_tips() -> None:
    """打印学习提示。"""
    print("\n学习提示：")
    print("1. 查看docs目录中的入门指南和提示工程指南")
    print("2. 尝试修改src/my_project中的代码，探索不同的参数和设置")
    print("3. 完成exercises.py中的练习，巩固所学内容")
    print("4. 运行examples目录中的示例，了解LLM的实际应用")


if __name__ == "__main__":
    try:
        main()
        print_learning_tips()
    except KeyboardInterrupt:
        print("\n\n程序已终止。")
        sys.exit(0)