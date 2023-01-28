from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from models.roles import Role


@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario = db.Column(db.String(64))
    correo = db.Column(db.String(120))
    password_hash = db.Column(db.String(128))
    # role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    #post = db.relationship('Post', backref='author', lazy= 'dynamic')

    # def __init__(self, **kwargs):
    #     super(self, Users).__init__(**kwargs)
    #     if self.role is None:
    #         if self.usuario == 'nicolas123':
    #             self.role = Role.query.filter_by(name= 'Administator').first()

    #     if self.role is None:
    #         if self.role is None:
    #             self.role = Role.query.filter_by(default=True).first()



    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
