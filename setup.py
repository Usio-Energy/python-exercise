from setuptools import setup, find_packages

setup(
    name='Fixercise Exchange Rate Retrieval',
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
)