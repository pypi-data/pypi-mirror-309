from setuptools import setup, find_packages

setup(
    name='RelativeAbundance',
    version='0.2.3',
    author='Lillian Tatka',
    description="""A package for assessing target engagement via relative abundance""",
    packages=find_packages(), 
    install_requires=[
        'numpy',  
        'pandas',
        'matplotlib'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  
        'Operating System :: OS Independent',
    ],
)
