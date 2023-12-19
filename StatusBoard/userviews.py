from flask import Blueprint, render_template, url_for, request, jsonify, redirect
from . import oidc
from . import db
from .models import User, Status
userviews = Blueprint('userviews', __name__)
import pprint

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class UserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    is_admin = BooleanField("Site Administrator")
    update = SubmitField("Update")
    add = SubmitField("Add")

class SearchUser(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    search = SubmitField("Search")

def getuserinfo(oidc):
    info = oidc.user_getinfo(['preferred_username', 'given_name', 'family_name', 'groups']) 
    groups = info.get('groups')
    is_admin = False
    for g in groups:
        if g == 'sbadmin':
            is_admin = True
    username = info.get('preferred_username')
    user_query = User.query.filter_by(username=username).first()  
    if user_query is None:
        new_user = User(username=username, first_name=info.get('given_name'), last_name=info.get('family_name'), is_admin=is_admin)
        db.session.add(new_user)
        db.session.commit()    
        user_query = User.query.filter_by(username=username).first()  
    else:
        if user_query.is_admin != is_admin:
            print("Admin mismatch", user_query.is_admin, is_admin)
            user_query.is_admin = is_admin
            db.session.commit()
            user_query = User.query.filter_by(username=username).first()  
    return User.query.filter_by(username=username).first()


@userviews.route("/")
def home():    
    if oidc.user_loggedin:
        userinfo = getuserinfo(oidc)
        
        return render_template("index.html", userinfo=userinfo, is_logged_in=True)
    else:
        return render_template("index.html", userinfo=False, is_logged_in=False)



@userviews.route("/user/<username>", methods=['GET', 'POST'])
@oidc.require_login
def userinfo(username):    
    userinfo = User.query.filter_by(username=username).first()
    if request.method == 'POST':
        u = User.query.filter_by(username=username).first()
        u.note = request.form.get('notes') 
        if request.form.get('status_reset') == 'on':
            u.nightly_reset_status = True
        else:
            u.nightly_reset_status = False
        if request.form.get('notes_reset') == 'on':
            u.nightly_reset_notes = True
        else:
            u.nightly_reset_notes = False
        db.session.commit()
    status = Status.query.all()
    if userinfo:
        return render_template("user.html", userinfo=userinfo, status=status,  is_logged_in=True)
    else:
        return redirect(url_for('userviews.home'))
    
@userviews.route("/user/<username>/status/<statusid>")
def set_user_status(username, statusid):
    u = User.query.filter_by(username=username).first()
    s = Status.query.get(statusid)
    if u and s:
        u.status_id = s.id
        db.session.commit()

    return jsonify({})


@userviews.route("/search/user")
@oidc.require_login
def userSearch():
    q = request.args.get("q")
    print(q)

    if q:
        results = User.query.filter(User.username.icontains(q) | User.last_name.icontains(q) | User.first_name.icontains(q)).all()
        
    else:
        results = []

    return render_template("search_results.html", results=results)
@userviews.route("/search/user/excludegroup/<id>")
@oidc.require_login
def userSearchExcludingGroupMembers(id):
    from .models import Group
    q = request.args.get("q")
    g = Group.query.get(id)
    if q:
        results = User.query.filter(User.username.icontains(q) | User.last_name.icontains(q) | User.first_name.icontains(q)).all()
        
    else:
        results = []
    print(results)
    return render_template("checkform.html", results=results, groupinfo=g)




@userviews.route("/admin/user")
@oidc.require_login
def userAdminHome():
    userinfo = getuserinfo(oidc)
    if not userinfo.is_admin:
        return redirect(url_for('usersview.home'))
    
    allUsers = User.query.with_entities(User.id,User.username,User.first_name,User.last_name)
    return render_template("useradm.html", userinfo=userinfo, userlist=allUsers, is_logged_in=True)

@userviews.route("/admin/user/edit/<id>", methods=['GET','POST'])
@oidc.require_login
def userAdminEdit(id):
    userinfo = getuserinfo(oidc)
    if not userinfo.is_admin:
        return redirect(url_for('usersview.home'))
    u = User.query.get(id)
    if userinfo.is_admin == False and userinfo.id != u.id:
        return redirect( url_for('userviews.home') )

    form = UserForm()
    if u is None:
        return redirect(url_for('userviews.home'))
    else:
        if request.method =='POST':
            fn = request.form.get('first_name')
            ln = request.form.get('last_name')
            adm = request.form.get('is_admin')
            u.first_name = fn
            u.last_name = ln
            if adm == 'y':
                u.is_admin = True
            else:
                u.is_admin = False
            db.session.commit()
            u = User.query.get(id)

        
        form.username.data = u.username
        form.first_name.data = u.first_name
        form.last_name.data = u.last_name
        
        form.is_admin.data = u.is_admin
        return render_template("user_editor.html", userinfo=userinfo,  edituser=u, is_logged_in=True, form=form)
    
    return redirect(url_for('views.home'))

@userviews.route('/adminuser/add', methods=['GET','POST'])
@oidc.require_login
def userAdminAddUser():
    userinfo = getuserinfo(oidc)
    if not userinfo.is_admin:
        return redirect(url_for('usersview.home'))
    if request.method == 'POST':
        
        un = request.form.get('username')
        fn = request.form.get('first_name')
        ln = request.form.get('last_name')
        adm = request.form.get('is_admin')
        print(request.form.get('add'))
        if adm == 'y':
            is_admin = True
        else:
            is_admin = False
        u = User(username=un, first_name=fn, last_name=ln,is_admin=is_admin)
        db.session.add(u)
        db.session.commit()
        return redirect(url_for('userviews.userAdminHome'))
    form = UserForm()
    return render_template("user_editor.html", userinfo=userinfo, newuser=True, is_logged_in=True, form=form)

@userviews.route('/admin/user/delete/<id>', methods=['GET','POST'])
@oidc.require_login
def userAdminDelUser(id):
    userinfo = getuserinfo(oidc)
    if not userinfo.is_admin:
        return redirect(url_for('usersview.home'))
    u = User.query.get(id)
    if u:
        db.session.delete(u)
        db.session.commit()
        return redirect(url_for('userviews.userAdminHome'))


    