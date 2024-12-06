# setup.py
from setuptools import setup, find_packages

setup(
    name='mypackageldcss',
    version='0.1',
    packages=find_packages(),
    description='Пример пакета с генераторами, итераторами, декораторами и дескрипторами',
    author='__token__',
    author_email='3529581712@qq.com',
    url='https://pypi.org/project/mypackageldcss/',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
