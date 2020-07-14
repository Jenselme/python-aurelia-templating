import pytest
from bs4 import BeautifulSoup

from aurelia_templating import render_string


def test_no_syntax():
    input_ = "Coucou toi"

    output = render_string(input_, {})

    assert f"{input_}\n" == output


@pytest.mark.parametrize(
    "template,context,expected",
    [
        ("Hi ${name}", {"name": "Julien"}, "Hi Julien"),
        ("Hi ${name}, how are you ${name}?", {"name": "Julien"}, "Hi Julien, how are you Julien?",),
        ("Hi ${name}", {}, "Hi "),
        (
            "Hi ${name1} and ${name2}!",
            {"name1": "Julien", "name2": "Pierre"},
            "Hi Julien and Pierre!",
        ),
        (
            """<p class="${cls}">${name}</p>""",
            {"name": "Julien", "cls": "my-class"},
            """<p class="my-class">Julien</p>""",
        ),
        (
            """<p class="${cls}">${name} ${name}</p>""",
            {"name": "Julien", "cls": "my-class"},
            """<p class="my-class">Julien Julien</p>""",
        ),
    ],
)
def test_variable_interpolation(template, context, expected):
    output = render_string(template, context)

    assert (
        BeautifulSoup(output, features="html.parser",).prettify()
        == BeautifulSoup(expected, features="html.parser").prettify()
    )


@pytest.mark.parametrize(
    "template,context,expected",
    (
        ("""<div if.bind="my_var">Test</div>""", {"my_var": True}, """<div>Test</div>"""),
        ("""<div if.bind="my_var">Test</div>""", {"my_var": False}, ""),
    ),
)
def test_basic_conditional_rendering(template, context, expected):
    output = render_string(template, context)

    assert (
        BeautifulSoup(output, features="html.parser",).prettify()
        == BeautifulSoup(expected, features="html.parser").prettify()
    )
