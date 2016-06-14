# -*- coding: utf-8 -*-
# setup.py
# Copyright (C) 2016 Kali Kaneko
# Everyone is permitted to copy and distribute verbatim or modified
# copies of this license document, and changing it is allowed as long
# as the name is changed.

# DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
# TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
# 0. You just DO WHAT THE FUCK YOU WANT TO.

from setuptools import setup


trove_classifiers = [
    "Development Status :: 3 - Alpha",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.7",
    "Topic :: Utilities"
]

killit = 'killit=killit:main'

setup(
    name='killit',
    version='0.0.1',
    url='https://github.com/kalikaneko/killit',
    license='WTFPL',
    author='Kali Kaneko',
    author_email='kali@leap.se',
    maintainer='Kali Kaneko',
    maintainer_email='kali@leap.se',
    description='Kill it with fire',
    classifiers=trove_classifiers,
    install_requires=['urwid', 'psutil'],
    entry_points={
        'console_scripts': [killit]
    },
)
