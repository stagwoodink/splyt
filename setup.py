from setuptools import setup, find_packages

setup(
    name='splyt',
    version='0.1.0',
    author='Xandr Stagwood',
    author_email='stagwoodink@gmail.com',
    description='A command-line tool to split images into grid sections.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/stagwoodink/splyt',
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=[
        'Pillow>=8.0.0',
    ],
    entry_points={
        'console_scripts': [
            'splyt=splyt.cli:main',
        ],
    },

    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Update if using a different license
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
