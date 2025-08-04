"""LLM学习资源模块，提供学习指南和资源链接。"""

from typing import List, Dict, Any


class LLMResources:
    """LLM学习资源类，包含各种学习资源。"""

    @staticmethod
    def get_beginner_resources() -> List[Dict[str, str]]:
        """获取适合初学者的LLM学习资源。

        Returns:
            资源列表，每个资源包含标题、描述和链接
        """
        return [
            {
                "title": "OpenAI文档",
                "description": "OpenAI官方文档，包含API使用指南和最佳实践",
                "url": "https://platform.openai.com/docs/"
            },
            {
                "title": "提示工程指南",
                "description": "全面的提示工程学习指南，包含各种技巧和示例",
                "url": "https://www.promptingguide.ai/zh"
            },
            {
                "title": "Hugging Face课程",
                "description": "Hugging Face提供的NLP和Transformers课程",
                "url": "https://huggingface.co/learn/nlp-course/zh-CN/chapter1/1"
            },
            {
                "title": "LangChain文档",
                "description": "LangChain框架文档，用于构建LLM应用",
                "url": "https://python.langchain.com/docs/get_started/"
            },
            {
                "title": "吴恩达《ChatGPT提示工程》课程",
                "description": "吴恩达与OpenAI合作推出的提示工程课程",
                "url": "https://github.com/datawhalechina/prompt-engineering-for-developers"
            }
        ]

    @staticmethod
    def get_learning_path() -> Dict[str, List[str]]:
        """获取LLM学习路径。

        Returns:
            学习路径字典，包含不同阶段的学习内容
        """
        return {
            "基础阶段": [
                "了解大型语言模型的基本概念和工作原理",
                "学习提示工程的基础知识",
                "掌握OpenAI API的基本使用方法",
                "了解token、温度等参数的含义"
            ],
            "进阶阶段": [
                "深入学习提示工程技巧",
                "了解上下文学习和少样本学习",
                "学习LangChain等框架的使用",
                "了解向量数据库和嵌入的概念"
            ],
            "实践阶段": [
                "构建简单的问答系统",
                "实现文档摘要和信息提取",
                "开发对话式AI应用",
                "探索多模态模型的应用"
            ],
            "高级阶段": [
                "了解模型微调和训练技术",
                "学习评估和优化LLM应用",
                "探索RAG（检索增强生成）技术",
                "研究LLM的伦理和安全问题"
            ]
        }

    @staticmethod
    def get_recommended_books() -> List[Dict[str, str]]:
        """获取推荐书籍列表。

        Returns:
            书籍列表，每本书包含标题、作者和描述
        """
        return [
            {
                "title": "人工智能：现代方法（第4版）",
                "author": "Stuart Russell, Peter Norvig",
                "description": "AI领域的经典教材，提供了人工智能的全面基础知识"
            },
            {
                "title": "深度学习",
                "author": "Ian Goodfellow, Yoshua Bengio, Aaron Courville",
                "description": "深度学习领域的权威著作，对理解神经网络和大型语言模型的基础很有帮助"
            },
            {
                "title": "自然语言处理综论",
                "author": "Daniel Jurafsky, James H. Martin",
                "description": "NLP领域的经典教材，涵盖了从基础到高级的自然语言处理技术"
            },
            {
                "title": "Transformers for Natural Language Processing",
                "author": "Denis Rothman",
                "description": "专注于Transformer模型在NLP中的应用，对理解现代LLM很有帮助"
            }
        ]


def show_resources() -> None:
    """显示LLM学习资源。"""
    resources = LLMResources()
    
    print("LLM学习资源指南\n")
    
    # 显示学习路径
    print("【LLM学习路径】")
    learning_path = resources.get_learning_path()
    for stage, items in learning_path.items():
        print(f"\n{stage}:")
        for i, item in enumerate(items, 1):
            print(f"  {i}. {item}")
    
    # 显示初学者资源
    print("\n\n【推荐学习资源】")
    beginner_resources = resources.get_beginner_resources()
    for i, resource in enumerate(beginner_resources, 1):
        print(f"\n{i}. {resource['title']}")
        print(f"   {resource['description']}")
        print(f"   链接: {resource['url']}")
    
    # 显示推荐书籍
    print("\n\n【推荐书籍】")
    books = resources.get_recommended_books()
    for i, book in enumerate(books, 1):
        print(f"\n{i}. {book['title']}")
        print(f"   作者: {book['author']}")
        print(f"   简介: {book['description']}")


if __name__ == "__main__":
    show_resources()