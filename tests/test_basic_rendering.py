from aurelia_templating import render_string


def test_no_syntax():
    input = 'Coucou toi'

    output = render_string(input, {})

    assert f'{input}\n' == output
