# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_models import ChatHistory, Base  # Import the ChatHistory model and Base from models.py

class ChatDatabase:
    def __init__(self, db_name: str = 'sqlite:///chat_history.db'):
        """
        Initialize the database connection and create the table if it doesn't exist.
        
        Args:
            db_name (str): The URI of the SQLite database.
        """
        # Define the SQLite database engine
        self.engine = create_engine(db_name)

        # Create the table if it doesn't exist
        Base.metadata.create_all(self.engine)

        # Set up the session (this allows us to interact with the database)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def save_message(self, sender: str, message: str):
        """
        Save a chat message to the database.
        
        Args:
            sender (str): The sender of the message ("User" or "Bot").
            message (str): The message content to save.
        """
        chat_message = ChatHistory(sender=sender, message=message)
        self.session.add(chat_message)  # Add the message to the current session
        self.session.commit()           # Commit (save) the changes

    def get_chat_history(self):
        """
        Retrieve the full chat history from the database.
        
        Returns:
            list: A list of all chat messages stored in the database.
        """
        return self.session.query(ChatHistory).all()

    def clear_chat_history(self):
        """
        Clear the chat history from the database.
        """
        self.session.query(ChatHistory).delete()
        self.session.commit()
