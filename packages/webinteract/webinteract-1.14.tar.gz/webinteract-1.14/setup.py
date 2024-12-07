from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='webinteract',
    version='1.14',    
    description='A Python module for simple web interaction',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://blog.pg12.org/web-page-interaction-in-python',
    author='A Andersen',
    author_email='a.andersen@pg12.org',
    license='Modified BSD License',
    license_files = ('LICENSE',),
    packages=['webinteract'],
    install_requires=['splinter',
                      'keyring',                     
                      'selenium',                     
                      'smartinput'],
    classifiers=[
        'License :: OSI Approved :: BSD License',  
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
