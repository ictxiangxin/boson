import boson.configure as configure
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

install_requires = [
    'jinja2>=2.7',
]

if __name__ == '__main__':
    long_description = '{} - {}'.format(configure.boson_title, configure.boson_description)
    setup(name=configure.boson_package_name,
          version='{}.{}'.format(configure.boson_version_major, configure.boson_version_minor),
          url=configure.boson_url,
          license=configure.boson_license,
          author=configure.boson_author,
          author_email=configure.boson_email,
          maintainer=configure.boson_author,
          maintainer_email=configure.boson_email,
          description=configure.boson_description,
          long_description=long_description,
          platforms=['MS Windows', 'Mac X', 'Unix/Linux'],
          keywords=[configure.boson_package_name, configure.boson_description],
          packages=[
              configure.boson_package_name,
              configure.boson_package_name + '.binary_generator',
              configure.boson_package_name + '.boson_script',
              configure.boson_package_name + '.boson_script.boson_script_parser',
              configure.boson_package_name + '.code_generator',
              configure.boson_package_name + '.lexer_generator',
              configure.boson_package_name + '.lexer_generator.regular_parser',
              configure.boson_package_name + '.parser_generator',
              configure.boson_package_name + '.parser_generator.bottom_up_generator',
          ],
          package_data={configure.boson_package_name: [
              '{}/integration/python/*{}'.format(configure.boson_template_directory, configure.boson_template_postfix),
              '{}/integration/python/checker/*{}'.format(configure.boson_template_directory, configure.boson_template_postfix),
              '{}/integration/c++/*{}'.format(configure.boson_template_directory, configure.boson_template_postfix),
              '{}/integration/java/*{}'.format(configure.boson_template_directory, configure.boson_template_postfix),
          ]},
          install_requires=install_requires,
          entry_points={'console_scripts': ['boson = boson.console:console_main']},
          classifiers=['Natural Language :: English',
                       'Programming Language :: Python',
                       'Operating System :: Microsoft :: Windows',
                       'Operating System :: Unix',
                       'Operating System :: MacOS',
                       'Programming Language :: Python :: 3'],
          zip_safe=False)
