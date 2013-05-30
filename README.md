# Cloud X Cloud
### By: Siddhant Mutha and Shantanu Gupta

This a project which we had made for **Yahoo! HackU 2013** at IIT Madras

In this, we basically have a single client for both **Dropbox** and **Google Drive**.
You can view, upload, download files from each of these services and also transfer files in between them.
There is another feature called **Magic** in which you simply drop the file and based on various parameters (currently only free space), it is decided where to put the file.

The software is based has been developed in Python using Dropbox and Drive APIs. We used the Qt framework (using PySide) to develop the GUI.

## Pre-requisites
* PySide
* Dropbox Python API
* Google Drive API

In the `dropbox_down.py` file insert your Dropbox `APP_KEY` and `APP_SECRET` appropriately.
Similarly, in the `drive_down.py` insert your Google Developers `CLIENT_KEY` AND `CLIENT_SECRET` appropriately.

## Running
Run it as `python main.py`
Initially, two web browser windows will open: one for Dropbox and another for Drive.
For the Dropbox one, simply grant permission to the app in the browser and press Enter in the command line.
Now, the Drive page will open. Grant permission, copy the code which is shown to the command line and press Enter.

You're now good to go!
