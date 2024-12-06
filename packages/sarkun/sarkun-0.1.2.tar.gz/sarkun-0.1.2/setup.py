# setup.py
from setuptools import setup, find_packages

setup(
    name="sarkun",  # Package name
    version="0.1.2",          # Version number
    packages=find_packages(),  # Automatically find packages
    include_package_data=True,  # Include non-Python files like README.md, LICENSE, etc.
    install_requires=[       # Dependencies (if any)
        'pyfiglet',
        'colorama',
        'emoji',
    ],
    entry_points={          # Define command-line entry points
        'console_scripts': [
            'sarkun = sarkun.sarkun:main',  # This maps the command "community-tool" to the main() function
        ],
    },
    classifiers=[  # Optional, metadata about your package
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    long_description=open('README.md').read(),  # Read the README file for the long description
    long_description_content_type='text/markdown',  # Markdown format
    url='https://github.com/kaankarakoc42/sarkun',  # URL to your project
    author='Mevlüt Kaan Karakoç',  # Author name
    author_email='karakockaan326@gmail.com',  # Author email
    license='MIT',  # License type
)
