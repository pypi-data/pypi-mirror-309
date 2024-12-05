# LilliePy #

this module initializes a LilliePy project

## What is LilliePy? #
it is a web framework that uses [ReactPy](https://reactpy.dev) fro the frontend, and [Flask](https://flask.palletsprojects.com/en/stable/) for the backend. It also includes other libraries to make the dev experience better.

## Requirements ##
##### you must need
 * [python](https://www.python.org/)
 * [pip](https://pypi.org/project/pip/)
 * [git](https://git-scm.com/)

## How to Use?
first you must create a python file,
after that, you must import ``` lilliepy ``` module, and put this code in:

```python
    # config.py (name this file anything)

    from lilliepy import create
    
    create() # put "sh" if you are using a linuxOS and not a windowsOS
```

or you could use the command line command

```bash
    python -m lilliepy
```

it will generate a Lilliepy app, you will know it was a success if the command line is in a green hue

and boom, your done, now have fun with the web framework, you can go ahead and delete you config file