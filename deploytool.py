#!/usr/bin/python

import os
import sys
import json
import glob
from subprocess import call


def get_app_version(filename):
  data = json.load(open(filename))
  return data['version']


def get_remote_version(user, repo):
  print('Getting remote version')

  filename = 'package.json'
  os.chdir('/tmp')
  call(['wget', 'https://raw.githubusercontent.com/' + user + '/' + repo + '/master/' + filename, '-O', filename])
  return get_app_version(filename)


def checkout(repo):
  if os.path.isdir(repo) and os.path.exists(repo + '/' + 'package.json'):
    print('Updating')
    os.chdir(repo)
    call(['git', 'pull'])
  else:
    print('Checkout')
    call(['git', 'clone', git_path])


def install_dependencies():
  print('Installing dependencies')
  call(['npm', 'install'])


def build():
  print('Cleaning dist/')
  call(['rm', '-f', 'dist/*.exe'])
  call(['rm', '-f', '*dist/.AppImage'])
  print('Building')
  call(['npm', 'run', 'dist'])
  call(['npm', 'run', 'win32'])


def deploy(src_dir, dest_dir, app_version):
  call(['mkdir', '-p', dest_dir])
  os.chdir(dest_dir)
  call(['mkdir', '-p', app_version ])

  print('Copying to ' + dest_dir + app_version)
  os.chdir(src_dir + '/dist')
  try:
    call(['mv', glob.glob('*.AppImage')[0], dest_dir + app_version + '/electron-atm-x86_64.AppImage'])
  except IndexError:
    pass

  try:
    call(['mv', glob.glob('*.exe')[0], dest_dir + app_version + '/electron-atm-setup.exe'])
  except IndexError:
    pass


if __name__ == '__main__':
  user = 'timgabets'
  repo = 'electron-atm'
  tmp_dir = '/tmp/'
  dest_dir = '/var/www/atmtools.org/html/dist/' + repo + '/'

  os.chdir(tmp_dir)

  version = get_remote_version(user, repo)
  print('Remote version: ' + version)

  if os.path.exists(dest_dir + version):
    print('App version ' + version + ' is already built in ' + dest_dir + version)
    sys.exit()

  checkout(repo)
  install_dependencies()
  build()
  deploy(tmp_dir + repo, dest_dir, version)



