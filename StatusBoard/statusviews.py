
from flask import Blueprint, render_template, url_for, request, jsonify, redirect
from . import oidc
from . import db 
from .models import Status
from .userviews import getuserinfo
import json

statusviews = Blueprint('statusviews', __name__)

#############################################################################
@statusviews.route("/status/", methods=['GET', 'POST'])
@oidc.require_login
def statusHome():
    if oidc.user_loggedin:
        is_logged_in = True
        userinfo = getuserinfo(oidc)
        if request.method == 'POST':
            status_name = request.form.get('name')
            status_color = request.form.get('status_color')
            new_status = Status(name=status_name, color=status_color)    
            db.session.add(new_status)
            db.session.commit()
        statusList = Status.query.all()
        return render_template("status.html", status=statusList, userinfo=userinfo, is_logged_in=oidc.user_loggedin)
    else:
        return redirect(url_for("statusviews.home"))

@statusviews.route("/status/edit/<id>", methods=['GET', 'POST'])
@oidc.require_login
def statusEdit(id):
    statusList = Status.query.get(id)
    new_name = request.form.get('name')
    new_color = request.form.get('status_color')
    
    if request.method == 'POST':
        statusList.name = new_name
        if new_color != 'null':
            statusList.color = new_color
        db.session.commit()
        return redirect(url_for('status.home'))
    
    statusList = Status.query.get(id)
    return render_template("edit_status.html", status=statusList )
@statusviews.route("/status/delete", methods=['GET', 'POST'])
@oidc.require_login
def statusDelete():
    data = json.loads(request.data)
    id = data['statusID']
    s = Status.query.get(id)
    if s:
        db.session.delete(s)
        db.session.commit()
    return jsonify({})