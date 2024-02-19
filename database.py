import sqlite3
import hashlib
import secrets


class UserDatabase:
    def __init__(self,db_name="user_database.db"):
        self.conn = sqlite3.connect(db_name)
        self.createTable()
        pass

    def createTable(self):
        """Attempts to create the user table if it doesnt exist"""
        with self.conn:
            self.conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL, token TEXT NOT NULL)")
        pass

    def registerUser(self,username:str,password:str):
        """Registers the user and returns resut:bool and token:str or none"""

        token = secrets.token_hex(16)
        hashedPassword = self.hashPassword(password)

        # Try to add the user into the database
        with self.conn:
            try:
                self.conn.execute("""
                INSERT INTO users (username, password, token)
                VALUES (?, ?, ?)
                """, (username, hashedPassword, token))
                return True, token
            
            # If the username or token isnt unique
            except sqlite3.IntegrityError:
                return False, None 

    def login(self,username:str, password:str):
        """Tries to log the user in, returns result:bool and token:str or none"""
        hashedPassword = self.hashPassword(password)

        with self.conn:
            cursor = self.conn.execute("""
                SELECT token FROM users 
                WHERE username = ? AND password = ?
                """, (username, hashedPassword))
            result = cursor.fetchone()
        if result:
            return True, result[0]
        else:
            return False, None

    def getUserData(self,token):
        """Returns the userID and username"""
        with self.conn:
            cursor = self.conn.execute("""
                SELECT ID, username FROM users
                WHERE token = ?
                """, (token))
            result = cursor.fetchone()

            if result:
                userID, username = result
                return {"id" : userID, "username": username}
            else:
                return None

    def hashPassword(self,password:str) -> str:
        """Uses sha256 to hash the password"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def isValidToken(self,token:str) -> bool:
        while self.conn:
            cursor = self.conn.execute("""
                SELECT username FROM users
                WHERE token = ?
                """, (token,))
            
            return bool(cursor.fetchone())
            
        pass