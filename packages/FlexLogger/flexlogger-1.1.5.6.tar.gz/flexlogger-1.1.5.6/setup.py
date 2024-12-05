from setuptools import setup, find_packages


setup(
    name='FlexLogger',
    version='1.1.5.6',
    packages=find_packages(),
    description='Wrapper for remote logging to a Database with the help of an API REST.',
    author='Anderson',
    author_email='anderbytes@gmail.com',

    long_description_content_type="text/markdown",

    install_requires=[
        "requests~=2.32.3",
        "fastapi~=0.115.5"
    ]
)
