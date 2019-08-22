from setuptools import setup

setup(
    name='MonE',
    packages=['MonE'],
    install_requires=[
        'flask',
        'flask_sqlalchemy',
        'flask-marshmallow',
        'marshmallow-sqlalchemy',
        'flask-security',
        'urllib3',
    ]
)
