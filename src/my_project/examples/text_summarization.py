"""文本摘要示例，展示如何使用LLM进行文本摘要。"""

import os
from typing import Optional

# 尝试导入openai库
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

from ..utils import load_environment_variables, get_api_key


class TextSummarizer:
    """文本摘要类，使用LLM生成文本摘要。"""

    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        """初始化文本摘要器。

        Args:
            model_name: 使用的模型名称
        """
        # 加载环境变量
        load_environment_variables()
        
        self.model_name = model_name
        self.api_key = get_api_key("OPENAI_API_KEY")
        
        # 检查OpenAI库是否可用
        if not OPENAI_AVAILABLE:
            print("警告: openai库未安装，无法使用OpenAI API")
            print("提示: 可以通过运行'pip install openai>=1.0.0'安装")
    
    def summarize(self, text: str, max_length: int = 150, language: str = "中文") -> Optional[str]:
        """生成文本摘要。

        Args:
            text: 需要摘要的文本
            max_length: 摘要的最大长度（字符数）
            language: 摘要的语言

        Returns:
            生成的摘要，如果API调用失败则返回None
        """
        if not OPENAI_AVAILABLE or not self.api_key:
            print("无法生成摘要：openai库未安装或API密钥未设置")
            return None
        
        # 设置OpenAI API密钥
        openai.api_key = self.api_key
        
        # 构建提示
        prompt = f"""请将以下文本总结为不超过{max_length}个字符的{language}摘要，保留关键信息和主要观点：

{text}

摘要："""
        
        try:
            # 调用OpenAI API
            response = openai.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "你是一个专业的文本摘要助手，善于提取文本的关键信息并生成简洁的摘要。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=max_length // 2,  # 粗略估计token数量
            )
            
            # 提取摘要
            summary = response.choices[0].message.content.strip()
            return summary
            
        except Exception as e:
            print(f"生成摘要时出错: {str(e)}")
            return None
    
    def summarize_mock(self, text: str, max_length: int = 150, language: str = "中文") -> str:
        """生成模拟的文本摘要（当无法使用OpenAI API时）。

        Args:
            text: 需要摘要的文本
            max_length: 摘要的最大长度（字符数）
            language: 摘要的语言

        Returns:
            模拟生成的摘要
        """
        # 简单的摘要生成逻辑：取前几句话
        sentences = text.split(". ")
        short_summary = ". ".join(sentences[:3]) + "."
        
        if len(short_summary) > max_length:
            short_summary = short_summary[:max_length-3] + "..."
        
        return f"[模拟摘要] {short_summary}"


def demonstrate_summarization() -> None:
    """演示文本摘要功能。"""
    # 示例文本
    sample_text = """
    大型语言模型（LLM）是一种基于深度学习的自然语言处理模型，通过在海量文本数据上训练，学习语言的规律和知识。
    这些模型通常基于Transformer架构，使用自注意力机制处理序列数据。LLM可以执行多种任务，如文本生成、翻译、问答和摘要等。
    近年来，随着计算能力的提升和训练数据的增加，LLM的规模和能力显著增长。从早期的BERT、GPT-2到后来的GPT-3、GPT-4、
    LLaMA和Claude等，模型参数从数亿增长到数千亿，性能也不断提升。这些模型展现出了强大的语言理解和生成能力，
    甚至表现出一定程度的推理能力和创造性。然而，LLM也面临着一些挑战，如幻觉（生成虚假信息）、偏见、安全风险等问题。
    未来，研究人员将继续探索如何提高模型的准确性、可解释性和安全性，同时降低训练和推理的计算成本。
    """
    
    # 创建文本摘要器
    summarizer = TextSummarizer()
    
    # 尝试使用OpenAI API生成摘要
    if OPENAI_AVAILABLE and summarizer.api_key:
        print("使用OpenAI API生成摘要...")
        summary = summarizer.summarize(sample_text)
        if summary:
            print("\nOpenAI API生成的摘要:")
            print(summary)
    else:
        print("OpenAI API不可用，使用模拟摘要...")
    
    # 使用模拟方法生成摘要
    mock_summary = summarizer.summarize_mock(sample_text)
    print("\n模拟生成的摘要:")
    print(mock_summary)


if __name__ == "__main__":
    demonstrate_summarization()