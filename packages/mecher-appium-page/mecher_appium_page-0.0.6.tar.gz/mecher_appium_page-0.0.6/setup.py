import os
from setuptools import find_packages
from setuptools import setup

with open('requirements.txt') as f:
    REQUIRES = f.readlines()

setup(
    name='mecher_appium_page',
    version=os.getenv("PACKAGE_VERSION", "0.0.1"),
    description='Universal Appium Page',
    maintainer='mecher',
    url='https://github.com/MaximChernyak98/mecher_appium_page',
    keywords=['testing'],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    dependency_links=[],
    long_description_content_type='text/plain',
    long_description='Universal Appium Page',
    setup_requires=['setuptools-git-versioning'],
)
