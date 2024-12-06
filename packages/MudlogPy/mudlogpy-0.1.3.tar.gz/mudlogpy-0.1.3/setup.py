from setuptools import find_packages, setup

setup(
    name='MudlogPy',
    packages=find_packages(include=['MudlogPy']),
    version='0.1.3',
    description='This library plots the mudlog having gas chromatograph and lithology logs',
    author='Landmark Resources Reservoir Characterization Department',
    install_requires=[],
    setup_requires=['numpy','lasio','matplotlib'],
    tests_require=['numpy==1.26.4','lasio==0.31','matplotlib==3.7.5']
)