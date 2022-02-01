from flask import request, jsonify

from app import app
from constants import HttpStatus, ResponseData
from service.DataService import getData, saveData


@app.route('/all', methods=['GET'])
def getAllData():
    try:
        if request.method == 'GET':
            data = getData("SELECT * FROM User")
            app.logger.info('[UserController][getAllData] getting all the data')
            response = jsonify(data)
            response.status_code = HttpStatus.OK
            return response
        else:
            ResponseData.construct['success'] = False
            ResponseData.construct['error'] = 'Something happened. Please try again!'
            app.logger.error('[UserController][getAllData] request failed')
            response = jsonify(ResponseData.construct)
            response.status_code = HttpStatus.BAD_REQUEST
            return response
    except Exception as e:
        print(e)
        app.logger.error('[UserController][getAllData] an exception occurred: ', e)
        ResponseData.construct['success'] = False
        ResponseData.construct['error'] = str(e)
        response.status_code = HttpStatus.BAD_REQUEST
        response = jsonify(ResponseData.construct)
        response.status_code = HttpStatus.BAD_REQUEST
        return response


@app.route('/add', methods=['POST'])
def saveDatas():
    try:
        json = request.json
        email = json['email']
        password = json['password']
        username = json['username']
        if email and password and username and request.method == 'POST':
            app.logger.info('[UserController][saveDatas] inserting user data')
            sql = "INSERT INTO user(email, password, username) VALUES( %s, %s, %s)"
            data = (email, password, username)
            response = saveData(sql, data)
            response = jsonify(response)
            response.status_code = HttpStatus.OK
            return response
        else:
            ResponseData.construct['success'] = False
            ResponseData.construct['error'] = 'Something happened. Please try again!'
            app.logger.error('[UserController][saveDatas] request failed')
            response = jsonify(ResponseData.construct)
            response.status_code = HttpStatus.BAD_REQUEST
            return response
    except Exception as e:
        print(e)
        ResponseData.construct['success'] = False
        ResponseData.construct['error'] = str(e)
        app.logger.error('[UserController][saveDatas] an exception occurred: ', e)
        response = jsonify(ResponseData.construct)
        response.status_code = HttpStatus.BAD_REQUEST
        return response


@app.route('/update/<string:id>', methods=['PUT'])
def updateData(id):
    try:
        json = request.json
        email = json['email']
        password = json['password']
        username = json['username']
        if email and password and username and request.method == 'PUT':
            sql = "UPDATE user SET email = %s, password = %s, username = %s WHERE username = %s"
            app.logger.info('[UserController][updateData] updating user data of the user ', id)
            data = (email, password, username, id)
            response = saveData(sql, data)
            response = jsonify(response)
            response.status_code = HttpStatus.OK
            return response
        else:
            ResponseData.construct['success'] = False
            ResponseData.construct['error'] = 'Something happened. Please try again!'
            app.logger.error('[UserController][updateData] request failed')
            response = jsonify(ResponseData.construct)
            response.status_code = HttpStatus.BAD_REQUEST
            return response
    except Exception as e:
        print(e)
        ResponseData.construct['success'] = False
        ResponseData.construct['error'] = str(e)
        app.logger.error('[UserController][updateData] an exception occurred: ', e)
        response = jsonify(ResponseData.construct)
        response.status_code = HttpStatus.BAD_REQUEST
        return response


@app.route('/delete/<string:id>', methods=['DELETE'])
def deleteData(id):
    try:
        if request.method == 'DELETE':
            app.logger.info('[UserController][deleteData] deleting user data of ', id)
            sql = "DELETE FROM user WHERE username = %s"
            response = saveData(sql, id)
            response = jsonify(response)
            response.status_code = HttpStatus.OK
            return response
        else:
            ResponseData.construct['success'] = False
            ResponseData.construct['error'] = 'Something happened. Please try again!'
            app.logger.error('[UserController][deleteData] request failed')
            response = jsonify(ResponseData.construct)
            response.status_code = HttpStatus.BAD_REQUEST
            return response
    except Exception as e:
        print(e)
        ResponseData.construct['success'] = False
        ResponseData.construct['error'] = str(e)
        app.logger.error('[UserController][deleteData] an exception occurred: ', e)
        response = jsonify(ResponseData.construct)
        response.status_code = HttpStatus.BAD_REQUEST
        return response
