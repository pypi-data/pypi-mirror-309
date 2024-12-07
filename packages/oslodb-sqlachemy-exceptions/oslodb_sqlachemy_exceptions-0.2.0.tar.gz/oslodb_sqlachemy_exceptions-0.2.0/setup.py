# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['oslodb_sqlachemy_exceptions']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.2.0,<2.0.0', 'debtcollector>=1.2.0,<2.0.0']

setup_kwargs = {
    'name': 'oslodb-sqlachemy-exceptions',
    'version': '0.2.0',
    'description': '',
    'long_description': 'None',
    'author': 'Douglas Bett',
    'author_email': 'bettdalpha@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
