from setuptools import setup

setup(
    name='webinteract',
    version='1.13',    
    description='A Python module for simple web interaction',
    url='https://blog.pg12.org/web-page-interaction-in-python',
    author='A Andersen',
    author_email='a.andersen@pg12.org',
    license='Modified BSD License',
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
