"""LLM基础模块，展示大型语言模型的基本用法。"""

import os
from typing import List, Dict, Any, Optional


class SimpleLLM:
    """简单的LLM封装类，用于演示基本概念。"""

    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        """初始化LLM模型。

        Args:
            model_name: 模型名称
        """
        self.model_name = model_name
        self.api_key = os.environ.get("OPENAI_API_KEY", "")
        self.history: List[Dict[str, str]] = []

    def add_message(self, role: str, content: str) -> None:
        """添加消息到历史记录。

        Args:
            role: 角色（'user', 'assistant', 或 'system'）
            content: 消息内容
        """
        self.history.append({"role": role, "content": content})

    def get_completion(self, prompt: str, temperature: float = 0.7) -> Optional[str]:
        """获取LLM的回复。

        Args:
            prompt: 用户输入的提示
            temperature: 温度参数，控制输出的随机性

        Returns:
            模型的回复，如果API密钥未设置则返回None
        """
        if not self.api_key:
            print("警告: 未设置API密钥，请设置OPENAI_API_KEY环境变量")
            return None

        # 在实际应用中，这里会调用OpenAI API
        # 这里仅作为示例，返回一个模拟的回复
        self.add_message("user", prompt)
        response = f"这是{self.model_name}对'{prompt}'的模拟回复。实际使用时会调用API获取真实回复。"
        self.add_message("assistant", response)
        return response

    def clear_history(self) -> None:
        """清除对话历史。"""
        self.history = []


def demonstrate_llm_usage() -> None:
    """演示LLM的基本用法。"""
    llm = SimpleLLM()
    
    # 设置系统提示
    llm.add_message("system", "你是一个乐于助人的AI助手。")
    
    # 获取回复
    response = llm.get_completion("请解释什么是大型语言模型？")
    print("\nLLM回复:")
    print(response)
    
    # 查看历史记录
    print("\n对话历史:")
    for msg in llm.history:
        print(f"{msg['role']}: {msg['content']}")


if __name__ == "__main__":
    demonstrate_llm_usage()