import tkinter as tk
from tkinter import scrolledtext

root = tk.Tk()
chat_display = None
user_input = None


def create_chatbot_layout():
    global chat_display, user_input, root

    # Set the title of the main window
    root.title("AI-ChatBot")
    # Set the size of the window
    root.geometry("400x500")

    # Add a scrolled text widget to display chat history
    chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled')
    chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    # Add a text entry box for user input
    user_input = tk.Entry(root, width=50)
    user_input.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    # Add a send button
    send_button = tk.Button(root, text="Send", command=send_message)
    send_button.grid(row=1, column=1, padx=10, pady=10)

    # Configure grid row/column weights to make the chat display expandable
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Start the main event loop
    root.mainloop()


def send_message():
    global chat_display, user_input, root

    message = user_input.get()
    if message.strip() != "":
        chat_display.config(state='normal')
        chat_display.insert(tk.END, "You: " + message + "\n")
        
        # Get bot's response
        bot_response = get_bot_response_test(message)
        chat_display.insert(tk.END, "Bot: " + bot_response + "\n\n")
        
        chat_display.config(state='disabled')
        chat_display.yview(tk.END)
        user_input.delete(0, tk.END)

        # Close the application if the user types "exit"
        if "exit" in message.lower():
            root.destroy()


# Function to generate a bot response
def get_bot_response_test(message:str) -> str:
    """
    Processes the user's message and generates a corresponding response from the bot.

    Args:
        message (str): The message input by the user, typically a question or statement.

    Returns:
        str: The bot's response to the user's message. This could be a greeting, a response 
             to a common question, or a message indicating that the bot doesn't understand 
             the input.
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
    create_chatbot_layout() 
