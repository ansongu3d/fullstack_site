import bcrypt

# hash is used when creating the user
def hash(string):
  return bcrypt.hashpw(string.encode(), bcrypt.gensalt()).decode()

# check is used when user tries to log in
def check(string, hashed_string):
  return bcrypt.checkpw(string.encode(), hashed_string.encode())
