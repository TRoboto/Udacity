# Mac - Initial Setup

### Install Intel® Distribution of OpenVINO™ Toolkit

Refer to [this page](https://docs.openvinotoolkit.org/latest/_docs_install_guides_installing_openvino_macos.html) for more information about how to install and setup the Intel® Distribution of OpenVINO™ Toolkit for MacOS.

### Install Nodejs and its dependencies

- Navigate to the [Node.js download page](https://nodejs.org/en/download/) and install the MacOS version. This should also install `npm` along with `node`. 
- Verify installation in a terminal with `node -v` and `npm -v` (it should show the installed version).

### Install the following dependencies

First, make sure you have [Homebrew](https://brew.sh/) installed on your machine.

Then, download a version of Python 3.5 from [here](https://www.python.org/downloads/). The project code is pre-compiled with the OpenVINO™ Toolkit to best work with Python 3.5. You can then follow the additional steps [here](https://evansdianga.com/install-pip-osx/) to add `pip3` on your Mac (making sure you stick with Python 3.5 - you do not need to install this again).

Next, run the following from the terminal:

```
pip3 install numpy
pip3 install paho-mqtt
brew install cmake
brew install zeromq
```

#### FFmpeg

This project makes use of FFmpeg’s `ffserver` functionality, which was deprecated in an older version. As such, a new install of ffmpeg will not include it if you do it directly from `brew. You can use the below to install the older version containing `ffserver`, as detailed in [this post](https://superuser.com/questions/1296377/why-am-i-getting-an-unable-to-find-a-suitable-output-format-for-http-localho/1297419#1297419).

```
git clone https://git.ffmpeg.org/ffmpeg.git ffmpeg
cd ffmpeg
git checkout 2ca65fc7b74444edd51d5803a2c1e05a801a6023
./configure
make -j4
```

### Install NPM

Follow the instructions in the main README file under “Install npm” to make sure the relevant NPM libraries are installed for the included Node servers.
