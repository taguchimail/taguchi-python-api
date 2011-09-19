from setuptools import setup

setup(
    name='taguchi-api',
    version='1.0dev1',
    packages=['taguchi'],
    scripts=['bin/taguchi-client'],

    # meta
    author='TaguchiMarketing Pty Ltd',
    author_email='support@taguchimail.com',
    url='https://github.com/taguchimail/taguchi-python-api',
    license='LICENSE.txt',
    description='Taguchi HTTP API wrappers.',
    long_description=open('README.rst').read(),
)
