# sphinx-grasple

**A Grasple exercise extension for Sphinx**.

This package contains a [Sphinx](http://www.sphinx-doc.org/en/master/) extension for inserting Grasple exercises into a Jupyter book as an iframe.

This package is a continuation of the package https://github.com/dbalague/sphinx-grasple/.

## Installation
To install the teachbooks-sphinx-grasple extension, follow these steps:

**Step 1: Install the Package**

Install the `teachbooks-sphinx-grasple` package using `pip`:
```
pip install teachbooks-sphinx-grasple
```

**Step 2: Add to `requirements.txt`**

Make sure that the package is included in your project's `requirements.txt` to track the dependency:
```
teachbooks-sphinx-grasple
```

**Step 3: Enable in `_config.yml`**

In your `_config.yml` file, add the extension to the list of Sphinx extra extensions (**important**: underscore, not dash this time):
```
sphinx: 
    extra_extensions:
        - teachbooks_sphinx_grasple
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
