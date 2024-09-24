from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_models import ChatHistory, Base 
from config import DB_URL

class ChatDatabase:
    def __init__(self, db_name: str = DB_URL):
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
        self.Session = sessionmaker(bind=self.engine)


    def get_table_name(self, session_number: int):
        """Generate the table name for a specific session."""
        return f'chat_history_{session_number}'


    def save_message(self, sender: str, message: str, session_number:int):
        """
        Save a chat message to the database.
        
        Args:
            sender (str): The sender of the message ("User" or "Bot").
            message (str): The message content to save.
        """
        session = self.Session()
        try:
            chat_message = ChatHistory(sender=sender, message=message, session_id=session_number)
            session.add(chat_message)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error saving message: {e}")
        finally:
            session.close()
            

    def get_chat_history(self, session_number:int):
        """
        Retrieve the full chat history from the database.
        
        Returns:
            list: A list of all chat messages stored in the database.
        """
        self.session = self.Session()
        try:
            chat_history = self.session.query(ChatHistory).filter(ChatHistory.session_id == session_number).all()
            return chat_history
        except Exception as e:
            print(f"Error retrieving chat history: {e}")
            return []
        finally:
            self.session.close()

    
    def clear_chat_history(self, session_number:int):
        """
        Clear the chat history from the database.
        """
        session = self.Session()
        try:
            self.session.query(ChatHistory).filter(ChatHistory.session_id == session_number).delete()
            session.commit()
        except Exception as e:
            self.session.rollback()
            print(f"Error clearing chat history: {e}")
        finally:
            self.session.close()  # Ensure the session is closed