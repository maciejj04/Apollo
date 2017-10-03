# Apollo
IDE: Pycharm
// TODO: program versions used in project


Run project by:
	- python go.py [ audioFile ]


Full env setup:
1. python 3.6.2 version
	- add Pythons folder path to system PATH variable,

2. Install SIP which is needed for Python bindings for QT:
	- pip3 install sip

3. Install PyQt4 - You may use 'PyQt4-4.11.4-cp36-cp36m-win_amd64.whl' file which is included in project files, 
   or download it from: http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyqt4.
	- pip install PyQt4-4.11.4-cp36-cp36m-win_amd64.whl
4. Install pyqtgraph widget - You may use 'pyqtgraph-0.10.0.win-amd64.exe' file which is included in project files, 
   or download it from: http://www.pyqtgraph.org/
   	- pyqtgraph-0.10.0.win-amd64.exe

5. Install NumPy - You may use 'numpy-1.13.1-cp36-none-win_amd64' file which is included in project files, 
   or download it from: https://pypi.python.org/pypi/numpy.
	- pip install numpy-1.13.1-cp36-none-win_amd64

6.  Install PuAudio - You may use 'PyAudio-0.2.11-cp36-cp36m-win_amd64.whl' file which is included in project files, 
   or download it from: https://pypi.python.org/pypi/PyAudio#downloads
	- pip install PyAudio-0.2.11-cp36-cp36m-win_amd64.whll

	
	
Troubleshoot:
	In case of: ImportError: DLL load failed: %1 nie jest prawidłową aplikacją systemu Win32.
		- pip uninstall pyqt4
		- pip install pyqt4 ^^ 
		
	This is because QtGui file was modified (why) and have - bytes.

