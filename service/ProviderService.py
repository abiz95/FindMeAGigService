import pymysql

from appConfig.db_config import mysql
from datetime import datetime
from service.DataService import *


def provider_user_registration(data):
    sql = "INSERT INTO gigdb.provider(company, emailid, pswd, phno, country, userstatus, cre_rec_ts, upd_rec_ts) " \
          "VALUES( %s, %s, %s, %s, %s, %s, %s, %s)"
    response = commit_query(sql, data)
    return response


def provider_add_gigs(req_params):
    title = str(req_params['title']).strip()
    description = str(req_params['description']).strip()
    dop = str(req_params['dop']).strip()
    deadline = str(req_params['deadline']).strip()
    category = str(req_params['category']).strip()
    tags = str(req_params['tags']).strip()
    mode = str(req_params['mode']).strip()
    pay = str(req_params['pay']).strip()
    location = str(req_params['location']).strip()
    pid = str(req_params['pid']).strip()
    now = datetime.now()
    sql = "INSERT INTO gigdb.gigs(title, description, dop, deadline, category, tags, mode, pay, location, " \
          "gigstatus, sid, pid, cre_rec_ts, upd_rec_ts) VALUES( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    data = (title, description, dop, deadline, category, tags, mode, pay, location, 'A', '0', pid, now, now)
    response = commit_query(sql, data)
    return response


def emailIDExists(emailid):
    sql = "SELECT * FROM gigdb.provider where emailid= %s"
    emailIDResponse = commit_query(sql, emailid)
    print(emailIDResponse)
    if emailIDResponse != '':
        emailResponse = "Failed"
        print(emailResponse)
    else:
        emailResponse = "Success" \
                        "" \
                        ""
        print(emailResponse)
    return emailResponse

