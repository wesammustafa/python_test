# Testing Scripts for Taxi
Testing scripts for covering taxi app scenarios:
  * Create driver
  * Change Status
  * Change Location
  * Check driver inside and outside areas
  * Create customer 
  * Complete booking cycle using manual dispatch

## Getting Started
These instructions will get you ready for running testing scripts on your local machine for testing purposes.

### Prerequisites
- python3.7 you can install it through this link [Python Installation](https://tecadmin.net/install-python-3-7-on-ubuntu-linuxmint/)
- pip3 you can install it through this link [pip Installation](https://linuxize.com/post/how-to-install-pip-on-ubuntu-18.04/)
- create your own virtual environment through this link [Virtual Env Installation](https://gist.github.com/Geoyi/d9fab4f609e9f75941946be45000632b)

### Installing and running
- Activate your virtual env
- Install need packages using the command ``` pip install -r requirements.txt ```
- Run all test scripts using the command ```pytest -v -s```
- Run specific script using the command ```pytest [script name] -v -s```
- Run specific test using the command ```pytest [script name]::[test name] -v -s```

Note:
  - please, don't forget to put the abbreviations ```-v -s``` in the previous command