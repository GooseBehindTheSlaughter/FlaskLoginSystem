from database import UserDatabase
import secrets

'''
# makes a random flask secret key
a = secrets.token_hex(32)
print(a)
'''

'''
# Create a user so you can actually login
db = UserDatabase()
db.registerUser("Admin","password")
'''

'''
# Check if your token is valid (use cookie editor to get)
db = UserDatabase()
token = ""
a = db.isValidToken(token)
print(a)
'''