"""PyPublish : an automated tools to publish my podcast"""

# Always prefer setuptools over distutils
from codecs import open
from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='PyPublish',

    version='1.0.0.dev1',

    description='Automatically process audio file with Auphonic and upload the result to archive.org',
    long_description=long_description,

    url='https://github.com/euterpiaradio/pypublish',

    author='Euterpia Radio',
    author_email='info@euterpiaradio.ch',

    license='CC-BY-NC-SA 4.0',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Podcast publishers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
    ],

    keywords='auphonic internetarchive audio podcast',

    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),

    entry_points={
        'console_scripts': [
            'pypublish=pypublish:main',
            'pyarchive=pyarchive:main',
        ],
    },
    install_requires=['PyYAML', 'pyyaml', 'lxml'],
)
