#! /bin/bash
# source ~/.zshrc
export FLASK_ENV=production
cd ..
exec gunicorn -b 0.0.0.0:7903 --access-logfile /logs/flask/access_app.log --error-logfile /logs/flask/error_app.log flask_app.main:app
