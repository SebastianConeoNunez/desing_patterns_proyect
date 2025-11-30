from abc import ABC, abstractmethod


class IDatabaseConnection(ABC):
    """ Interface for database connection.""" 
    
    @abstractmethod
    def connect(self) -> None:
        """ Method to connect to the database."""