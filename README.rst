Python Aurelia Templating
#########################

The goal of this library is to render templates written for the `Aurelia <https://aurelia.io>`__ JS framework with Python.
I tried to do a simple implementation mostly to ease coding.
This implementation is most likely slow on big templates and I don't intend to "fix" this at this time (although PRs are welcomed).

What I currently plan to support eventually:

- [X] Basic string interpolation.
- [X] Support ``if.bind``
- [X] Support ``repeat.for="friend of friends"``
- [ ] Support complex expressions in interpolation and ``if.bind`` like operators (``&&`` and ``||``) and ternaries.
- [ ] Import components with ``require``
- [ ] Slot injection
- [X] Extended support for ``bind`` with things like ``class.bind``
- [ ] Support filters: ``${test | format}``

Resources: the `templating basics <https://aurelia.io/docs/templating/basics#introduction>`__ in the documentation.

I plan to work on this library from time to time.
If you want to contribute, please feel free to do so.


Getting started
---------------

.. code:: python

    from aurelia_templating import render_string

    render_string('<div>Hello ${name}</div>', {'name': 'Julien'})
    # Returns ``<div>Hello Julien</div>``


Contributing
------------

This project uses `poetry <https://python-poetry.org/>`__ to manage dependencies and `pre-commit <https://pre-commit.com/>`__ to run pre-commits hooks.

#. Run ``poetry install`` to install dependencies in a venv.
#. Run ``poetry shell`` to enable this venv.
#. Run ``pytest`` to launch tests.
#. Run ``tox`` to run tests against multiple environments.
#. Install hooks with ``pre-commit install`` and ``pre-commit install -t pre-push``

PRs are welcomed!
