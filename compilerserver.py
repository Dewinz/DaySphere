import PyInstaller.__main__

PyInstaller.__main__.run([
    '--onefile',
    '-n=DaySphere Server',
    '-i=.\\assets\\logo@4x.ico',
    '.\\communication\\server.py',
])