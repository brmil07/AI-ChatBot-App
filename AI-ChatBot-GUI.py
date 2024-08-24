import tkinter as tk
from tkinter import scrolledtext


class ChatbotApp:
    def __init__(self, root: tk.Tk):
        """
        Initialize the chatbot application, setting up the GUI components.

        Args:
            root (tk.Tk): The root window object for the Tkinter application.
        """
        self.root = root
        self.root.title("AI-ChatBot")
        self.root.geometry("500x400")

        self.create_widgets()
        self.display_welcome_message()


    def create_widgets(self):
        """Create and arrange the GUI widgets in the application."""
        # Add a scrolled text widget to display chat history
        self.chat_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state='disabled')
        self.chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Add a text entry box for user input
        self.user_input = tk.Entry(self.root, width=50)
        self.user_input.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.user_input.bind("<Return>", self.send_message)  # Allow pressing Enter to send

        # Add a send button
        send_button = tk.Button(self.root, text="Send", command=self.send_message)
        send_button.grid(row=1, column=1, padx=10, pady=10)

        # Configure grid row/column weights to make the chat display expandable
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)


    def send_message(self, event=None):
        """Handle the event of sending a message from the user."""
        message = self.user_input.get().strip()
        if message:
            self.display_message("You", message)
            bot_response = self.get_bot_response_test(message)
            self.display_message("Bot", bot_response)
            self.user_input.delete(0, tk.END)

            # Close the application if the user types "exit"
            if "exit" in message.lower():
                self.root.quit()


    def display_welcome_message(self):
        """Display a welcome message when the application starts."""
        welcome_message = "Welcome to the AI-ChatBot! How can I assist you today?"
        self.display_message("Bot", welcome_message)


    def display_message(self, sender: str, message: str):
        """
        Display a message in the chat display area.

        Args:
            sender (str): The sender of the message (e.g., "You" or "Bot").
            message (str): The message content to display.
        """
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, f"{sender}: {message}\n")
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


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotApp(root)
    root.mainloop()
