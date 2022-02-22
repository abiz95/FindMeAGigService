from flask import request, jsonify

from app import app
from constants import *
from service.ProviderService import *
from datetime import datetime


@app.route('/pLogin', methods=['GET'])
def getProviderLogin():
    try:
        if request.method == 'GET':
            data = get_data_where("SELECT * FROM User where email=%s and password=%s")
            app.logger.info('[UserController][getPUserData] getting user data')
            response = jsonify(data)
            response.status_code = HttpStatus.OK
            return response
        else:
            ResponseData.construct['success'] = False
            ResponseData.construct['error'] = 'Something happened. Please try again!'
            app.logger.error('[UserController][getPUserData] request failed')
            response = jsonify(ResponseData.construct)
            response.status_code = HttpStatus.BAD_REQUEST
            return response
    except Exception as e:
        print(e)
        app.logger.error('[UserController][getPUserData] an exception occurred: ', e)
        ResponseData.construct['success'] = False
        ResponseData.construct['error'] = str(e)
        response.status_code = HttpStatus.BAD_REQUEST
        response = jsonify(ResponseData.construct)
        response.status_code = HttpStatus.BAD_REQUEST
        return response


@app.route('/providerUserRegistration', methods=['POST'])
def providerUserRegistration():
    try:
        req_params = request.json
        username_exist = get_data_where('SELECT * FROM gigdb.provider WHERE emailid = %s', req_params['emailid'])
        if not username_exist:
            password_exist = get_data_where('SELECT * FROM gigdb.provider WHERE pswd = %s', req_params['pswd'])
            if not password_exist:
                company = str(req_params['company']).strip()
                emailid = str(req_params['emailid']).strip()
                pswd = str(req_params['pswd']).strip()
                phno = str(req_params['phno']).strip()
                country = str(req_params['country']).strip()
                status= 'A'
                now = datetime.now()
                data = (company, emailid, pswd, phno, country, status, now, now)
                if req_params['company'] and req_params['emailid'] and req_params['pswd'] and  req_params['phno'] and req_params['country']:
                    signup_response = provider_user_registration(data)  # calling provider_registration()
                    signup_response = jsonify(signup_response)
                    signup_response.status_code = HttpStatus.OK
                    return signup_response
                else:
                    app.logger.error('[providerController][provider_user_registration] * Please fill all Mandatory Fields!')
                    ResponseData.construct['success'] = False
                    ResponseData.construct['error'] = '* Please fill all Mandatory Fields!'
                    signup_response = jsonify(ResponseData.construct)
                    signup_response.status_code = HttpStatus.BAD_REQUEST
                    return signup_response
            else:
                app.logger.error('[providerController][providerUserRegistration] * Weak Password!!!')
                ResponseData.construct['success'] = False
                ResponseData.construct['error'] = '* Weak Password!!!'
                signup_response = jsonify(ResponseData.construct)
                signup_response.status_code = HttpStatus.BAD_REQUEST
                return signup_response
        else:
            app.logger.error('[providerController][providerUserRegistration] * Username exists!!!')
            ResponseData.construct['success'] = False
            ResponseData.construct['error'] = '* Username exists!!!'
            signup_response = jsonify(ResponseData.construct)
            signup_response.status_code = HttpStatus.BAD_REQUEST
            return signup_response
    except Exception as e:
        print(e)
        ResponseData.construct['success'] = False
        ResponseData.construct['error'] = str(e)
        app.logger.error('[providerController][saveDatas] an exception occurred: ', e)
        signup_response = jsonify(ResponseData.construct)
        signup_response.status_code = HttpStatus.BAD_REQUEST
        return signup_response


@app.route('/add_gigs', methods=['POST'])
def add_gigs():
    try:
        req_params = request.json
        if req_params['title'] and req_params['dop'] and req_params['deadline'] and \
                req_params['category'] and req_params['mode'] and req_params['pay'] and \
                req_params['location']:
            app.logger.info('[ProviderController][saveData] inserting new gig details')
            addGigs_response = provider_add_gigs(req_params)  # calling saveDatas to insert new Gig
            addGigs_response = jsonify(addGigs_response)
            addGigs_response.status_code = HttpStatus.OK
            return addGigs_response
        else:
            app.logger.error('[ProviderController][addGigs] * Unable to add this Gig, '
                             'please revalidate the information provided!')
            ResponseData.construct['success'] = False
            ResponseData.construct['error'] = '* Unable to add this Gig, please fill all the required fields!'
            addGigs_response = jsonify(ResponseData.construct)
            addGigs_response.status_code = HttpStatus.BAD_REQUEST
            return addGigs_response
    except Exception as e:
        print(e)
        ResponseData.construct['success'] = False
        ResponseData.construct['error'] = str(e)
        app.logger.error('[ProviderController][saveDatas] an exception occurred: ', e)
        addGigs_response = jsonify(ResponseData.construct)
        addGigs_response.status_code = HttpStatus.BAD_REQUEST
        return addGigs_response


@app.route('/provider_proposal_search', methods=['POST'])
def provider_proposal_search():
    try:
        req_params = request.json
        if req_params['gid']:
            app.logger.info('[ProviderController][get_data_where] Provider searching proposals for a particular GigID')
            sql = "select proposals.gid, proposals.msg, proposals.sid, portfolio.about, portfolio.education, " \
                  "portfolio.position, portfolio.experience, portfolio.skills from gigdb.proposals,gigdb.portfolio " \
                  "where gid = %s and proposals.sid = portfolio.sid"
            data = (req_params['gid'])
            retrieve_gigs_response = get_data_where(sql, data)  # calling get_data_where to retrieve Gig details
            retrieve_gigs_response = jsonify(retrieve_gigs_response)
            retrieve_gigs_response.status_code = HttpStatus.OK
            return retrieve_gigs_response
        else:
            app.logger.error('[ProviderController][providerProposalSearch] * Unable to retrieve Gig details!')
            ResponseData.construct['success'] = False
            ResponseData.construct['error'] = '* Unable to retrieve Gig details, please select a Gig ID from dropdown!'
            retrieve_gigs_response = jsonify(ResponseData.construct)
            retrieve_gigs_response.status_code = HttpStatus.BAD_REQUEST
            return retrieve_gigs_response
    except Exception as e:
        print(e)
        ResponseData.construct['success'] = False
        ResponseData.construct['error'] = str(e)
        app.logger.error('[ProviderController][saveDatas] an exception occurred: ', e)
        retrieve_gigs_response = jsonify(ResponseData.construct)
        retrieve_gigs_response.status_code = HttpStatus.BAD_REQUEST
        return retrieve_gigs_response


@app.route('/provider_proposal_view_portfolio', methods=['POST'])
def provider_proposal_view_portfolio():
    try:
       req_params = request.json
    except Exception as e:
        print(e)
        ResponseData.construct['success'] = False
        ResponseData.construct['error'] = str(e)
        app.logger.error('[ProviderController][saveDatas] an exception occurred: ', e)
        retrieve_gigs_response = jsonify(ResponseData.construct)
        retrieve_gigs_response.status_code = HttpStatus.BAD_REQUEST
        return retrieve_gigs_response
