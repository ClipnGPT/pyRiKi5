#https://github.com/pyinstaller/pyinstaller/pull/3888/files

#-----------------------------------------------------------------------------
# Copyright (c) 2017-2018, PyInstaller Development Team.
#
# Distributed under the terms of the GNU General Public License with exception
# for distributing bootloader.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

from PyInstaller.utils.hooks import copy_metadata
datas = copy_metadata('google-cloud-speech')

