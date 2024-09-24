import tkinter as tk
import logging
from tkinter import scrolledtext, messagebox
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from chat_database import ChatDatabase
from config import DB_URL

logging.basicConfig(filename='chatbot_app.log', level=logging.ERROR)


class ChatbotApp:
    def __init__(self, root: tk.Tk, model_name: str = "llama3.1", window_title: str = "AI-ChatBot App", window_size: str = "600x500"):
        """
        Initialize the chatbot application, setting up the GUI components.

        Args:
            root (tk.Tk): The root window object for the Tkinter application.
        """
        self.root = root
        self.model_name = model_name
        self.window_title = window_title
        self.window_size = window_size
        self.root.title(self.window_title)
        self.root.geometry(self.window_size)
        self.context = "" # context can be managed to include chat history
        self.current_session = 1  # Default session
        self.session_data = {}  # Store chat data for each session

        self.db = ChatDatabase(DB_URL)

        try:
            self.init_llm_model()
            self.create_widgets()
            self.display_welcome_message()
            self.load_chat_history() 
        except Exception as e:
            self.display_message("System", f"Error initializing application: {e}", "system")
            self.root.after(1000, self.root.quit)  # Close the application after 1 second


    def init_llm_model(self):
        template = """
        Answer the question below.
        Here is the conversation history: {context}
        Question: {question}
        Answer:
        """
        try:
            self.llm_model = OllamaLLM(model=self.model_name) 
            self.prompt = ChatPromptTemplate.from_template(template)
            self.chain = self.prompt | self.llm_model
        except Exception as e:
            logging.error(f"Failed to initialize the model: {e}")
            raise RuntimeError(f"Failed to initialize the model: {e}")
        

    def create_widgets(self):
        """Create and arrange the GUI widgets in the application."""
        # Add a scrolled text widget to display chat history
        self.chat_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state='disabled')
        self.chat_display.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Add a text entry box for user input
        self.user_input = tk.Entry(self.root, width=50)
        self.user_input.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.user_input.bind("<Return>", self.send_message_llm)  # Allow pressing Enter to send

        # Define text tags for styling "You" and "Bot" messages
        self.chat_display.tag_configure("you", foreground="blue", font=("Arial", 10, "bold"))
        self.chat_display.tag_configure("user_message", foreground="black", font=("Arial", 10))
        self.chat_display.tag_configure("bot", foreground="green", font=("Arial", 10, "bold"))
        self.chat_display.tag_configure("bot_message", foreground="black", font=("Arial", 10, "italic"))

        # Add a send button
        send_button = tk.Button(self.root, text="Send", command=self.send_message_llm)
        send_button.grid(row=1, column=1, padx=10, pady=10)

        # Add an exit button
        exit_button = tk.Button(self.root, text="Exit", command=self.exit_program)
        exit_button.grid(row=1, column=2, padx=10, pady=10)

        # Add a clear chat button
        clear_chat_button = tk.Button(self.root, text="Clear Chat", command=self.clear_chat)
        clear_chat_button.grid(row=2, column=3, padx=10, pady=10)

        # Add a clear chat session button
        clear_session_button = tk.Button(self.root, text="Clear Session", command=self.clear_chat_session)
        clear_session_button.grid(row=2, column=0, padx=10, pady=10)

        # Add session buttons
        session_button1 = tk.Button(self.root, text="Session 1", command=lambda: self.switch_session(1))
        session_button1.grid(row=2, column=1, padx=10, pady=10)

        session_button2 = tk.Button(self.root, text="Session 2", command=lambda: self.switch_session(2))
        session_button2.grid(row=2, column=2, padx=10, pady=10)

        # Configure grid row/column weights to make the chat display expandable
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)


    def send_message_test(self, event=None):
        """Handle the event of sending a message from the user."""
        message = self.user_input.get().strip()
        if message:
            self.display_message("You:", message, "you")
            bot_response = self.get_bot_response_test(message)
            self.display_message("Bot:", bot_response, "bot")
            self.user_input.delete(0, tk.END)

            # Close the application if the user types "exit"
            if message.lower() == "exit":
                self.root.quit()


    def exit_program(self, event=None):
        self.root.after(1000, self.root.quit)


    def clear_chat(self):
        """Clear all messages from the chat display."""
        self.chat_display.config(state='normal')
        self.chat_display.delete('1.0', tk.END)
        self.chat_display.config(state='disabled')


    def clear_chat_session(self, event=None):
        """Clear all messages from the chat display."""
        self.chat_display.config(state='normal')
        self.chat_display.delete('1.0', tk.END)  # Clear all text
        self.chat_display.config(state='disabled')  # Disable editing
        self.db.clear_chat_history(self.current_session)


    def switch_session(self, session_number: int):
        """Switch to a different session."""
        self.current_session = session_number
        self.clear_chat()  # Clear the current chat display
        self.load_chat_history()  # Load chat history for the new session
        messagebox.showinfo("Session Change", f"Switched to Session {self.current_session}")


    def load_chat_history(self):
        """Load previous chat history from the database and display it."""
        chat_history = self.db.get_chat_history(self.current_session)
        for entry in chat_history:
            self.display_message(entry.sender, entry.message, "bot" if entry.sender == "Bot" else "you")


    def send_message_llm(self, event=None):
        """Handle the event of sending a message from the user."""
        message = self.user_input.get().strip()
        if message:
            try:
                self.display_message("You", message, "you")
                self.db.save_message("User", message, self.current_session)
                bot_response = self.get_bot_response_llm(message)
                self.display_message("Bot", bot_response, "bot")
                self.db.save_message("Bot", bot_response, self.current_session)
            except Exception as e:
                self.display_message("System", f"Error generating response: {e}", "system")
                self.root.after(1000, self.root.quit)  
            self.user_input.delete(0, tk.END)
            if message.lower() == "exit":
                self.root.quit()


    def display_welcome_message(self):
        """Display a welcome message when the application starts."""
        welcome_message = f"Welcome to the AI-ChatBot, powered by the {self.model_name} model! How can I assist you today?"
        self.display_message("Bot", welcome_message, "bot")


    def display_message(self, sender: str, message: str, tag:str):
        """
        Display a message in the chat display area.

        Args:
            sender (str): The sender of the message (e.g., "You" or "Bot").
            message (str): The message content to display.
            tag (str): The tag to apply to the message for styling.
        """
        self.chat_display.config(state='normal')

        if sender == "Bot" and tag:
            self.chat_display.insert(tk.END, f"{sender}: ", tag)
            self.chat_display.insert(tk.END, f"{message}\n", "bot_message")
        elif sender == "You":
            self.chat_display.insert(tk.END, f"{sender}: ", tag)
            self.chat_display.insert(tk.END, f"{message}\n", "user_message")
        else:
            self.chat_display.insert(tk.END, f"{sender}: {message}\n", tag)

        self.chat_display.config(state='disabled')
        self.chat_display.yview(tk.END)


    def get_bot_response_test(self, message: str) -> str:
        """
        Generate a bot response based on the user's message.

        Args:
            message (str): The message input by the user.

        Returns:
            str: The bot's response to the user's message.
        """
        message = message.lower()
        if "hello" in message:
            return "Hello! How can I assist you today?"
        elif "how are you" in message:
            return "I'm just a bot, but I'm functioning as expected!"
        elif "exit" in message:
            return "Goodbye! Ending the chat session."
        else:
            return "I'm sorry, I don't understand that."


    def get_bot_response_llm(self, message:str) -> str:
        """
        Generate a bot response based on the user's message using the LLM model.

        Args:
            message (str): The message input by the user.

        Returns:
            str: The LLM bot's response to the user's message.
        """
        user_input = message.lower()
        try:
            result = self.chain.invoke({"context": self.context, "question": user_input})
            self.context += f"\nUser: {user_input}\nAI: {result}"
            return result
        except Exception as e:
            logging.error(f"Error generating response: {e}")
            return f"Error generating response: {e}"


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotApp(root, model_name="llama3.1")
    root.mainloop()
