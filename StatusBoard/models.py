from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import event

#
# Many to many tables
#
group_members= db.Table( 'group_members',
    db.Column('user_id',  db.Integer, db.ForeignKey('user.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'))
)
group_mods = db.Table( 'group_mods',
    db.Column('user_id',  db.Integer, db.ForeignKey('user.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'))
)  
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'), default=1)
    nightly_reset_status = db.Column(db.Boolean, default=False)
    nightly_reset_notes = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    note = db.Column(db.String(300))


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    description = db.Column(db.String(150), nullable=True)
    members = db.relationship('User', secondary=group_members, backref='groups')
    mods = db.relationship('User',secondary=group_mods, backref='mod_on')
@event.listens_for(Group.__table__, 'after_create')
def create_default_group_data(*args, **kwargs):
    db.session.add(Group(name='Demo'))
    db.session.commit()


class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(7), unique=True, nullable=False)
    color = db.Column(db.String(32))
    users = db.relationship('User', backref='status')
@event.listens_for(Status.__table__, 'after_create')
def create_default_status_data(*args, **kwargs):
    db.session.add(Status(name='UNKNOWN', color='btn-secondary'))
    db.session.add(Status(name='IN', color='btn-success'))
    db.session.add(Status(name='OUT', color='btn-danger'))
    db.session.commit()
    


