def get_ip(event):
    try:
        requestContext = event.get('requestContext', {})
        identity = requestContext.get('identity', {})
        sourceIp = identity.get('sourceIp')
    except:
        sourceIp = None
    headers = event.get('headers')
    if headers:
        ip = headers.get('CF-Connecting-IP') or headers.get('cf-connecting-ip') \
            or headers.get('X-Real-IP') or headers.get('x-real-ip') \
            or headers.get('X-Forwarded-For') or headers.get('x-forwarded-for')
    else:
        ip = sourceIp
    if not ip:
        return None
    return ip.split(',')[0]