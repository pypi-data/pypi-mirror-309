# jzsk_runid_build/setup.py 

from setuptools import setup, find_packages

setup(
    name='jzsk_runid',
    version='0.0.3',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'mlflow==2.14.1',
        'numpy',
        'oss2==2.19.1'
    ],
    author='zsp',
    author_email='465620024@qq.com',
    description='runid build for jzsk'
)