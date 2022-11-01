
import time
import requests
import configparser

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from pushbullet.pushbullet import Pushbullet


USE_SENDGRID = False
SENDGRID_API_KEY = None
USE_PUSHOVER = False
PUSH_TOKEN = None
PUSH_USER = None
USE_PUSHBULLET = False
PUSHBULLET_TOKEN = None
IP = None
REQUESTS_COOLDOWN = 10 * 60 # 10 Minutes


def init_config():
	global REQUESTS_COOLDOWN, USE_SENDGRID, SENDGRID_API_KEY, USE_PUSHOVER, PUSH_TOKEN, PUSH_USER, USE_PUSHBULLET, PUSHBULLET_TOKEN
	config = configparser.ConfigParser()
	config.read('config.ini')

	try:
		requests_cooldown = config.getint("SETTINGS", "REQUESTS_COOLDOWN")
		REQUESTS_COOLDOWN = requests_cooldown
	except (configparser.NoSectionError, KeyError):
		pass

	USE_SENDGRID = config.getboolean("SENDGRID", "USE_SENDGRID")
	SENDGRID_API_KEY = config.get("SENDGRID", "SENDGRID_API_KEY")
	USE_PUSHOVER = config.getboolean("PUSHOVER", "USE_PUSHOVER")
	PUSH_TOKEN = config.get("PUSHOVER", "PUSH_TOKEN")
	PUSH_USER = config.get("PUSHOVER", "PUSH_USER")
	USE_PUSHBULLET = config.getboolean("PUSHBULLET", "USE_PUSHBULLET")
	PUSHBULLET_TOKEN = config.get("PUSHBULLET", "PUSHBULLET_TOKEN")

def get_ip():
	ip = requests.get("https://api.ipify.org").content.decode("utf-8")
	return str(ip)

def send_notification(msg):
    print(f"Sending notification: {msg}")

    if USE_SENDGRID and SENDGRID_API_KEY:
        message = Mail(
            subject="IP Updater",
            html_content=msg)
        try:
            sg = SendGridAPIClient(SENDGRID_API_KEY)
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)

    if USE_PUSHBULLET and PUSHBULLET_TOKEN:
        pb = Pushbullet(api_key=PUSHBULLET_TOKEN)
        pb.push_note("IP Updater", msg)
    
    if USE_PUSHOVER and PUSH_TOKEN:
        url = "https://api.pushover.net/1/messages.json"
        data = {
            "token": PUSH_TOKEN,
            "user": PUSH_USER,
            "message": msg
        }
        requests.post(url, data)

def update_ip():
	global IP

	ip = get_ip()
	if ip == "" or ip == None:
		return

	if ip == IP:
		return

	IP = ip
	send_notification(f"New IP: {IP}")

def main():
	init_config()

	while True:
		update_ip()
		time.sleep(REQUESTS_COOLDOWN)

if __name__ == "__main__":
	main()

