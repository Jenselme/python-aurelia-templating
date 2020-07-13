import re


def render_string(template_string: str, context: dict) -> str:
    """Render the template string passed as a parameter with the supplied context."""
    output = ""
    for line in template_string.split("\n"):
        processed_line = _process_line(line, context)
        output += processed_line + "\n"

    return output[:-1]


def _process_line(line, context):
    # Process variable interpolation.
    all_variables = re.findall(r"\$\{(\w+)\}", line)
    for variable_name in all_variables:
        line = line.replace(fr"${{{variable_name}}}", context.get(variable_name, ""))

    return line
