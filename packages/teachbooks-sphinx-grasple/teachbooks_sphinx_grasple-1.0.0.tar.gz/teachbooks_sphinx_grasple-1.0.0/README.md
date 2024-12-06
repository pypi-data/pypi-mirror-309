# sphinx-grasple

**A Grasple exercise extension for Sphinx**.

This package contains a [Sphinx](http://www.sphinx-doc.org/en/master/) extension for inserting Grasple exercises into a Jupyter book as an iframe.

This package is a continuation of the package https://github.com/dbalague/sphinx-grasple/.

## Get started

To get started with `sphinx-grasple`, first add it as a submodule to .gitmodules

```code
...
[submodule "sphinx-grasple"]
	path = sphinx-grasple
	url = https://github.com/TeachBooks/Sphinx-Grasple-public.git
...
```

then, add `sphinx_grasple` to your sphinx `extensions` in the `conf.py`

```code
...
extensions = ["sphinx_grasple"]
...
```

and do not forget to install the submodule:

```code
pip install sphinx-grasple/
```

## Usage

To use, include the following in your Jupyter book

```code
::::{grasple}
:iframeclass: dark-light
:url: https://embed.grasple.com/exercises/f6c1bb4b-e63e-492e-910a-5a8c433de281?id=75093
:label: grasple_exercise_1_3_4
:dropdown:
:description: Cross product in $\R^4$?

::::
```

## Important Note

The tests provided are still the original ones from sphinx-exercise and have not (yet) been adapted.
