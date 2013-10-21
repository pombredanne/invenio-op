# -*- coding: utf-8 -*-
##
## This file is part of Invenio.
## Copyright (C) 2006, 2007, 2008, 2010, 2011, 2013 CERN.
##
## Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""
Invenio utilities to perform a REST like authentication.
"""
import re

try:
    from uuid import uuid4
except ImportError:
    import random

    def uuid4():
        return "%x" % random.getrandbits(16*8)


from invenio.config import CFG_WEB_API_KEY_ALLOWED_URL
from invenio.access_control_config import CFG_WEB_API_KEY_STATUS
from invenio.web_api_key_model import WebAPIKey

_CFG_WEB_API_KEY_ALLOWED_URL = [(re.compile(_url), _authorized_time,
                                _need_timestamp)
                                for _url, _authorized_time, _need_timestamp
                                in CFG_WEB_API_KEY_ALLOWED_URL]


def create_new_web_api_key(uid, key_description=None):
    """
    Creates a new pair REST API key / secret key for the user. To do that it
    uses the uuid4 function.

    @param uid: User's id for the new REST API key
    @type uid: int
    @param key_description: User's description for the REST API key
    @type key_description: string
    """
    WebAPIKey.create_new(uid, key_description)


def show_web_api_keys(uid, diff_status=CFG_WEB_API_KEY_STATUS['REMOVED']):
    """
    Makes a query to the DB to obtain all the user's REST API keys

    @param uid: User's id
    @type uid: int
    @param diff_status: This string indicates if the query will show
    all the REST API keys or only the ones that still active (usefull in the
    admin part)
    @type diff_statusparam: string

    """
    return WebAPIKey.show_keys(uid, diff_status)


def mark_web_api_key_as_removed(key_id):
    """
    When the user wants to remove one of his key, this functions puts the status
    value of that key to remove, this way the user doesn't see the key anymore
    but the admin user stills see it, make statistics whit it, etc.

    @param key_id: The id of the REST key that will be "removed"
    @type key_id: string
    """
    WebAPIKey.mark_as(key_id, CFG_WEB_API_KEY_STATUS['REMOVED'])


def get_available_web_api_keys(uid):
    """
    Search for all the available REST keys, it means all the user's keys that are
    not marked as REMOVED or REVOKED

    @param uid: The user id
    @type uid: int

    @return: WebAPIKey objects
    """
    return WebAPIKey.get_available(uid)


def acc_get_uid_from_request():
    """
    Looks in the data base for the secret that matches with the API key in the
    request. If the REST API key is found and if the signature is correct
    returns the user's id.

    @return: If everything goes well it returns the user's uid, it not -1
    """

    return WebAPIKey.acc_get_uid_from_request()


def build_web_request(path, params=None, uid=-1, api_key=None, timestamp=True):
    """
    Build a new request that uses REST authentication.
    1. Add your REST API key to the params
    2. Add the current timestamp to the params, if needed
    3. Sort the query string params
    4. Merge path and the sorted query string to a single string
    5. Create a HMAC-SHA1 signature of this string
       using your secret key as the key
    6. Append the hex-encoded signature to your query string

    @note: If the api_key parameter is None, then this method performs a search
        in the data base using the uid parameter to get on of the user's REST
        API key. If the user has one or more usable REST  API key this method
        uses the first to appear.

    @param path: uri of the request until the "?" (i.e.: /search)
    @type path: string
    @param params: All the params of the request (i.e.: req.args or a dictionary
    with the param name as key)
    @type params: string or dict
    @param api_key: User REST API key
    @type api_key: string
    @param uid: User's id to do the search for the REST API key
    @type uid: int
    @param timestamp: Indicates if timestamp is needed in the request
    @type timestamp: boolean

    @return: Signed request string or, in case of error, ''
    """

    return WebAPIKey.build_web_request(path, params, uid, api_key, timestamp)
