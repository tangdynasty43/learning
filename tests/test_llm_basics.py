"""测试LLM基础模块。"""

import os
import unittest
from unittest.mock import patch

from src.my_project.llm_basics import SimpleLLM


class TestSimpleLLM(unittest.TestCase):
    """测试SimpleLLM类。"""

    def setUp(self):
        """测试前的设置。"""
        # 创建一个测试用的LLM实例
        self.llm = SimpleLLM(model_name="test-model")

    def test_initialization(self):
        """测试初始化。"""
        self.assertEqual(self.llm.model_name, "test-model")
        self.assertEqual(self.llm.history, [])

    def test_add_message(self):
        """测试添加消息功能。"""
        self.llm.add_message("user", "Hello")
        self.assertEqual(len(self.llm.history), 1)
        self.assertEqual(self.llm.history[0]["role"], "user")
        self.assertEqual(self.llm.history[0]["content"], "Hello")

    def test_clear_history(self):
        """测试清除历史记录功能。"""
        self.llm.add_message("user", "Hello")
        self.llm.add_message("assistant", "Hi there")
        self.assertEqual(len(self.llm.history), 2)
        
        self.llm.clear_history()
        self.assertEqual(len(self.llm.history), 0)

    @patch.dict(os.environ, {"OPENAI_API_KEY": "fake-api-key"})
    def test_get_completion_with_api_key(self):
        """测试获取回复功能（有API密钥的情况）。"""
        # 重新创建实例以使用模拟的环境变量
        llm = SimpleLLM()
        response = llm.get_completion("Test prompt")
        
        # 验证响应不为None
        self.assertIsNotNone(response)
        
        # 验证历史记录已更新
        self.assertEqual(len(llm.history), 2)
        self.assertEqual(llm.history[0]["role"], "user")
        self.assertEqual(llm.history[0]["content"], "Test prompt")
        self.assertEqual(llm.history[1]["role"], "assistant")

    def test_get_completion_without_api_key(self):
        """测试获取回复功能（无API密钥的情况）。"""
        # 确保API密钥为空
        self.llm.api_key = ""
        
        # 捕获打印输出
        with patch("builtins.print") as mock_print:
            response = self.llm.get_completion("Test prompt")
            
            # 验证警告消息已打印
            mock_print.assert_called_with("警告: 未设置API密钥，请设置OPENAI_API_KEY环境变量")
        
        # 验证响应为None
        self.assertIsNone(response)
        
        # 验证用户消息已添加到历史记录
        self.assertEqual(len(self.llm.history), 1)
        self.assertEqual(self.llm.history[0]["role"], "user")
        self.assertEqual(self.llm.history[0]["content"], "Test prompt")


if __name__ == "__main__":
    unittest.main()