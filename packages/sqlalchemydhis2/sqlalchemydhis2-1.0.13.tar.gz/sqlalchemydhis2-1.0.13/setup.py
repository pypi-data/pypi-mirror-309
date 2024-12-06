import os
import re

from setuptools import setup, find_packages

v = open(
    os.path.join(os.path.dirname(__file__), "sqlalchemy_dhis2", "__init__.py")
)
VERSION = re.compile(r'.*__version__ = "(.*?)"', re.S).match(v.read()).group(1)
v.close()

readme = os.path.join(os.path.dirname(__file__), "README.md")


setup(
    name="sqlalchemydhis2",
    version=VERSION,
    description="DHIS2 API for SQLAlchemy",
    long_description=open(readme).read(),
    long_description_content_type="text/markdown",
    url="https://github.com/talexie/sqlalchemy_dhis2",
    author="Alex Tumwesigye",
    author_email="atumwesigye@gmail.com",
    license="Apache-2.0",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Database :: Front-Ends",
        "Operating System :: Microsoft :: Windows",
    ],
    keywords="SQLAlchemy DHIS2",
    project_urls={
        "Documentation": "https://github.com/talexie/sqlalchemy_dhis2/wiki",
        "Source": "https://github.com/talexie/sqlalchemy_dhis2",
        "Tracker": "https://github.com/talexie/sqlalchemy_dhis2/issues",
    },
    packages=find_packages(include=["sqlalchemy_dhis2"]),
    include_package_data=True,
    install_requires=["SQLAlchemy", "duckdb", "polars"],
    zip_safe=False,
    entry_points={
        "sqlalchemy.dialects": [
            "dhis2 = sqlalchemy_dhis2.jsonhttp_dialect:JSONHTTPDialect",
        ]
    },
)