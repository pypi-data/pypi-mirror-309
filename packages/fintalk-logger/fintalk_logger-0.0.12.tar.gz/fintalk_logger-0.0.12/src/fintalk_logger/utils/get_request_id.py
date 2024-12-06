def get_request_id(event):
    requestContext = event.get('requestContext')
    if not requestContext:
        return None
    return requestContext.get('requestId')