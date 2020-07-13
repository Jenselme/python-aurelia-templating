import re

from bs4 import BeautifulSoup


def render_string(template_string: str, context: dict) -> str:
    """Render the template string passed as a parameter with the supplied context."""
    template_string = _remove_hidden_elements(template_string, context)
    output = _interpolate_variables(template_string, context)
    return output


def _remove_hidden_elements(template_string, context):
    soup = BeautifulSoup(template_string, features="html.parser")
    for element in soup.find_all(lambda elt: elt.has_attr("if.bind")):
        variable_name = element.get("if.bind")
        if not context.get(variable_name):
            element.decompose()
        else:
            del element["if.bind"]

    return soup.prettify()


def _interpolate_variables(template_string, context):
    output = ""
    for line in template_string.split("\n"):
        processed_line = _interpolate_variables_in_line(line, context)
        output += processed_line + "\n"

    # Remove extra line break at the end.
    return output[:-1]


def _interpolate_variables_in_line(line, context):
    # Process variable interpolation.
    all_variables = re.findall(r"\$\{(\w+)\}", line)
    for variable_name in all_variables:
        line = line.replace(fr"${{{variable_name}}}", context.get(variable_name, ""))

    return line
