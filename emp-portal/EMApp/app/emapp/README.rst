Employee Task Management App Core Module
=====
core: Responsible for parsing all the registered plugins for ETM App
=====

Responsible for parsing all the registered plugins for ETM App.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "core" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'core',
    ]

2. Add from core.tools import register_plugins.

3. Add below line in manage.py and wsgi.py
    ```
        core_app = register_plugins.AppRegister()
        core_app.register()
    ```
4. Start the development server and visit http://127.0.0.1:8000
