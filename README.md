# Hackernews scraper and analysis

### Hosted data visualization at http://usarneme-hn.surge.sh/

The script runs once daily, pulls all domains out where articles are hosted and then linked to on ycombinator's hackernews aggregator. Both the article hosts (domain/website) and the articles' title words are pulled out and put into a word cloud. You can see the word cloud by visiting http://usarneme-hn.surge.sh/

---

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

---

## Prereqs

This project uses a shell script which should run on Mac and Linux machines without issue. For Windows you'll either have to use git-bash, the linux integrated environment, powershell or something else idk.

You should have bash or another CLI script language installed and enabled.

I am using surge.sh to host the output html+css+javascript. You can choose any static web host you want but surge is easy to automate updates. See https://surge.sh/help/ for instructions on setting this up on your machine.

Python3 must also be installed and able to be used from the command line. Check out how to install and use it here https://www.python.org/downloads/.

---

## How to use:


1. Clone this repository:
`git clone https://github.com/Usarneme/pieathon/`

2. Enter the cloned directory and get the path to the python script:
`cd pieathon`
`pwd` should output the full path to the directory, for me it is at `/Users/usarneme/Projects/pieathon`

3. Enable the shell script to be executed from the command line:
`chmod +x orchestrator.sh`

4. Get the path to your bash binary:
`which bash` should output the full directory, for me it is at `/bin/sh`

5. Create a .plist XML file with nano or your editor of choice:
`nano ~/Library/LaunchAgents/hackernews.scraper.plist`

```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>hackernews.scraper</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/sh</string>
        <string>/Users/usarneme/Projects/pieathon/orchestrator.sh</string>
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

Use Ctrl+O to save, then Ctrl+X to exit the nano editor.


You can use different hour and minutes. Mine is set up to run at 11:16am local machine time once each day.


You can also use a different place to store log files. It should create the file on first run if it didn't previously exist but it couldn't hurt to `touch /Users/usarneme/Library/Logs/hackernews_scraper.log` to create the file ahead of time.

6. Load the plist file into your launch daemon: `launchctl load ~/Library/LaunchAgents/hackernews.scraper.plist`

7. Success! Confirm the existence with `launchctl print gui/$(id -u)/hackernews.scraper`.


Remind yourself to check this and the log file again after the script runs next (whatever time of day you set it to run at in the .plist). Pay attention to the `last exit code` in the printout as that will give you some more info into tracking down any possible errors in the script run.

---

If you need to remove the job, you can do so with:
`launchctl unload ~/Library/LaunchAgents/hackernews.scraper.plist`
which will remove it from the list of automatic scripts.

---

WARRANTY: Code is provided as-is. No warranty. I take no responsibility for what you do with it. Don't break any local laws. Don't use this for evil. I am just trying to learn Python and automation (cron jobs) for Macs so consider this for learning only; not production ready.
