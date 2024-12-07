# Installation

## pip install (Linux, macOS & Windows)

This method should work with a number of Python versions, but **we strongly recommend that you use Python 3.10**. Older Python versions are no longer tested and may not work correctly. Newer Python versions may not have wheels for all required dependencies. For Linux the [install script](#install-script-linux) is recommended.

You can install psychopy-bids and its dependencies by:

```console
pip install psychopy-bids
```

If you prefer _not_ to install _all_ the dependencies (e.g. because the platform or Python version you’re working on doesn’t have that dependency easily available) then you could do:

```console
pip install psychopy-bids --no-deps
```

For further information on pip visit [pip install - pip documentation](https://pip.pypa.io/en/stable/cli/pip_install/).

## Standalone PsychoPy (macOS & Windows)

For the simplest installation, download and install the standalone package. You can find all versions on [PsychoPy releases on github](https://github.com/psychopy/psychopy/releases). **Use at least version 2023.1.0 or later**.

First, start PsychoPy and select **Plugin/packages manager...** from the Tools menu.

![Tools](img/inst-fig01.png)

There are now three different ways in which you can install psychopy-bids.

![Plugins & Packages](img/inst-fig02.png)

- **Option 1 - Search package (Recommended):** Search for _psychopy-bids_ using the search bar. Then select the package below, decide which version you want to install and click _Install_ to complete the process.
- **Option 2 - Install from file:** Click _Install from File_, locate the wheel file on your computer and click _Open_ to install the package.
- **Option 3 - Open PIP terminal:** Click _Open PIP terminal_, type `pip install psychopy-bids` into the command prompt and wait for the package to install successfully.

### Older Standalone PsychoPy versions (Windows)

If you are using a standalone PsychoPy version older than 2023.1.0, you need to install psychopy-bids differently. First, open your terminal. To do this

1. Select the Start button.
2. Type "cmd".
3. Select Command Prompt from the list.

To avoid possible problems, it is best to start Command Prompt as administrator.

![Command Prompt](img/inst-fig03.png)

To install **psychopy-bids** use `"<path>\python.exe" -m pip install psychopy-bids`. If you have installed PsychoPy to the standard installation folder, your path is most likely going to be `C:\Program Files\PsychoPy`. In this case, you would run the command `"C:\Program Files\PsychoPy\python.exe" -m pip install psychopy-bids`.

## Anaconda and Miniconda (Linux, maxOS & Windows)

For information on how to start conda visit [Getting started with conda](https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html#starting-conda).

We provide an [environment file](files/psychopy_bids-env.yml) that can be used to install psychopy-bids and its dependencies. Download the file, open your terminal (or Anaconda Prompt if you are using Windows), navigate to the directory you saved the file to, and run:

```console
conda env create -n psychopy-bids -f psychopy_bids-env.yml
```

This will create an environment named `psychopy-bids`.  To activate the newly-created environment and run PsychoPy with the psychopy-bids plugin, execute:

```console
conda activate psychopy-bids
psychopy
```

## Install script (Linux)

```bash
 curl -O https://raw.githubusercontent.com/wieluk/psychopy_linux_installer/main/psychopy_linux_installer
 chmod +x psychopy_linux_installer
 ./psychopy_linux_installer --additional-packages==psychopy-bids,seedir
```

[More information on GitHub](https://github.com/wieluk/psychopy_linux_installer)

## Post-Installation Steps

### Check PsychoPy Preferences

Select **Preferences** from the File menu. In the **General** menu, check to see if psychopy-bids is called at **start up plugins**. If not, add it and click OK. You will then need to restart the Builder for the changes to take effect.

![PsychoPy Preferences](img/inst-fig04.png)

### Use the Components

As you can see in the next figure the **BIDS Beh Event component**, the **BIDS Task Event component** and the **BIDS Export routine** are now available and ready to use.

![PsychoPyBuilder](img/inst-fig05.png)
