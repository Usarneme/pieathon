# Hackernews scraper and analysis

Respect the robots.txt for ycombinator https://news.ycombinator.com/robots.txt:
```
User-Agent: *
Crawl-delay: 30
Disallow: /collapse?
Disallow: /context?
Disallow: /flag?
Disallow: /login
Disallow: /logout
Disallow: /r?
Disallow: /reply?
Disallow: /submitlink?
Disallow: /vote?
Disallow: /x?
```

Basically, don't run the script more than once every 30 seconds and don't touch those disabllowed directories. I am setting this up as a once-daily cronjob on a Mac using launchctl as follows:


1. clone this repository:
`git clone https://github.com/Usarneme/pieathon/`

2. Enter the cloned directory and get the path to the python script:
`cd pieathon`
`pwd` should output the full path to the script, for me it is at `/Users/usarneme/Projects/pieathon/scrape.py`

3. Get the path to your python3 binary file is correct:
`which python3` should output the full directory, for me it is at `/usr/local/bin/python3`

4. Create a .plist XML file with `nano ~/Library/LaunchAgents/hackernews.scraper.plist`

```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>hackernews.scraper</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/python3</string>
        <string>/Users/usarneme/Projects/pieathon/scrape.py</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>11</integer>
        <key>Minute</key>
        <integer>16</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/Users/usarneme/Library/Logs/hackernews_scraper.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/usarneme/Library/Logs/hackernews_scraper.log</string>
</dict>
</plist>
```

You can use different hour and minutes. Mine is set up to run at 11:16am each day.
You can also use a different place to store log files. It should create the file on first run if it didn't previously exist but it couldn't hurt to `touch /Users/usarneme/Library/Logs/hackernews_scraper.log` to create the file ahead of time.

5. Load the plist file into your launch daemon: `launchctl load ~/Library/LaunchAgents/hackernews.scraper.plist`

6. Success!

---

WARRANTY: Code is provided as-is. Don't break any local laws. Don't use this for evil. I am just trying to learn Python and automation (cron jobs) for Macs so consider this for learning only; not production ready.
