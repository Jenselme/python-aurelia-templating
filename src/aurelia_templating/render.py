def render_string(template_string: str, context: dict) -> str:
    """Render the template string passed as a parameter with the supplied context.
    """
    output = ''
    for line in template_string.split('\n'):
        output += line + '\n'

    return output
