import re

from bs4 import BeautifulSoup
from bs4.element import NavigableString, TemplateString

TERMINATION_NODE_TYPES = (NavigableString, TemplateString)


def render_string(template_string: str, context: dict) -> str:
    """Render the template string passed as a parameter with the supplied context."""
    soup = BeautifulSoup(template_string, features="html.parser")
    _render_node(soup, context)
    return soup.prettify()


def _render_node(node, context):
    for child in node.children:
        was_removed = _remove_hidden_elements(child, context)
        if was_removed:
            continue

        _interpolate_variables(child, context)
        if hasattr(child, "children"):
            _render_node(child, context)


def _remove_hidden_elements(node, context) -> bool:
    if isinstance(node, TERMINATION_NODE_TYPES):
        return False

    variable_name = node.get("if.bind")
    if variable_name is None:
        return False

    if not context.get(variable_name):
        node.decompose()
        return True

    del node["if.bind"]
    return False


def _interpolate_variables(node, context):
    if isinstance(node, TERMINATION_NODE_TYPES):
        _interpolate_variables_in_string(node, context)
    else:
        _interpolate_variables_in_attributes(node, context)


def _interpolate_variables_in_string(string_node, context):
    base_string = string_node.string
    for variable_name in _find_interpolations_in_string(string_node.string):
        base_string = _interpolate_string(base_string, variable_name, context)

    string_node.replace_with(base_string)


def _find_interpolations_in_string(string: str) -> list:
    return re.findall(r"\$\{(\w+)\}", string)


def _interpolate_string(string, variable_name, context):
    return string.replace(fr"${{{variable_name}}}", context.get(variable_name, ""))


def _interpolate_variables_in_attributes(node, context):
    for attr_name, attrs_list in node.attrs.items():
        new_attrs_list = []
        for attr_value in attrs_list:
            for variable_name in _find_interpolations_in_string(attr_value):
                new_attrs_list.append(_interpolate_string(attr_value, variable_name, context))
        node.attrs[attr_name] = new_attrs_list
