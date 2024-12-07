# jzsk_runid_build/setup.py 

from setuptools import setup, find_packages

setup(
    name='jzsk_runid_build',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'mlflow',
        'numpy',
        'oss2'
    ],
    author='zsp',
    author_email='465620024@qq.com',
    description='runid build for jzsk'
)