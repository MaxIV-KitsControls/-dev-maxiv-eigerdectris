#!/usr/bin/env python

from setuptools import setup

setup(name = "tangods-eigerdectris",
      version = "0.4.0",
      description = "Device server for the Eiger detector",
      packages =['dectris_eiger'],
      py_modules=['EigerDectris'],
      scripts = ['scripts/EigerDectris']
     )
