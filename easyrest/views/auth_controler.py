"""Controler which defines auth behavior
"""
import datetime as dt

from pyramid.view import view_config
from pyramid.authentication import AuthTicket

from ..scripts.json_helpers import wrap
from ..models.user import User
from ..models.token import Token
from ..auth import restrict_access, remember, forget


@view_config(route_name='login', renderer='json', request_method='GET')
def login_get(request):
    """Temporary controller for development
    Returns:
        list of all users and their tokens
    """
    user_list = request.dbsession.query(User).all()
    data = []
    for user in user_list:
        tokens = user.token
        tokens = [token.as_dict() for token in tokens]
        user = user.as_dict()
        user.update({"tokens": tokens})
        data.append(user)
    return wrap(data, True, '')


@view_config(route_name='login', renderer='json', request_method='POST')
def login_post(request):
    """Login controler. Check email and password provided by request,
    create token, write token in db, return token in header.
    Expects:
        POST request with json:
        {
            "email": (str),
            "password": (str)
        }
    Return:
        empty list with aditional header:
            {'X-Auth-Token': token}
    """
    req_json = request.json_body
    email, password = req_json["email"], req_json["password"]
    user = request.dbsession.query(User).filter(User.email == email).first()
    if user is None:
        return wrap([email], False, "No such user %s" % (user))
    if user.password != password:
        return wrap([password], False, "Wrong password %s" % (password))
    res_headers = remember(request, user)

    response = request.response
    response.headers.update(res_headers)

    return wrap([user.status.name])


@view_config(route_name='login', renderer='json', request_method='DELETE')
@restrict_access(user_types=['Client'])
def login_del(request):
    """Controler for logout. Check header for token, find token in db,
    delete token, return empty list with cleare header.
    Expects:
        DELETE request with header:
            {'X-Auth-Token': token}
    Return:
        empty list with aditional header:
            {'X-Auth-Token': ''}
    """
    res_headers = forget(request)
    response = request.response
    response.headers.update(res_headers)
    return wrap([])