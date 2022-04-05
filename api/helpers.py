import re


def deviceType(request):
    return request.user_agent.browser.family
    MOBILE_AGENT_RE = re.compile(
        r".*(iphone|mobile|androidtouch)", re.IGNORECASE)

    if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
        return "mobile"
    else:
        return request.META['HTTP_USER_AGENT']
