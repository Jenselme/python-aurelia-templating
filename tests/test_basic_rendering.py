from aurelia_templating import render_string

import pytest


def test_no_syntax():
    input = 'Coucou toi'

    output = render_string(input, {})

    assert f'{input}\n' == output


@pytest.mark.parametrize(
    "template,context,expected",
    [
        ("Hi ${name}", {'name': 'Julien'}, "Hi Julien\n"),
        ("Hi ${name}, how are you ${name}?", {'name': 'Julien'}, "Hi Julien, how are you Julien?\n"),
        ("Hi ${name}", {}, "Hi \n"),
        ("Hi ${name1} and ${name2}!", {'name1': 'Julien', 'name2': 'Pierre'}, "Hi Julien and Pierre!\n"),
    ]
)
def test_variable_interpolation(template, context, expected):
    output = render_string(template, context)

    assert output == expected
