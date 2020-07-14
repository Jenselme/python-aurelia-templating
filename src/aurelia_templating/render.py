import re
from copy import copy

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

        was_repeated = _repeat_node(child, context)
        if was_repeated:
            # The node use to do the repetition doesn't exist any more, moving on.
            continue

        _interpolate_variables(child, context)
        _bind_attributes(child, context)
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


def _repeat_node(node, context) -> bool:
    if isinstance(node, TERMINATION_NODE_TYPES):
        return False

    loop_expression = node.attrs.get("repeat.for")
    if loop_expression is None:
        return False

    if search := re.search(
        r"^(?P<loop_variable>\w+)\s+of\s+(?P<context_iterator>\w+)", loop_expression
    ):
        del node.attrs["repeat.for"]
        found_variables = search.groupdict()
        for loop_value in context.get(found_variables["context_iterator"]):
            loop_context = {
                **context,
                found_variables["loop_variable"]: loop_value,
            }
            new_node = copy(node)
            _render_node(new_node, loop_context)
            node.parent.append(new_node)

        # Remove the existing node, it has been replaced it by the repeated element.
        node.decompose()

        return True

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
        # attrs_list is a list of all values.
        # Eg for class="container cls" it will be ["container", "cls"]
        for attr_value in attrs_list:
            interpolations = _find_interpolations_in_string(attr_value)
            if interpolations:
                for variable_name in interpolations:
                    new_attrs_list.append(_interpolate_string(attr_value, variable_name, context))
            else:
                new_attrs_list.append(attr_value)
        node.attrs[attr_name] = new_attrs_list


def _bind_attributes(node, context):
    if isinstance(node, TERMINATION_NODE_TYPES):
        return

    attrs_to_delete = set()
    attrs_to_add = {}
    for attr_name, attr_values in node.attrs.items():
        if not attr_name.endswith(".bind"):
            continue

        attrs_to_delete.add(attr_name)
        stripped_attr_name = attr_name.replace(".bind", "")
        variable_name = "".join(attr_values)
        attrs_to_add[stripped_attr_name] = context.get(variable_name)

    node.attrs.update(attrs_to_add)

    for attr_to_delete in attrs_to_delete:
        del node.attrs[attr_to_delete]
