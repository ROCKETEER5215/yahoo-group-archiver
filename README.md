yahoo-group-archiver
====================

This tool archives a Yahoo group using the non-public API used by the Yahoo Groups website UI.

Features:
* Saves full email content
* Downloads attachments as separate files
* Fetch all files
* Fetch all photos
* Fetch all database tables
* Fetch all links
* Fetch all events in the calendar
* Fetch all polls

Requirements:
* Python 2.7 or 3+

Usage:
```bash
pip install -r requirements.txt
./yahoo.py -ct '<T_cookie>' -cy '<Y_cookie>' '<groupid>'
```

You will need to get the `T` and `Y` cookie values from an authenticated
browser session.

The cookies should look like this, where `someLongText` and `someShortText` are arbitrary strings:
- T: `z=someLongText&a=someLongText&sk=someLongText&ks=someLongText&kt=someLongText&ku=someLongText&d=someLongText&af=someLongText`
- Y: `v=1&n=someLongText&l=someShortText=someShortText&r=hp&intl=us`

In Google Chrome these steps are required:
1. Go to [Yahoo Groups](https://groups.yahoo.com/neo).
2. Click the 🔒 padlock, or ⓘ (cicled letter i) in the address bar to the left of the website address.
3. Click "Cookies".
4. On the Allowed tab select "Yahoo.com" followed by "Cookies" in the tree listing.
5. Select the T cookie, right click the value in the _Content_ field and _Select All_. Then copy the value and paste in
   place of the `<T_cookie>` in the above command line.
6. Select the Y cookie, right click the value in the _Content_ field and _Select All_. Then copy the value and paste in
   place of the `<Y_cookie>` in the above command line.

In Firefox:
1. Go to [Yahoo Groups](https://groups.yahoo.com/neo) (make sure you're signed in with your account).
2. Press Shift-F9 or select the menu Tools/Web Developer/Storage Inspector.
3. Double click on the T cookie's value and copy the content in place of `<T_cookie>` in the above command line.
4. Double click on the Y cookie's value and copy the content in place of `<Y_cookie>` in the above command line.

Note: the string you paste _must_ be surrounded by quotes.

Using the `--cookie-file` (or `-cf`) option allows you to specify a file in which the authentication cookies will be
loaded and saved in.

If your using a Chrome browser you can use the [EditThisCookie](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg?hl=en) extension to make a cookie file. Go to options and change the export formant to Perl::LWP then go to [Yahoo Groups](https://groups.yahoo.com/neo) and use the export button to copy the cookies to the clipboard. Make a txt file and paste the cookies in it then add `#LWP-Cookies-2.0` to the first line of the file.

Files will be placed into the directory structure groupname/{email,files,photos,databases}

## Command Line Options
```
usage: yahoo.py [-h] [-ct COOKIE_T] [-cy COOKIE_Y] [-ce COOKIE_E]
                [-cf COOKIE_FILE] [-e] [-at] [-f] [-i] [-t] [-r] [-d] [-l]
                [-c] [-p] [-a] [-m] [-o] [--user-agent USER_AGENT]
                [--start START] [--stop STOP] [--ids IDS [IDS ...]] [-w] [-v]
                [--colour] [--delay DELAY]
                group

positional arguments:
  group

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose
  --colour, --color     Colour log output to terminal
  --delay DELAY         Minimum delay between requests (default 0.2s)

Authentication Options:
  -ct COOKIE_T, --cookie_t COOKIE_T
                        T authentication cookie from yahoo.com
  -cy COOKIE_Y, --cookie_y COOKIE_Y
                        Y authentication cookie from yahoo.com
  -ce COOKIE_E, --cookie_e COOKIE_E
                        Additional EuConsent cookie is required in EU
  -cf COOKIE_FILE, --cookie-file COOKIE_FILE
                        File to store authentication cookies to. Cookies
                        passed on the command line will overwrite any already
                        in the file.

What to archive:
  By default, all the below.

  -e, --email           Only archive html and raw email and attachments (from
                        email) through the messages API
  -at, --attachments    Only archive attachments (from attachments list)
  -f, --files           Only archive files
  -i, --photos          Only archive photo galleries
  -t, --topics          Only archive HTML email and attachments through the
                        topics API
  -r, --raw             Only archive raw email without attachments through the
                        messages API
  -d, --database        Only archive database
  -l, --links           Only archive links
  -c, --calendar        Only archive events
  -p, --polls           Only archive polls
  -a, --about           Only archive general info about the group
  -m, --members         Only archive members
  -o, --overwrite       Overwrite existing files such as email and database
                        records

Request Options:
  --user-agent USER_AGENT
                        Override the default user agent used to make requests

Message Range Options:
  Options to specify which messages to download. Use of multiple options
  will be combined. Note: These options will also try to fetch message IDs
  that may not exist in the group.

  --start START         Email message id to start from (specifying this will
                        cause only specified message contents to be
                        downloaded, and not message indexes). Default to 1, if
                        end option provided.
  --stop STOP           Email message id to stop at (inclusive), defaults to
                        last message ID available, if start option provided.
  --ids IDS [IDS ...]   Get email message by ID(s). Space separated,
                        terminated by another flag or --

Output Options:
  -w, --warc            Output WARC file of raw network requests. [Requires
                        warcio package installed]
```
## Yahoo Loader

If you have alot of groups to download yahooloader.py can automate the task of having to manually enter and run each one using yahoo.py.
* To use yahooloader.py:
1. Create a txt file called groups.txt in the same directory as yahooloader.py.
2. Use instructions given above to retrive your `T` and `Y` cookie values from a web browser.
3. You can also get or make a cookie file (if you need a EuConsent cookie use this method).
4. Put your `T` cookie on the first line of groups.txt _without_ quotes.
5. Put your `Y` cookie on the second line of groups.txt _without_ quotes.
6. If your using a cookie file put cookie.txt on the first line of groups.txt.
7. _Do not leave blank lines inbetween anything in groups.txt as this will cause errors!_.
8. Look at the Command Line Options section above, everything listed under `What to archive:` can be used in groups.txt.
9. To use the default in groups.txt (meaning archive everything) use `getAllDefault`.
10. On the next line you _must_ specify your global archive options, these will be used for any groups that do not have options defined.
11. From this point on copy and paste the url address's for the groups you want to download with one per line.
12. If you want to use a different set of options for downloading a certain group put them on the line above it.
* Examples of groups.txt file:
```
z=someLongText&a=someLongText&sk=someLongText&ks=someLongText&kt=someLongText&ku=someLongText&d=someLongText&af=someLongText
v=1&n=someLongText&l=someShortText=someShortText&r=hp&intl=us
getAllDefault
--files
https://groups.yahoo.com/neo/groups/ExampleGroup1/info
https://groups.yahoo.com/neo/groups/ExampleGroup2/info
```
All the files are downloaded for ExampleGroup1.

Everything is downloaded for ExampleGroup2.

```
cookie.txt
--files
https://groups.yahoo.com/neo/groups/ExampleGroup1/info
https://groups.yahoo.com/neo/groups/ExampleGroup2/info
getAllDefault
https://groups.yahoo.com/neo/groups/ExampleGroup3/info
```
All the files are downloaded for ExampleGroup1 and ExampleGroup2.

Everything is downloaded for ExampleGroup3.

13. Yahooloader checks the output of yahoo.py for each group and looks for errors and saves them in yahooloaderlog.txt.
14. Groups that had errors will be added to redownload.txt you should check each of the groups in the list to see whats missing and
go to the groups to make sure there is nothing wrong with them. If yahooloader has been running a long time authentication errors will happen sometimes. 
15. You can then rename or delete your old groups.txt and use your redownload.txt as the new groups.txt and reattempt to download the groups with errors.
* To run yahooloader.py
```
python yahooloader.py
```

## Next steps

This tool saves a complete archive of a Yahoo Group in Yahoo Groups API's custom JSON format. But this can be hard for people—and particularly non-technical people—to read.

The [Yahoo Group Archive Tools](https://github.com/anirvan/yahoo-group-archive-tools) software takes the output of this archive, and convert it into [`mbox`](https://en.wikipedia.org/wiki/Mbox) format, as well as [individual email files](https://en.wikipedia.org/wiki/Email#Message_format). Mail folders stored as `mbox` can be imported by a wide range of desktop and server-side email clients, including [Thunderbird](https://addons.thunderbird.net/en-US/thunderbird/addon/importexporttools-ng/) (Linux, Mac, Windows), [Apple Mail.app](https://support.apple.com/guide/mail/import-or-export-mailboxes-mlhlp1030/mac) (Mac), [Microsoft Outlook](https://duckduckgo.com/?q=outlook+mbox+import&ia=web) (Windows and Mac); in some cases, users will need to use an external utility. Once a list is imported into one of these clients, it may be possible to export the list content into other formats, like printing to PDF.

We're not responsible for third party software like Yahoo Group Archive Tools, so to be safe, please retain the original output of this tool.

## Alternatives to this tool
### Yahoo Get My Data
Yahoo have a ["Get My Data" tool](https://groups.yahoo.com/neo/getmydata) for downloading content of groups of which you
are a member.
It gives you:
* all group emails in .mbox format, _with all addresses unredacted_
* all files (except attachments)
* all links
* photos and attachments _you_ sent/uploaded to the group
No further data is returned, even if you are group owner.

The primary benefit to using the Yahoo tool is for retrieving the full, unredacted email archive for a group. Archival
methods that scrape the API from a non-moderator/owner(?) account will have email addresses in the message contents
redacted.

Downsides to using this tool are that not all group content is returned, even for group owners!
The current lag time from requesting the data to being able to download it is about a week at the time of writing.

One user of Yahoo's Get My Data described it as ["woefully
incomplete"](https://github.com/IgnoredAmbience/yahoo-group-archiver/issues/87).
