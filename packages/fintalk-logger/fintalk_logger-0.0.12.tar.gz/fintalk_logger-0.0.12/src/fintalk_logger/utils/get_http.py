def get_http(event):
    if not event.get('headers'):
        return None
    host = event['headers'].get('Host') or event['headers'].get('host')
    useragent = event['headers'].get('User-Agent') or event['headers'].get('user-agent')
    return {
        'url': f"https://{host}{event['path']}",
        'useragent': useragent,
        'method': event['httpMethod'],
        'host': host
    }