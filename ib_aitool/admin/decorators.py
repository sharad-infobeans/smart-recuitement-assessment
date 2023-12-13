from decorators import current_user
from functools import wraps
from flask import abort
from ib_aitool.database.models.Role import Role

def has_permission(permission=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            role = Role(name='Interviewer')
            role_permissions = role.permissions()
            if permission not in role_permissions:
                return f(*args,**kwargs)
                abort(403)
            return f(*args,**kwargs)

        return decorated_function
    return decorator



def has_role(role_name=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            role = Role(name='Interviewer')
            if role_name != role.name:
                return f(*args,**kwargs)
                abort(403)
            return f(*args,**kwargs)

        return decorated_function
    return decorator