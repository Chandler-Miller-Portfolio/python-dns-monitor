# DNS Monitor for Discord Alerts
This Python script periodically checks the A records (IPv4 addresses) of specified domains, logs their IPs and TTL values, and sends Discord alerts if there's a change in IPs or a drop in TTL. It’s ideal for monitoring DNS propagation, TTL changes, or potential DNS hijacking.

## Features
- Periodically checks DNS A records for a list of domains.
- Logs results to `dns_lookup.log`.
- Sends alerts to a Discord channel using a web-hook if:
- IP addresses change.
- TTL drops.
- Built in error handling for common DNS exceptions.

## Requirements
Python 3.7+
`dnspython`
`schedule`
`requests`
`python-dotenv`

You can install the dependencies with:

`pip install -r requirements.txt`

Or manually:

`pip install dnspython schedule requests python-dotenv`

## Setup
1. Clone the repository.

2. Create a `.env` file in the same directory as the script with the following content:
`DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/your-webhook-url`

3. (Optional) Modify the list of domains in the main() function to suit your needs:

```
domains = [

"google.com",

"openai.com",

"apple.com"

]
```

## Usage
Run the script using Python:

`python dns_monitor.py`

It will:
- Perform a DNS check for each domain every 5 minutes.
- Log each result to `dns_lookup.log`
- Send a Discord alert if a domain's IPs change or TTL drops.

## Log Example

```
2025-04-02 14:03:01,412 - INFO - Resolved google.com to ['142.250.72.14'] with TTL 299
2025-04-02 14:08:01,560 - WARNING - DNS Change for google.com: IPs changed from ['142.250.72.14'] to ['142.250.72.78']
```

## Notes
- The script uses a blocking loop (`while True`) with 1-second sleeps for scheduling. You may adapt this for async use or containerization if needed.
- It currently only checks A records; feel free to expand it to support AAAA, MX, etc.