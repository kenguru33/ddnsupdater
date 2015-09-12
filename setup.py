from setuptools import setup, find_packages

setup(
    name='dnsupdater',
    version='0.2',
    packages=find_packages(),
    url='bernt-anker.com',
    license='GPLv3',
    author='Bernt Anker',
    author_email='bernt.anker@me.com',
    description='Dynamic DNS Updater',
    install_requires=['', ],
    dependency_links=[
        'https://github.com/claneys/pygodaddy/archive/master.zip',
    ],
    entry_points={
        'console_scripts': [
            'gd-dnsupdater=dnsupdater:gd_dnsupdater',
        ],
    },
)
