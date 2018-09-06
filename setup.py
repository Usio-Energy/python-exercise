from setuptools import setup, find_packages
from setuptools.command.install import install
import os


class Schedule(install):
    def run(self):
        install.run(self)
        os.system("echo 'Adding daily run to crontab'")
        os.system("crontab -l > tmpcron")
        os.system("echo '0 9 * * * /usr/bin/env fixercise' >> tmpcron")
        os.system("crontab tmpcron")
        os.system("rm tmpcron")


setup(
    name='fixercise',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
        'appdirs',
    ],
    entry_points='''
        [console_scripts]
        fixercise=fixercise.retrieval:run
    ''',
    cmdclass={'install': Schedule},
)