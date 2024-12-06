from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Ripoff Numpy'
LONG_DESCRIPTION = 'A library for manipulating matrices while boiling your RAM'

# Setting up
setup(
        name="MARtrix", 
        version=VERSION,
        author="Ram",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[],

        keywords=['python', 'matrices'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)