from distutils.core import setup

setup(
    name='ddnsupdater',
    version='0.1',
    packages=['ddnsupdater'],
    url='bernt-anker.com',
    license='GPLv3',
    author='Bernt Anker',
    author_email='bernt.anker@me.com',
    description='Dynamic DNS Updater', requires=['pygodaddy',],
    entry_point='gddnsupdate.py',
)
