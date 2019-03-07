from app import create_app
from flask_script import Manager
from flask_migrate import MigrateCommand

app = create_app('default')
manage = Manager(app)
manage.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manage.run()




