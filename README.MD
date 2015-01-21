This gui app I created for personal usage. Use it to create query of music files on selected directory, parsing lyrics from lyrics.wikia.com and fill tags.

###Requirements
- wxPython
- Beautiful Soup

###Install dependencies for wxPython
Need to install the required packages with development tools (c++ compiler, python) and related libraries (gtk2 and optionally webkit, jpg, tiff, opengl, etc.). [Original article].

For Debian 6.0:
```sh
su apt-get install dpkg-dev build-essential swig python-dev libwebkit-dev libjpeg-dev libtiff-dev checkinstall freeglut3 freeglut3-dev libgtk2.0-dev  libsdl1.2-dev libgstreamer-plugins-base0.10-dev
```
For Ubuntu 12.04+:
```sh
sudo apt-get install dpkg-dev build-essential swig python2.7-dev libwebkitgtk-dev libjpeg-dev libtiff-dev checkinstall ubuntu-restricted-extras freeglut3 freeglut3-dev libgtk2.0-dev  libsdl1.2-dev libgstreamer-plugins-base0.10-dev
```

###Configure and Build wxPython 3.0

Download, uncompress and create build directory:
```sh
wget http://downloads.sourceforge.net/wxpython/wxPython-src-3.0.0.0.tar.bz2
tar xvjf wxPython-src-3.0.0.0.tar.bz2
cd wxPython-src-3.0.0.0/
mkdir bld && cd wxPython/
```
Build and install:
```sh
sudo checkinstall -y --pkgname=wxpython --pkgversion=3.0.0 --pkgrelease=1 --pkglicense=wxWidgets --pkgsource=http://www.wxpython.org/ --maintainer=reingart@gmail.com --requires=python-wxversion,python2.7,python -D  python build-wxpython.py --build_dir=../bld --install
```
You can check your installation in a python terminal:
```sh
>>> import wx
>>> wx.version()
'3.0.0.0 gtk2 (classic)'
```

### Installing Beautiful Soup
```sh
pip install beautifulsoup4
```
Or if u wanna install this with the system package manager:
```sh
apt-get install python-bs4
```

[original article]:http://wiki.wxpython.org/CheckInstall