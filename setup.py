import sys
from cx_Freeze import Executable, setup

base = 'Win32GUI' if sys.platform == 'win32' else None

executables = [Executable('main.py',
                          targetName='Moth.exe',
                          base=base,
                          shortcutName='Moth',
                          shortcutDir='moth_game'
                          )]

includes = ['pygame']

excludes = []

zip_include_packages = []


include_files = ['data', 'levels', 'main_code', 'ui']

options = {
    'build_exe': {
        'include_msvcr': True,
        'excludes': excludes,
        'includes': includes,
        'zip_include_packages': zip_include_packages,
        'include_files': include_files,
    }
}

setup(name='Moth',
      version='1.0',
      description='just moth',
      executables=executables,
      options=options)
