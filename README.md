# Simple Oauth 2.0 Authorisation with Python (For Google Search Console)

## Overview

This script should be used as a starting point for those who want to play with Pythong and the Google Search Console (GSC) API. I have attempted to keep some form of logical folder structure in place while also removing as much unnecessary code as possible; the script only allows you ton log in, see the profiles you have access to and to log out again.

## Folder structure and files

* `/` - Entry, houses `main.py`
  * `/src` - Houses all code
    * `client_secret.json` - Client secret (not in repo due to security) that can be obtained from [Google Cloud Console - Credentials](https://console.cloud.google.com/apis/credentials)
    * `/utils` - All helper functions
      * `authorise.py` - Authorisation process (for Oauth 2.0)

> **Warning**: Please note you will have to obtain and create a `client_secret.json` in the `/src` folder!

## Google admin

You will have to do some admin in Google to obtain a client secret.

1. Create a project in [Google Cloud Console - Credentials](https://console.cloud.google.com/apis/credentials)
2. Create OAUTH 2.0 Client ID
  * Type is desktop
3. Download the client secret (`client_secret.json`)
4. Move the client secret to the `/src` folder
5. Configure the OAuth consent screen to your liking

## Running

The tool currently opens a Flask local server on port `:8080`. You can start the application by navigating to the folder that contains the `main.py` file and xecute the `python3 main.py` command.

## Notes

### Language used

* Python3

## Creator

Kevin Ellen

