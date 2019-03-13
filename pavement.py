#!/usr/bin/python

from paver.easy import *
import paver.doctools
import os
import glob
import shutil
import sys

sys.path.append(os.path.dirname(__file__))


@task
def setup():
  sh('python3 setup.py -q install')
  pass

@task
def test():
  sh('nosetests --with-coverage --cover-erase --cover-branches --cover-html --cover-package=src test')
  pass

@task
def run():
  sh('python3 -m src.driver.driver airportcodes.txt')
  sh('python3 -m src.driver.driver airportcodeswerr.txt')

@task
def clean():
  for pycfile in glob.glob("*/*/*.pyc"): os.remove(pycfile)
  for pycache in glob.glob("*/__pycache__"): os.removedirs(pycache)
  for pycache in glob.glob("./__pycache__"): shutil.rmtree(pycache)
  try:  
    shutil.rmtree(os.getcwd() + "/cover")
  except:
    pass
  pass

  
@task
@needs(['setup', 'clean', 'test'])
def default():
  pass
