"""LLM学习练习模块，提供实践任务。"""

from typing import List, Dict, Any


class LLMExercise:
    """LLM练习类，包含各种练习任务。"""

    @staticmethod
    def exercise_1() -> Dict[str, Any]:
        """练习1：创建一个简单的提示工程示例。

        任务：完成以下提示模板，使其能够生成结构化的回复
        
        Returns:
            包含练习描述和提示模板的字典
        """
        return {
            "title": "提示工程基础",
            "description": "修改下面的提示模板，使其能够生成结构化的回复",
            "template": """
            你是一个专业的{领域}专家。请针对