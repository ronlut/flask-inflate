"""
Flask-Inflate
-------------

A simple flask extension to deal with gzipped (compressed) request data sent by clients.
"""
from setuptools import setup


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]

setup(
    name='Flask-Inflate',
    version='0.2',
    url='https://github.com/ronlut/flask-inflate',
    license='MIT',
    author='Rony Lutsky',
    author_email='ronlut@gmail.com',
    description='Inflate / Decompress gzipped requests',
    long_description=__doc__,
    py_modules=['flask_inflate'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=parse_requirements('requirements.txt'),
    classifiers=[
          'Framework :: Flask',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
          'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)