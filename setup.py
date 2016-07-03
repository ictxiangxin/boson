import boson.bs_configure as configure
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

install_requires = [
    "jinja2>=2.7",
]

if __name__ == "__main__":
    long_description = "%s - %s" % (configure.boson_title, configure.boson_description)

    setup(name=configure.boson_package_name,
          version="%d.%d" % (configure.boson_version_main, configure.boson_version_sub),
          url=configure.boson_url,
          license=configure.boson_license,
          author=configure.boson_author,
          author_email=configure.boson_author_email,
          maintainer=configure.boson_author,
          maintainer_email=configure.boson_author_email,
          description=configure.boson_description,
          long_description=long_description,
          platforms=["MS Windows", "Mac X", "Unix/Linux"],
          keywords=[configure.boson_package_name, configure.boson_description],
          packages=[configure.boson_package_name],
          package_data={configure.boson_package_name: ["%s/*%s" % (configure.boson_template_directory, configure.boson_template_postfix)]},
          install_requires=install_requires,
          entry_points={"console_scripts": ["boson = boson.boson:boson_main"]},
          classifiers=["Natural Language :: English",
                       "Programming Language :: Python",
                       "Operating System :: Microsoft :: Windows",
                       "Operating System :: Unix",
                       "Operating System :: MacOS",
                       "Programming Language :: Python :: 3"],
          zip_safe=False)
