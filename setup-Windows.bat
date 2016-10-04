python -m pip install -r requirements.txt
IF %PROCESSOR_ARCHITECTURE% == x86 (
powershell -Command "(New-Object Net.WebClient).DownloadFile('https://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.11.4/PyQt4-4.11.4-gpl-Py2.7-Qt4.8.7-x32.exe/download', 'pyqt.exe')")
IF %PROCESSOR_ARCHITECTURE% == AMD64 (
powershell -Command "(New-Object Net.WebClient).DownloadFile('https://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.11.4/PyQt4-4.11.4-gpl-Py2.7-Qt4.8.7-x64.exe/download', 'pyqt.exe')")
pyqt.exe