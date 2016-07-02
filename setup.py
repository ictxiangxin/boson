import boson.bs_configure as configure
from distutils.core import setup

if __name__ == "__main__":
    with open('README.md') as fp:
        long_description = fp.read()

    setup(name=configure.boson_package_name,
          version='%d.%d' % (configure.boson_version_main, configure.boson_version_sub),
          author='ict',
          author_email='ictxiangxin@gmail.com',
          maintainer='ict',
          maintainer_email='ictxiangxin@gmail.com',
          description='Grammar analyzer generator',
          long_description=long_description,
          platforms=['MS Windows', 'Mac X', 'Unix/Linux'],
          keywords=['boson', 'grammar analyzer generator'],
          packages=['boson'],
          packages_data={"boson", ["templates/*.template"]},
          classifiers=['Natural Language :: English',
                       'Programming Language :: Python',
                       'Operating System :: Microsoft :: Windows',
                       'Operating System :: Unix',
                       'Operating System :: MacOS',
                       'Programming Language :: Python :: 3'], )
