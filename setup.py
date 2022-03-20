#!/usr/bin/env python

from setuptools import setup
from pathlib import Path

try:
    current_directory = Path(__file__).parent
    long_description = (current_directory / "README.md").read_text()
except:
    long_description = ""

setup(
    name='fastapi-uuidbase62',
    version='0.2',
    description='Leverage Stripe-formatted IDs for internal UUID values in your Pydantic models and FastAPI views; automatically validates prefixes, and converts to/from UUID values.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='James Addison',
    author_email='addi00@gmail.com',
    url='https://github.com/jaddison/fastapi-uuidbase62',
    project_urls={
        'Documentation': 'https://github.com/jaddison/fastapi-uuidbase62',
        # 'Funding': 'https://donate.pypi.org',
        'Say Thanks!': 'https://github.com/jaddison/fastapi-uuidbase62/issues',
        'Source': 'https://github.com/jaddison/fastapi-uuidbase62',
        'Tracker': 'https://github.com/jaddison/fastapi-uuidbase62/issues',
    },
    packages=['uuidbase62'],
    keywords='stripe uuid base62 fastapi pydantic serialize',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: FastAPI',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
    ],
    python_requires='>=3.7, <4',
    install_requires=['fastapi']
)
