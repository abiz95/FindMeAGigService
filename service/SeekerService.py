from flask import jsonify

from service.DataService import *
from datetime import datetime
from app import app
from constants import *


class SeekerModule:

    @staticmethod
    def seeker_authentication(username):
        sqlquery = "SELECT * FROM gigdb.seeker WHERE emailid = %s"
        seeker_response = get_data_where(sqlquery, username)
        return seeker_response

    @classmethod
    def seeker_registration(cls, req_params):
        username = str(req_params['seekerEmail']).strip()
        password = str(req_params['seekerPassword']).strip()
        firstname = str(req_params['seekerFirstName']).strip()
        lastname = str(req_params['seekerLastName']).strip()
        phone = str(req_params['seekerPhoneNumber']).strip()
        country = str(req_params['seekerCountry']).strip()
        securityq = str(req_params['seekerSecurityQuestion']).strip()
        securitya = str(req_params['seekerSecurityQuestionAnswer']).strip()
        gender = str(req_params['seekerGender']).strip()
        cre_rec_ts = upd_rec_ts = plan_cre_ts = datetime.now()
        data = (username, password, firstname, lastname, phone, country, 'freetier', plan_cre_ts, 'A', 'A', cre_rec_ts,
                upd_rec_ts, securityq, securitya, req_params['seekerDOB'], gender)
        app.logger.info('[SeekerModule][seeker_registration] Inserting New seeker')
        sqlquery = "insert into gigdb.seeker( emailid, pswd, fname, lname, phno, country, plan, plan_cre_ts, " \
                   "planstatus, userstatus, cre_rec_ts, upd_rec_ts, securityq, securitya, dob, gender) values(%s," \
                   "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s); "
        commit_query(sqlquery, data)
        sqlquery = "select sid, fname, lname, emailid from gigdb.seeker where emailid = %s"
        seeker_response = get_data_where(sqlquery, username)
        return seeker_response

    @staticmethod
    def insert_education(req_params):
        sid = str(req_params['sid']).strip()
        course = str(req_params['seekerEducationCourse']).strip()
        course_title = str(req_params['seekerEducationCourseTitle']).strip()
        university = str(req_params['seekerEducationUniversity']).strip()
        from_date = str(req_params['seekerEducationStartDate']).strip()
        to_date = str(req_params['seekerEducationLastDate']).strip()
        cre_rec_ts = upd_rec_ts = datetime.now()
        data = (sid, course, course_title, university, from_date, to_date, cre_rec_ts, upd_rec_ts)
        sqlquery = "insert into gigdb.education (sid, course, course_title, university, from_date, to_date, " \
                   "cre_rec_ts, upd_rec_ts) values (%s,%s,%s,%s,%s,%s,%s,%s)"
        seeker_response = commit_query(sqlquery, data)
        return seeker_response

    @staticmethod
    def insert_experience(req_params):
        sid = str(req_params['sid']).strip()
        job_title = str(req_params['seekerExperienceJobTitle']).strip()
        company = str(req_params['seekerExperienceCompany']).strip()
        location = str(req_params['seekerExperienceLocation']).strip()
        country = str(req_params['seekerExperienceCountry']).strip()
        from_date = str(req_params['seekerExperienceStartDate']).strip()
        to_date = str(req_params['seekerExperienceLastDate']).strip()
        cre_rec_ts = upd_rec_ts = datetime.now()
        data = (sid, job_title, company, location, country, from_date, to_date, cre_rec_ts, upd_rec_ts)
        sqlquery = "insert into gigdb.experience ( sid, job_title, company, location, country, from_date, to_date, " \
                   "cre_rec_ts, upd_rec_ts ) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        seeker_response = commit_query(sqlquery, data)
        return seeker_response

    @staticmethod
    def insert_certification(req_params):
        sid = str(req_params['sid']).strip()
        title = str(req_params['seekerCertificateTitle']).strip()
        from_date = str(req_params['seekerCertificateStartDate']).strip()
        to_date = str(req_params['seekerCertificateEndDate']).strip()
        cre_rec_ts = upd_rec_ts = datetime.now()
        data = (sid, title, from_date, to_date, cre_rec_ts, upd_rec_ts)
        sqlquery = " insert into gigdb.certification (sid, title, from_date, to_date, cre_rec_ts, upd_rec_ts) values " \
                   "(%s,%s,%s,%s,%s,%s)"
        seeker_response = commit_query(sqlquery, data)
        return seeker_response

    @classmethod
    def portfolio_insert(cls, req_params):
        cre_rec_ts = upd_rec_ts = datetime.now()
        data = (str(req_params['sid']).strip(), str(req_params['about']).strip(), str(req_params['skills']).strip(),
                cre_rec_ts, upd_rec_ts)
        app.logger.error('[SeekerController][seeker_portfolio_insert] * Adding portfolio details!')
        sqlquery = "insert into gigdb.portfolio( sid, about, position, skills, cre_rec_ts, upd_rec_ts) " \
                   "values (%s,%s,%s,%s,%s,%s)"
        seeker_response = commit_query(sqlquery, data)
        return seeker_response

    @staticmethod
    def portfolio_view(fnid, sid):
        sqlquery = ""
        if fnid == 'about':
            sqlquery = "select sid, about, skills from gigdb.portfolio where sid = %s"
        elif fnid == 'education':
            sqlquery = "select sid, course, course_title, university, from_date, to_date from gigdb.education " \
                       "where sid = %s"
        elif fnid == 'experience':
            sqlquery = "select sid, job_title, company, location, country, from_date, to_date from gigdb.experience " \
                       "where sid = %s"
        elif fnid == 'certification':
            sqlquery = "select sid, title, from_date, to_date from gigdb.certification where sid = %s"
        seeker_response = get_data_where(sqlquery, sid)
        return seeker_response

    @classmethod
    def portfolio_update(cls, req_params):
        upd_rec_ts = datetime.now()
        data = (str(req_params['about']).strip(), str(req_params['position']).strip(),
                str(req_params['skills']).strip(), upd_rec_ts, str(req_params['sid']).strip())
        app.logger.error('[SeekerController][seeker_portfolio_insert] * Updating portfolio details!')
        sqlquery = "update gigdb.portfolio set about = %s, position = %s, skills = %s, upd_rec_ts = %s " \
                   "where portfolio.sid = %s"
        seeker_response = commit_query(sqlquery, data)
        return seeker_response

    @staticmethod
    def list_of_openings(req_params):
        app.logger.error(
            '[SeekerController][seeker_list_of_openings] * Listing all openings that match skills of logged in seeker!')
        skill_response = get_data_where('select portfolio.skills from gigdb.portfolio where portfolio.sid = %s',
                                        str(req_params['sid']).strip())
        skill_dict = skill_response[0]  # list indices must be integers or slices, not str X skill_response['skills'] X
        skill_str = skill_dict['skills']
        skill_list = skill_str.split(",")
        skill_list_stripped = []
        for skill in skill_list:
            skill = str(skill).strip()
            skill_list_stripped.append(skill)
        #gig_list = tuple(gig_list)
        data = (skill_list_stripped, skill_list_stripped)
        sqlquery = "SELECT gigs.gid,gigs.title, gigs.dop, gigs.deadline, gigs.category, gigs.tags, gigs.pay " \
                   "FROM gigdb.gigs where gigs.gigstatus = 'A' and ( gigs.category in %s or gigs.tags in %s ) " \
                   "order by gigs.dop DESC "
        seeker_response = get_data_where(sqlquery, data)
        return seeker_response

    @staticmethod
    def gig_view_count(gig_id):
        app.logger.error('[SeekerController][seeker_view_count_insert] * Updating Gigs-View count details!')
        sqlquery = "update gigdb.gigs set view_count = view_count+1 where gigs.gid=%s"
        commit_query(sqlquery, gig_id)

    @staticmethod
    def view_gig_details(req_params):
        gig_id = str(req_params['gid']).strip()
        SeekerModule.gig_view_count(gig_id)
        app.logger.error('[SeekerController][seeker_view_gig_details] * View details of gig selected by the seeker!')
        sqlquery = "SELECT * FROM gigdb.gigs where gigs.gid = %s "
        seeker_response = get_data_where(sqlquery, gig_id)
        return seeker_response

    @staticmethod
    def search_gigs(req_params):  # listing based on user selected options (skill, mode, location)
        app.logger.error('[SeekerController][seeker_search_gigs] * Listing all gigs that match seekerz selection !')
        data = (str(req_params['mode']).strip(), str(req_params['location']).strip(), str(req_params['skill']).strip(),
                str(req_params['skill']).strip())
        sqlquery = "SELECT gigs.gid,gigs.title, gigs.dop, gigs.deadline, gigs.category, gigs.tags, gigs.pay " \
                   " FROM gigdb.gigs where gigs.gigstatus = 'A' and gigs.mode = %s and location = %s " \
                   "and ( gigs.category in %s or gigs.tags in %s ) order by gigs.dop DESC"
        seeker_response = get_data_where(sqlquery, data)
        return seeker_response

    @staticmethod
    def update_profile(req_params):
        upd_rec_ts = datetime.now()
        firstname = str(req_params['firstname']).strip()
        lastname = str(req_params['lastname']).strip()
        phone = str(req_params['phone']).strip()
        country = str(req_params['country']).strip()
        question = str(req_params['securityq']).strip()
        answer = str(req_params['securitya']).strip()
        gender = str(req_params['gender']).strip()
        data = (firstname, lastname, phone, country, upd_rec_ts, question, answer, req_params['dob'], gender,
                req_params['sid'])
        sqlquery = "update gigdb.seeker set fname = %s, lname = %s, phno = %s, country = %s, upd_rec_ts = %s, " \
                   "securityq = %s, securitya = %s, dob = %s, gender = %s where seeker.sid = %s"
        seeker_response = commit_query(sqlquery, data)
        return seeker_response

    @staticmethod
    def send_proposal(req_params):
        cre_rec_ts = upd_rec_ts = datetime.now()
        message = str(req_params['message']).strip()
        data = (str(req_params['gid']).strip(), str(req_params['sid']).strip(), message, cre_rec_ts, upd_rec_ts,
                req_params['pid'])
        app.logger.info('[SeekerModule][seeker_send_proposal] Seeker sending proposal ')
        sqlquery = "insert into gigdb.proposals( gid, sid, msg , cre_rec_ts, upd_rec_ts, pid) values(%s,%s,%s,%s,%s,%s)"
        seeker_response = commit_query(sqlquery, data)
        return seeker_response
