import bcrypt

class Common:
    @staticmethod
    def hash_password(string: str) -> str:
        """Hash password using bcrypt."""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(string.encode('utf-8'), salt)
        return hashed.decode('utf-8')