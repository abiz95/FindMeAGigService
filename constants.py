import string


class HttpStatus:
    OK = 200
    CREATED = 201
    NOT_FOUND = 404
    BAD_REQUEST = 400


class ResponseData:
    construct = {
        'error': [],
        'success': True
    }


class Queries:
    getQuery: string = "SELECT * FROM User",
    saveQuery = "INSERT INTO user(email, password, username) VALUES( %s, %s, %s)",
    updateQuery = "UPDATE user SET email = %s, password = %s, username = %s WHERE username = %s",
    deleteQuery = "DELETE FROM user WHERE username = %s"
