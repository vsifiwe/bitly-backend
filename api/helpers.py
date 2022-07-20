def deviceType(request):
    # Documentation: https: // github.com/selwin/django-user_agents
    # based on https: // github.com/selwin/python-user-agents
    data = {
        'os': request.user_agent.os.family,
        'browser': request.user_agent.browser.family,
    }
    return data


def decode_utf8(input_iterator):
    for l in input_iterator:
        yield l.decode('utf-8')
