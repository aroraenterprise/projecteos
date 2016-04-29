"""
Project: flask-rest
Author: Saj Arora
Description: Handles various response types
"""


def make_empty_ok_response():
    """Returns OK response with empty body"""
    return '', 204


def make_json_ok_response(data):
    """Returns OK response with json body"""
    return data

def make_list_response(reponse_list, cursor=None, more=False, total_count=None):
    """Creates reponse with list of items and also meta data useful for pagination

    Args:
        reponse_list (list): list of items to be in response
        cursor (Cursor, optional): ndb query cursor
        more (bool, optional): whether there's more items in terms of pagination
        total_count (int, optional): Total number of items

    Returns:
        dict: response to be serialized and sent to client
    """
    return {
        'list': reponse_list,
        'meta': {
            'next_cursor': cursor.urlsafe() if cursor else '',
            'more': more,
            'total_count': total_count
        }
    }