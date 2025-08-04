"""问答系统示例，展示如何使用LLM构建简单的问答系统。"""

import os
from typing import List, Dict, Any, Optional, Tuple

# 尝试导入openai库
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

from ..utils import load_environment_variables, get_api_key


class SimpleQASystem:
    """简单的问答系统，使用LLM回答问题。"""

    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        """初始化问答系统。

        Args:
            model_name: 使用的模型名称
        """
        # 加载环境变量
        load_environment_variables()
        
        self.model_name = model_name
        self.api_key = get_api_key("OPENAI_API_KEY")
        self.knowledge_base: List[str] = []
        
        # 检查OpenAI库是否可用
        if not OPENAI_AVAILABLE:
            print("警告: openai库未安装，无法使用OpenAI API")
            print("提示: 可以通过运行'pip install openai>=1.0.0'安装")
    
    def add_knowledge(self, text: str) -> None:
        """添加知识到知识库。

        Args:
            text: 要添加的知识文本
        """
        self.knowledge_base.append(text)
        print(f"已添加知识到知识库（当前共{len(self.knowledge_base)}条）")
    
    def get_relevant_knowledge(self, question: str) -> str:
        """获取与问题相关的知识。

        在实际应用中，这里可以使用向量数据库和嵌入进行相似度搜索。
        这里使用简单的关键词匹配作为示例。

        Args:
            question: 用户问题

        Returns:
            与问题相关的知识文本
        """
        if not self.knowledge_base:
            return ""
        
        # 简单的关键词匹配（在实际应用中应使用更复杂的检索方法）
        question_words = set(question.lower().split())
        relevant_texts = []
        
        for text in self.knowledge_base:
            text_words = set(text.lower().split())
            # 计算问题和知识文本的词汇重叠度
            overlap = len(question_words.intersection(text_words))
            if overlap > 0:
                relevant_texts.append((text, overlap))
        
        # 按相关性排序
        relevant_texts.sort(key=lambda x: x[1], reverse=True)
        
        # 返回最相关的知识（最多3条）
        result = "\n\n".join([text for text, _ in relevant_texts[:3]])
        return result
    
    def answer_question(self, question: str) -> Optional[str]:
        """回答问题。

        Args:
            question: 用户问题

        Returns:
            回答内容，如果API调用失败则返回None
        """
        if not OPENAI_AVAILABLE or not self.api_key:
            print("无法回答问题：openai库未安装或API密钥未设置")
            return self.answer_question_mock(question)
        
        # 设置OpenAI API密钥
        openai.api_key = self.api_key
        
        # 获取相关知识
        relevant_knowledge = self.get_relevant_knowledge(question)
        
        # 构建提示
        system_prompt = "你是一个知识渊博、乐于助人的AI助手。请根据提供的信息回答问题，如果信息不足，可以使用你的通用知识，但要明确指出哪些是基于提供的信息，哪些是基于你的知识。"
        
        if relevant_knowledge:
            user_prompt = f"""基于以下信息回答问题：

{relevant_knowledge}

问题：{question}"""
        else:
            user_prompt = f"问题：{question}"
        
        try:
            # 调用OpenAI API
            response = openai.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=500,
            )
            
            # 提取回答
            answer = response.choices[0].message.content.strip()
            return answer
            
        except Exception as e:
            print(f"回答问题时出错: {str(e)}")
            return self.answer_question_mock(question)
    
    def answer_question_mock(self, question: str) -> str:
        """生成模拟的问题回答（当无法使用OpenAI API时）。

        Args:
            question: 用户问题

        Returns:
            模拟生成的回答
        """
        # 获取相关知识
        relevant_knowledge = self.get_relevant_knowledge(question)
        
        if relevant_knowledge:
            return f"[模拟回答] 根据我的知识库，我找到了以下相关信息：\n\n{relevant_knowledge}\n\n这些信息可能有助于回答你的问题：