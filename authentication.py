def login(username, password):
    """
    Dummy authentication function.
    For testing, this function returns True if the username equals the password.
    """
    if username and password and username == password:
        return True
    return False

def logout():
    """
    Dummy logout function.
    """
    return True
