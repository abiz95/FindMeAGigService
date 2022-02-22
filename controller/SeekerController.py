from flask import request, jsonify

from service.SeekerService import *


@app.route('/seeker_login', methods=['POST'])
def seeker_login():
    try:
        req_params = request.json
        username = str(req_params['seekerEmail']).strip()
        password = str(req_params['seekerPassword']).strip()
        if username and password:
            app.logger.info('[SeekerController][seeker_login] Authenticating seeker')
            login_response = SeekerModule.seeker_authentication(username)  # used class method
            if login_response:
                user_details = login_response[0]  # only one row returned from result_set list of dict, convert row2dict
                if user_details.get('seekerEmail') == password:  # used get() of dict to access value
                    login_response = jsonify(login_response)
                    login_response.status_code = HttpStatus.OK
                    return login_response
                else:
                    app.logger.error('[SeekerController][seeker_login] Incorrect Password! ')
                    ResponseData.construct['success'] = False
                    ResponseData.construct['error'] = 'Incorrect Password!'
                    login_response = jsonify(ResponseData.construct)
                    login_response.status_code = HttpStatus.UNAUTHORIZED
                    return login_response
            else:
                app.logger.error('[SeekerController][seeker_login] Invalid User! ')
                ResponseData.construct['success'] = False
                ResponseData.construct['error'] = 'Invalid User!'
                login_response = jsonify(ResponseData.construct)
                login_response.status_code = HttpStatus.UNAUTHORIZED
                return login_response

        # either user haven't entered username or password  or method not POST (write appropriate error and log msg)
        else:
            app.logger.error('[SeekerController][seeker_login] *Empty data either username or password')
            ResponseData.construct['success'] = False
            ResponseData.construct['error'] = ' *Empty data either username or password '
            login_response = jsonify(ResponseData.construct)
            login_response.status_code = HttpStatus.BAD_REQUEST
            return login_response
    except Exception as e:
        print(e)
        ResponseData.construct['success'] = False
        ResponseData.construct['error'] = str(e)
        app.logger.error('[SeekerController][saveDatas] an exception occurred: ', e)
        login_response = jsonify(ResponseData.construct)
        login_response.status_code = HttpStatus.BAD_REQUEST
        return login_response


@app.route('/seeker_signup', methods=['POST'])
def seeker_signup():
    try:
        req_params = request.json
        username = str(req_params['seekerEmail']).strip()
        username_exist = get_data_where('SELECT * FROM gigdb.seeker WHERE emailid = %s', username)
        if not username_exist:
            if req_params['seekerEmail'] and req_params['seekerPassword'] and req_params['seekerFirstName'] and \
                    req_params['seekerPhoneNumber']:
                signup_response = SeekerModule.seeker_registration(req_params)  # calling seeker_registration()
                signup_response = jsonify(signup_response)
                signup_response.status_code = HttpStatus.OK
                return signup_response
            else:
                app.logger.error('[SeekerController][seeker_signup] * Please fill all Mandatory Fields!')
                ResponseData.construct['success'] = False
                ResponseData.construct['error'] = '* Please fill all Mandatory Fields!'
                signup_response = jsonify(ResponseData.construct)
                signup_response.status_code = HttpStatus.BAD_REQUEST
                return signup_response
        else:
            app.logger.error('[SeekerController][seeker_signup] * Username exists!!!')
            ResponseData.construct['success'] = False
            ResponseData.construct['error'] = '* Username exists!!!'
            signup_response = jsonify(ResponseData.construct)
            signup_response.status_code = HttpStatus.BAD_REQUEST
            return signup_response
    except Exception as e:
        print(e)
        ResponseData.construct['success'] = False
        ResponseData.construct['error'] = str(e)
        app.logger.error('[SeekerController][saveDatas] an exception occurred: ', e)
        signup_response = jsonify(ResponseData.construct)
        signup_response.status_code = HttpStatus.BAD_REQUEST
        return signup_response


@app.route('/seeker_portfolio_insert/<string:fnid>', methods=['POST'])
def seeker_portfolio_insert(fnid: str):
    try:
        req_params = request.json
        portfolio_response = {}
        if fnid == 'about':
            portfolio_response = SeekerModule.portfolio_insert(req_params)
        elif fnid == 'education':
            portfolio_response = SeekerModule.insert_education(req_params)
        elif fnid == 'experience':
            portfolio_response = SeekerModule.insert_experience(req_params)
        elif fnid == 'certification':
            portfolio_response = SeekerModule.insert_certification(req_params)
        portfolio_response = jsonify(portfolio_response)
        portfolio_response.status_code = HttpStatus.OK
        return portfolio_response
    except Exception as e:
        print(e)
        ResponseData.construct['success'] = False
        ResponseData.construct['error'] = str(e)
        app.logger.error('[SeekerController][saveDatas] an exception occurred: ', e)
        portfolio_response = jsonify(ResponseData.construct)
        portfolio_response.status_code = HttpStatus.BAD_REQUEST
        return portfolio_response


@app.route('/seeker_portfolio_view/<string:fnid>/<string:sid>', methods=['GET'])
def seeker_portfolio_view(fnid: str, sid: int):
    try:
        portfolio_response = SeekerModule.portfolio_view(fnid, sid)
        portfolio_response = jsonify(portfolio_response)
        portfolio_response.status_code = HttpStatus.OK
        return portfolio_response
    except Exception as e:
        print(e)
        ResponseData.construct['success'] = False
        ResponseData.construct['error'] = str(e)
        app.logger.error('[SeekerController][saveDatas] an exception occurred: ', e)
        portfolio_response = jsonify(ResponseData.construct)
        portfolio_response.status_code = HttpStatus.BAD_REQUEST
        return portfolio_response


