import logging
import dns.resolver
import schedule
import time
import requests
from dotenv import load_dotenv
import os

load_dotenv()
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

previous_dns = {}

# Setup logging
logging.basicConfig(
    filename='dns_lookup.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def send_discord_alert(message):
    payload = {"content": message}
    try:
        requests.post(DISCORD_WEBHOOK_URL, json=payload)
    except Exception as e:
        error_msg = f"Failed to send Discord alert: {e}"
        print(error_msg)
        logging.error(error_msg)

def log_dns_resolution(domain):
    global previous_dns
    try:
        answers = dns.resolver.resolve(domain, 'A')
        current_ips = [rdata.address for rdata in answers]
        current_ttl = answers.rrset.ttl

        result = f"Resolved {domain} to {current_ips} with TTL {current_ttl}"
        print(result)
        logging.info(result)
        
        prev = previous_dns.get(domain)
        if prev:
            if prev['ips'] != current_ips:
                msg = f"DNS Change for {domain}: IPs changed from {prev['ips']} to {current_ips}"
                send_discord_alert(msg)
                logging.warning(msg)
            elif current_ttl < prev['ttl']:
                msg = f"TTL dropped for {domain}: from {prev['ttl']} to {current_ttl}"
                send_discord_alert(msg)
                logging.warning(msg)

        previous_dns[domain] = {'ips': current_ips, 'ttl': current_ttl}

    except dns.resolver.NXDOMAIN:
        error_msg = f"Domain {domain} does not exist"
        print(error_msg)
        logging.error(error_msg)
    except dns.resolver.Timeout:
        error_msg = f"DNS query for {domain} timed out"
        print(error_msg)
        logging.error(error_msg)
    except dns.resolver.NoAnswer:
        error_msg = f"No DNS answer for {domain}"
        print(error_msg)
        logging.error(error_msg)

def main():
    domains = [
        "google.com",
        "openai.com",
        "apple.com"
    ]

    for domain in domains:
        log_dns_resolution(domain)

if __name__ == "__main__":
    if not DISCORD_WEBHOOK_URL:
        raise ValueError("DISCORD_WEBHOOK_URL is not set in .env file")

    schedule.every(5).minutes.do(main)

    while True:
        schedule.run_pending()
        time.sleep(1)