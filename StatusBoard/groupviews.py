from flask import Blueprint, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired
#from wtforms_alchemy import QuerySelectMultipleField
from . import oidc
from . import db
from .models import Group
from .userviews import getuserinfo
#from .forms import GroupForm,SearchUser


groupviews = Blueprint('groupviews', __name__)

class GroupForm(FlaskForm):
    name = StringField("Group Name", validators=[DataRequired()])
    description = StringField("Description")
    update = SubmitField("Update")
    add = SubmitField("Add")


@groupviews.route("/groups")
def groupHome():
    allGroups = Group.query.limit(25).all()
    if oidc.user_loggedin:    
        userinfo = getuserinfo(oidc)
        return render_template("groups.html", userinfo=userinfo, is_logged_in=True, grouplist=allGroups)
    else:
        return render_template("groups.html", userinfo=False, is_logged_in=False, grouplist=allGroups)

@groupviews.route("/group/<id>")
def groupShow(id):
    groupinfo = Group.query.get(id)
    if oidc.user_loggedin:    
        userinfo = getuserinfo(oidc)
        return render_template("groups.html", userinfo=userinfo,  groupinfo=groupinfo, is_logged_in=True )
    else:
        return render_template("groups.html", userinfo=False, groupinfo=groupinfo, is_logged_in=False)
    

#@groupviews.route("/group/admin")
#@oidc.require_login
#def groupAdminHome():
#    userinfo = getuserinfo(oidc)
#    allGroups = Group.query.limit(3).all()
#    return render_template("groupsmgr.html", userinfo=userinfo, grouplist=allGroups, is_logged_in=True )

@groupviews.route("/group/admin/add", methods=['GET', 'POST'])
@oidc.require_login
def groupAdminAdd():
    userinfo = getuserinfo(oidc)
    if not userinfo.is_admin:
        return redirect(url_for('userviews.home'))
    if request.method == 'POST':
        new_name = request.form.get('name')
        new_desc = request.form.get('description')
        new_group = Group(name=new_name, description=new_desc)
        db.session.add(new_group)
        db.session.commit()
        print(new_group.id)
        return redirect(url_for('groupviews.groupAdminEdit', id=new_group.id))
        
        
    newGroupForm = GroupForm()
    return render_template("groupsmgr.html", form=newGroupForm, userinfo=userinfo,  is_logged_in=True )

@groupviews.route("/group/admin/edit/<id>", methods=['GET', 'POST'])
@oidc.require_login
def groupAdminEdit(id):
    userinfo = getuserinfo(oidc)
    groupinfo = Group.query.get(id)
    if userinfo not in groupinfo.members and not userinfo.is_admin:
        return redirect(url_for('userviews.home'))
    if request.method == 'POST':
        groupinfo.name = request.form.get('name')
        groupinfo.description = request.form.get('description')
        db.session.commit()
    newGroupForm = GroupForm()
    newGroupForm.name.data = groupinfo.name
    if groupinfo.description:
        newGroupForm.description = groupinfo.description
    return render_template("groupsmgr.html", form=newGroupForm, groupinfo=groupinfo, userinfo=userinfo,  is_logged_in=True )

@groupviews.route("/group/admin/delete/<id>", methods=['GET', 'POST'])
@oidc.require_login
def groupAdminDelete(id):
    userinfo = getuserinfo(oidc)
    groupinfo = Group.query.get(id)
    if not userinfo.is_admin:
        return redirect(url_for('userviews.home'))
    db.session.delete(groupinfo)
    db.session.commit()
    return render_template("groupsmgr.html", userinfo=userinfo,  is_logged_in=True )

@groupviews.route("/group/admin/<gid>/member", methods=['GET', 'POST'])
@oidc.require_login
def groupMembersShow(gid):
    userinfo = getuserinfo(oidc)
    groupinfo = Group.query.get(gid)
    if userinfo not in groupinfo.members and not userinfo.is_admin:
        return redirect(url_for('userviews.home'))

    return render_template('groupmembers.html', groupinfo=groupinfo)
@groupviews.route("/group/admin/edit/<gid>/member/<action>/<uid>", methods=['GET', 'POST'])
@oidc.require_login
def groupAdminUpdateMembers(gid,action,uid):
    userinfo = getuserinfo(oidc)
    groupinfo = Group.query.get(gid)
    if userinfo not in groupinfo.members and not userinfo.is_admin:
        return redirect(url_for('userviews.home'))
    
    from .models import User
    u = User.query.get(uid)
    g = Group.query.get(gid)
    if action == 'add':
        g.members.append(u)
    elif action == 'delete':
        g.members.remove(u)
    elif action == 'addmod':
        g.mods.append(u)
    elif action == 'deletemod':
        g.mods.remove(u)
    else:
        return redirect(url_for('userviews.home'))
    db.session.commit()
    return redirect(url_for('groupviews.groupAdminEdit',id=g.id))

@groupviews.route("/search/group")
def groupSearch():
    q = request.args.get("q")
    if q:
        results = Group.query.filter(Group.name.icontains(q)).limit(50).all()    
    else:
        results = []
    return render_template("group_search.html", results=results)