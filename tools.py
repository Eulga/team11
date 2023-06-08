from flask_bcrypt import bcrypt


def checkpassword(inputpw, userpw):
    if bcrypt.checkpw(inputpw.encode("utf-8"), userpw):
        result = True
    else:
        result = False

    return result
