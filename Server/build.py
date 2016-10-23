from distutils.core import setup
import py2exe, sys, os

sys.argv.append('py2exe')

BoE_data_files = []
for folder in ['chat/Main']:
    for files in os.listdir(folder):
        f1 = os.path.join(folder , files)
        if os.path.isfile(f1): # skip directories
            f2 = folder, [f1]
            BoE_data_files.append(f2)

setup(
    options = {'py2exe': {'bundle_files': 1, 'compressed': True, 'dll_excludes': ['w9xpopen.exe', 'mpr.dll', 'crypt32.dll']}},
    windows = [
        {
            "script": "server.py",
            "icon_resources": [(1, "../Client-Python/assets/BoE.ico")],
            "dest_base" : "BoE-sever"
        }
    ],
    zipfile = None,
    data_files = BoE_data_files,

)