@app.route('/seeker_send_proposal', methods=['POST'])
def seeker_send_proposal():
    try:
        req_params = request.json  # gid, pid, sid message(paid user)
        proposal_response = SeekerModule.send_proposal(req_params)
        return proposal_response
    except Exception as e:
        print(e)
        ResponseData.construct['success'] = False
        ResponseData.construct['error'] = str(e)
        app.logger.error('[SeekerController][saveDatas] an exception occurred: ', e)
        proposal_response = jsonify(ResponseData.construct)
        proposal_response.status_code = HttpStatus.BAD_REQUEST
        return proposal_response


@app.route('/seeker_portfolio_update', methods=['PUT'])
def seeker_portfolio_update():
    try:
        req_params = request.json
        portfolio_response = SeekerModule.portfolio_update(req_params)
        portfolio_response = jsonify(portfolio_response)
        portfolio_response.status_code = HttpStatus.OK
        return portfolio_response
    except Exception as e:
        print(e)
        ResponseData.construct['success'] = False
        ResponseData.construct['error'] = str(e)
        app.logger.error('[SeekerController][saveDatas] an exception occurred: ', e)
        portfolio_response = jsonify(ResponseData.construct)
        portfolio_response.status_code = HttpStatus.BAD_REQUEST
        return portfolio_response


@app.route('/seeker_list_of_openings', methods=['POST'])
def seeker_list_of_openings():
    try:
        req_params = request.json
        list_response = SeekerModule.list_of_openings(req_params)
        if list_response:
            list_response = jsonify(list_response)
            list_response.status_code = HttpStatus.OK
            return list_response
        else:
            app.logger.error('[SeekerController][seeker_list_of_openings] * No gigs found!!!')
            ResponseData.construct['success'] = False
            ResponseData.construct['error'] = '* No gigs found!!!'
            list_response = jsonify(ResponseData.construct)
            list_response.status_code = HttpStatus.BAD_REQUEST
            return list_response
    except Exception as e:
        print(e)
        ResponseData.construct['success'] = False
        ResponseData.construct['error'] = str(e)
        app.logger.error('[SeekerController][saveDatas] an exception occurred: ', e)
        list_response = jsonify(ResponseData.construct)
        list_response.status_code = HttpStatus.BAD_REQUEST
        return list_response


@app.route('/seeker_view_gig_details', methods=['POST'])
def seeker_view_gig_details():
    try:
        req_params = request.json  # gets gig id from request (view button)
        view_response = SeekerModule.view_gig_details(req_params)
        if view_response:
            view_response = jsonify(view_response)
            view_response.status_code = HttpStatus.OK
            return view_response
        else:
            app.logger.error('[SeekerController][seeker_view_gig_details] * Gig does not exist!!!')
            ResponseData.construct['success'] = False
            ResponseData.construct['error'] = '* Gig does not exist!!!'
            view_response = jsonify(ResponseData.construct)
            view_response.status_code = HttpStatus.BAD_REQUEST
            return view_response
    except Exception as e:
        print(e)
        ResponseData.construct['success'] = False
        ResponseData.construct['error'] = str(e)
        app.logger.error('[SeekerController][saveDatas] an exception occurred: ', e)
        view_response = jsonify(ResponseData.construct)
        view_response.status_code = HttpStatus.BAD_REQUEST
        return view_response


@app.route('/seeker_search_gigs', methods=['POST'])
def seeker_search_gigs():
    try:
        req_params = request.json  # gets gig id from request
        search_response = SeekerModule.search_gigs(req_params)
        if search_response:
            search_response = jsonify(search_response)
            search_response.status_code = HttpStatus.OK
            return search_response
        else:
            app.logger.error('[SeekerController][seeker_search_gigs] * No gigs found!!!')
            ResponseData.construct['success'] = False
            ResponseData.construct['error'] = '* No gigs found!!!'
            list_response = jsonify(ResponseData.construct)
            list_response.status_code = HttpStatus.BAD_REQUEST
            return list_response
    except Exception as e:
        print(e)
        ResponseData.construct['success'] = False
        ResponseData.construct['error'] = str(e)
        app.logger.error('[SeekerController][saveDatas] an exception occurred: ', e)
        search_response = jsonify(ResponseData.construct)
        search_response.status_code = HttpStatus.BAD_REQUEST
        return search_response


@app.route('/seeker_update_profile', methods=['PUT'])
def seeker_update_profile():
    try:
        req_params = request.json
        app.logger.error('[SeekerController][seeker_update_profile] * Updating Seeker Profile!')
        update_response = SeekerModule.update_profile(req_params)
        update_response = jsonify(update_response)
        update_response.status_code = HttpStatus.OK
        return update_response
    except Exception as e:
        print(e)
        ResponseData.construct['success'] = False
        ResponseData.construct['error'] = str(e)
        app.logger.error('[SeekerController][saveDatas] an exception occurred: ', e)
        update_response = jsonify(ResponseData.construct)
        update_response.status_code = HttpStatus.BAD_REQUEST
        return update_response
