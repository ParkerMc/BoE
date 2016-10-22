from distutils.core import setup
import py2exe, sys, os

sys.argv.append('py2exe')
sys.path.insert(0, "C:/Python27/Lib/site-packages/PyQt4")
BoE_data_files = []
for folder in ['ui', 'assets']:
    for files in os.listdir(folder):
        f1 = os.path.join(folder , files)
        if os.path.isfile(f1): # skip directories
            f2 = folder, [f1]
            BoE_data_files.append(f2)
            
setup(
    options = {'py2exe': {'bundle_files': 1, 'compressed': True}},
    windows = [
        {
            "script": "client.py",
            "icon_resources": [(1, "assets/BoE.ico")]
        }
    ],
    zipfile = None,
    data_files = BoE_data_files,
    
)
