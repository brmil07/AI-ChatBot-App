from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

# Create a declarative base class for the database models
Base = declarative_base()

# Define the ChatHistory model (a table for storing chat messages)
class ChatHistory(Base):
    __tablename__ = 'chat_history'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    sender = Column(String, nullable=False)        # "User" or "Bot"
    message = Column(Text, nullable=False)         # The actual message content
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)  # Timestamp of the message