# IP-Updater

This script is meant to be run as a service on a server that doesn't have a static IP or DNS.
When the ISP dynamically allocates a new IP at random, this script will send an update message of the new IP using different APIs.
I mostly use PushBullet to receive a notification on my phone that the IP was changed (incase I need to access my raspberry pi at home).