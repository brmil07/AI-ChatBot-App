import pytest
import textwrap
import tkinter as tk
from unittest.mock import MagicMock, patch
from AI_ChatBot_GUI import ChatbotApp


class TestChatbotApp:
    @pytest.fixture
    def setup_app(self):
        """Fixture to set up and tear down the ChatbotApp instance."""
        root = tk.Tk()
        app = ChatbotApp(root, model_name="phi3")
        # Mock the user_input to avoid Tkinter-related issues
        app.user_input = MagicMock()
        yield app, root
        root.destroy()

    @patch('AI_ChatBot_GUI.OllamaLLM')
    @patch('AI_ChatBot_GUI.ChatPromptTemplate.from_template')
    def test_init_llm_model(self, mock_from_template, mock_llm, setup_app):
        """Test the initialization of the LLM model."""
        mock_llm.return_value = MagicMock()
        mock_from_template.return_value = MagicMock()
        
        app, _ = setup_app
        app.init_llm_model()
        
        mock_llm.assert_called_once_with(model="phi3")
        
        expected_template = textwrap.dedent("""
            Answer the question below.
            Here is the conversation history: {context}
            Question: {question}
            Answer:
        """).strip()
        
        actual_template = textwrap.dedent(mock_from_template.call_args[0][0]).strip()
        
        assert actual_template == expected_template
        assert app.chain is not None

    def test_display_message(self, setup_app):
        """Test the display_message method."""
        app, _ = setup_app
        app.display_message("You", "Hello", "you")
        app.display_message("Bot", "Hi there!", "bot")
        
        content = app.chat_display.get("1.0", tk.END).strip()
        assert "You: Hello" in content
        assert "Bot: Hi there!" in content

    @patch('AI_ChatBot_GUI.ChatPromptTemplate.from_template')
    @patch('AI_ChatBot_GUI.OllamaLLM')
    def test_get_bot_response_llm(self, mock_llm, mock_from_template, setup_app):
        """Test the get_bot_response_llm method."""
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = "This is a response"
        app, _ = setup_app
        app.chain = mock_chain
        
        response = app.get_bot_response_llm("Hello")
        
        assert response == "This is a response"
        assert "User: hello" in app.context
        assert "AI: This is a response" in app.context

    def test_send_message_llm(self, setup_app):
        """Test the send_message_llm method."""
        app, _ = setup_app
        app.get_bot_response_llm = MagicMock(return_value="Test response")
        app.display_message = MagicMock()
        
        # Simulate user input
        app.user_input.get.return_value = "Hello"
        
        app.send_message_llm()
        
        # Check if display_message was called with the expected arguments
        assert app.display_message.call_count == 2
        app.display_message.assert_any_call("You", "Hello", "you")
        app.display_message.assert_any_call("Bot", "Test response", "bot")
        
        # Check if delete was called once with the expected arguments
        app.user_input.delete.assert_called_once_with(0, tk.END)

    @patch('AI_ChatBot_GUI.ChatbotApp.get_bot_response_test')
    def test_send_message_test(self, mock_get_bot_response_test, setup_app):
        """Test the send_message_test method."""
        mock_get_bot_response_test.return_value = "Test response"
        app, _ = setup_app
        app.display_message = MagicMock()
        
        # Simulate user input
        app.user_input.get.return_value = "Hello"
        
        app.send_message_test()
        
        # Check if display_message was called with the expected arguments
        assert app.display_message.call_count == 2
        app.display_message.assert_any_call("You:", "Hello", "you")
        app.display_message.assert_any_call("Bot:", "Test response", "bot")
        
        # Check if delete was called once with the expected arguments
        app.user_input.delete.assert_called_once_with(0, tk.END)
