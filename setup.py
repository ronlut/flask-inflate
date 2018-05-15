from setuptools import setup, find_packages

setup(name='flask-inflate',
      version='0.1',
      description='Inflate / Decompress gzipped requests',
      url='https://github.com/ronlut/flask-inflate',
      author='Rony Lutsky',
      author_email='ronlut@gmail.com',
      py_modules=['flask_inflate'],
      zip_safe=False,
      install_requires=[
          'flask',
      ])
