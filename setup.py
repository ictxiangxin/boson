__author__ = 'Fule Liu'

import sys

if sys.version[0] < '3':
    raise SystemError("The Python version must be 3, your python version info is " + sys.version)

from distutils.core import setup

with open('README.md') as fp:
    LONG_DESCRIPTION = fp.read()


# TODO: add more specific information about boson.
setup(name='boson',
      version='0.5',
      author='ict',
      author_email='ictxiangxin@gmail.com',
      maintainer='ict',
      maintainer_email='ictxiangxin@gmail.com',
      description='Grammar analyzer generator',
      long_description=LONG_DESCRIPTION,
      platforms=['MS Windows', 'Mac X', 'Unix/Linux'],
      keywords=['boson', 'grammar analyzer generator'],
      packages=['boson'],
      classifiers=['Natural Language :: English',
                   'Programming Language :: Python',
                   'Operating System :: Microsoft :: Windows',
                   'Operating System :: Unix',
                   'Operating System :: MacOS',
                   'Programming Language :: Python :: 3'], )
