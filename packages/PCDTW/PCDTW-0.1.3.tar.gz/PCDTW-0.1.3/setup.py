from setuptools import setup, find_packages

setup(
    name='PCDTW',
    version='0.1.3',
    packages=find_packages(),
    install_requires=['numpy','pandas','dtaidistance'],  # List your package dependencies here
    author='Jamie Dixson',
    author_email='realtorjamied@gmail.com',
    description='This package has functions for the conversion of amino acid sequences to physicochemical vectors and the subsequent analysis of those vector sequences.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/JamberFX/PCDTWPackage',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
