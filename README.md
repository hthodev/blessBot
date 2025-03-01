# Blockless Bless Network Bot 

## Description
This script automates network or node operations for Blockless Bless Network.

## Features
- **Automated node interaction**
- **Multi account**
- **Multi NodeID**
- **Proxy support**

## Installation

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/hthodev/blessBot.git
   ```
2. Install the necessary dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Register to blockless bless network account first, if you dont have you can register [here](https://bless.network/dashboard?ref=G8Y9MO).
2. To get your `token/user.txt`, follow this step:
	- Login to your bless account in `https://bless.network/dashboard`, make sure you is in this link (dashboard) before go to next step
	- Go to inspect element, press F12 or right-click then pick inspect element in your browser
	- Go to application tab - look for Local Storage in storage list -> click `https://bless.network` and you will see your B7S_AUTH_TOKEN.
	- or you can go Console tab and paste this 
	```bash
	localStorage.getItem('B7S_AUTH_TOKEN')
	```
4. To get your `id` and `hardwareid`, follow this step:
	- Download the [extension](https://chromewebstore.google.com/detail/bless/pljbjcehnhcnofmkdbjolghdcjnmekia)
	- after you download the extension, open `chrome://extensions/?id=pljbjcehnhcnofmkdbjolghdcjnmekia`
  	- Enable `Developer mode` in top right, then press `service worker`, or you can right click the extension windows and use `inspect/inspect element` too. You will see new tab open.
  	![image](https://github.com/user-attachments/assets/63151405-cd49-4dff-9eec-a787a9aa3144)
	- Go to `network` tab, then open the `Bless extension` and login to your account.
  	- After you login to your account, search name with your pubkey (example : `12D3xxxx:hardwareid`), open and copy the `pubkey` and `hardwareid`
	![image](https://github.com/user-attachments/assets/70bcb0c6-9c47-4c81-9bf4-a55ab912fba6)

6. If you want to use `proxy`, you can add in the config file for each proxy.txt.

5. Run the script:
	```bash
	py main.py
	```
***NOTE:***
- **The total time is refreshed every 10minute connection, One account only can have 5 nodeid connected, I recomended to save your Nodeid(pubkey) and hardwareid of your account**
- **Your hardwareinfo data of the nodeid is saved in hardwareInfo.json when you running the script, please do not delete this file. If you add more nodeid or accounts, it will automatically add the data when you start the script**

## Note
This script only for testing purpose, using this script might violates ToS and may get your account permanently banned.

## Warning
Using proxy clean, do not use proxy dirty has been redflag from cloudfare

My reff code if you want to use :) : 
https://bless.network/dashboard?ref=G8Y9MO

## PLEASE GIVE ME A START GITHUB
