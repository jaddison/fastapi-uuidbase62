#!/usr/bin/env python

from distutils.core import setup

setup(name='fastapi-uuidbase62',
      version='0.1',
      description='Leverage Stripe-formatted IDs for internal UUID values in your Pydantic models and FastAPI views; automatically validates prefixes, and converts to/from UUID values.',
      author='James Addison',
      author_email='addi00@gmail.com',
      url='',
      packages=['uuidbase62'],
      python_requires='>=3.6, <4',
      install_requires=['fastapi']
      )
