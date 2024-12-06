from setuptools import find_packages
from setuptools import setup

with open('requirements.txt') as f:
    REQUIRES = f.readlines()

setup(
    name='mecher_appium_page',
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
    setuptools_git_versioning={
        "enabled": True,
        "count_commits_from_version_file": True,  # enable commits tracking
        "dev_template": "{tag}.dev{ccount}",  # suffix for versions will be .dev
        "dirty_template": "{tag}.dev{ccount}",  # same thing here
    },
    setup_requires=['setuptools-git-versioning'],
)
