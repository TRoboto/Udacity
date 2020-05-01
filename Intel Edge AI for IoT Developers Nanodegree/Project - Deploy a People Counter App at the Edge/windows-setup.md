# Windows - Initial Setup

### Install the Windows Subsystem for Linux (WSL)

To get started, install the [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10). Select the Ubuntu 16 distribution.

Make sure to follow the instructions on the [Initialize a Distribution](https://docs.microsoft.com/en-us/windows/wsl/initialize-distro) page as well, especially the following command with the terminal window:

```
sudo apt update && sudo apt upgrade
```

This will allow you to essentially work within the Linux environment for your project. To make it easier to work with various commands, we suggest within the WSL terminal to right-click the menu bar, select “Properties”, and "Use Ctrl+Shift+C/V As Copy/Paste", so you can paste into the terminal (make note of the “Shift” included in this command vs. just `Ctrl+C` or `Ctrl+V`).

Next, you’ll follow the Linux Setup instructions, but do note there are a couple of additional notes before moving on from the OpenVINO™ Toolkit installation in the Linux Setup instructions:

1. Use your normal browser in Windows to navigate to the OpenVINO™ installation website. Once you get a link to download OpenVINO™ **for Linux** (right-click on the full package download and copy the link over), use `wget` within the WSL terminal to download it.

    ```
    wget {openvino download URL}
    ```

    Note that this will download the `.tgz` file in your current directory. You can then further follow the Linux instructions to extract and install these files.

2. Note that when you run the verification scripts at the end of installing OpenVINO™, the WSL terminal will not allow the second script to open a display window. As long as the first script runs fine and the second script only fails at displaying the window, everything should be installed fine.

### Install NPM

Follow the instructions in the main README file under “Install npm” to make sure the relevant NPM libraries are installed for the included Node servers.

### Use Visual Studios with WSL

So far, you have been stuck working from the WSL terminal, and likely don’t want to edit all your code from within there. You can follow the instructions [here](https://code.visualstudio.com/docs/remote/wsl) to link the Visual Studios IDE to WSL, and allow you to edit your code files outside of the terminal window.

### Other WSL Questions

If you have additional questions specific to using WSL, see the FAQ [here](https://docs.microsoft.com/en-us/windows/wsl/faq).
