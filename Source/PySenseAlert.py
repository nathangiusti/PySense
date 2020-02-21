import json

def createAlert(user, name):
    alert = {}
    alert['enabled'] = 'true'
    alert['name'] = name
    user = {}
    user['type'] = "user"
    user['id'] = 'temp'
    alert['parties'] = 'temp'