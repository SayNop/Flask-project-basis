# Flask-project-basis
A self-used flask project basis

python Env: Py3.7

## Requirements

Jinja2==2.11.3

MarkupSafe==1.1.0

itsdangerous==1.1.0

Flask==1.1.4

Flask-Cors==3.0.7

Flask-Limiter==1.0.1

Flask-RESTful==0.3.6

Flask-SQLAlchemy==2.3.2

Flask-HTTPAuth==4.5.0

PyMySQL==1.0.2

greenlet==0.4.15

gunicorn==19.9.0

redis==2.10.6


## Structure
The project follows the standard directory structure. Below is an overview of the main directories and their contents:

- **`flask_app/`**: Contains the core source code of the project.
    - **`main.py`**: The entry point of the application.
    - **`__init__.py`**: Initialize the flask application.
    - **`resources/`**: Contains all bluepoints.

- **`common/`**: Contains packages and tools of the project. **If your use PyCharm, mark this dir as Sources Root**
    - **`settings/`**: Database ORM
    - **`model/`**: Database ORM 
    - **`utils/`**: Contains all py files.

- **`scripts/`**: Script files used during deployment. (change scripts mode `chmod +x scripts/*.sh`)


## Manual
- Check all `todo` in code.
- Update log file path in `scripts/run_flask.sh`.
- For api writing, see the `example` blueprint code.
- Run `scripts/run_flask.sh` to start server.


## Pycharm Run / Debug Configurations
Add *Flask server*
- Select *Target type: Custom*
- Input *Target: flask_app.main* (flask app path)
- Input *Application: app* (flask app name)


## About Models
Create a data table
1. Write the create table SQL statement (refer to `common/models/example.sql`)
2. Write ORM according to the data table field type


## Dev
- conn redis in views
    ```python
    from flask import current_app
    current_app.redis_master.set('test', 1)
    ```

- use logger in views
    ```python
    from flask import current_app
    current_app.logger.info('Logger test')
    # logger content in *flask.log*
    ```
