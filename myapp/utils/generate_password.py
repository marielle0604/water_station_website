import bcrypt

# Change 'yourpassword' to whatever password you want
password = 'admin123'.encode('utf-8')  # Replace with your desired password
salt = bcrypt.gensalt(rounds=12)
hashed = bcrypt.hashpw(password, salt)

print("Your password hash:")
print(hashed.decode('utf-8'))