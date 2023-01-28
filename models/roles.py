from app import db, login_manager
from models.permissions import Permissions


class Role(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(64), unique= True)
    default = db.Column(db.Boolean, default= False, index= True)
    permissions = db.Column(db.Integer)
    # user = db.relationship('User', backref='role', lazy='dynamic')
    
    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0
    
    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permissions(self, perm):
        if self.has_permissions(perm):
            self.permissions -= perm
   
    def reset_permissions(self):
        self.permissions = 0

    def has_permissions(self, perm):
        return self.permissions & perm == perm

    def insert_roles(self):
        roles = {
            'User': [Permissions.FOLLOW, Permissions.COMMENT, Permissions.WRITE],
            'Moderator': [Permissions.FOLLOW, Permissions.COMMENT, Permissions.WRITE, Permissions.MODERATE],
            'Administrator': [Permissions.FOLLOW, Permissions.COMMENT, Permissions.WRITE, Permissions.MODERATE, Permissions.ADMIN],
        }

        default_role = 'User'

        for  r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
        
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()
        
    

