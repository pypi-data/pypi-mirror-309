import json
import base64

def getUserPayload(event):
    headers = event.get('headers')
    if not headers:
        return None
    authorization = headers.get('Authorization') or headers.get('authorization')
    if not authorization:
        return None
    payload = authorization.split('.')[1]
    if not payload:
        return None
    try:
        return json.loads(base64.b64decode(payload).decode('utf-8'))
    except:
        return None

def get_user(event):
    requestContext = event.get('requestContext')
    if not requestContext:
        return None
    context = requestContext.get('authorizer')
    payload = getUserPayload(event)
    if not payload:
        return None
    return {
        'id': payload.get('sub'),
        'status': context.get('status'),
        'groups': payload.get('groups') or payload.get('cognito:groups'),
        'email': payload.get('email'),
        'type': context.get('type') or payload.get('type'),
        'companyId': context.get('companyId'),
        'scope': payload.get('scope')
    }