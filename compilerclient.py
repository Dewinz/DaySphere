import PyInstaller.__main__

PyInstaller.__main__.run([
    '--noconsole',
    '-n=DaySphere',
    '-i=.\\assets\\logo@4x.ico',
    '.\\__start__.py',
])