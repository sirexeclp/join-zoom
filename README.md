# Join Zoom

This tool stores all your zoom (and other browser-based)
meeting credentials and makes joining meetings fast and effortless.
All your zoom-meeting passwords are safely stored in an unencrypted text file.

## Install

Requirements are listed in the `requirements.txt`.
The need to be installed for the script to run.

## Config

The config file is located at `~/.zoom/config`.
It uses an INI like syntax.
Each section represents one meeting entry.
The section name is used as the identifier for the corresponding meeting.
Currently, two types of meetings are supported:

- `zoom`
- `browser`

The following entry stores a zoom meeting with the zoom meeting id 123456789 and the password 123456. The default type is zoom so the line `type = zoom` might be omitted in this case.

```
[test]
id = 123456789
pw = 123456
type = zoom
```

The next example is a browser-based meeting.
The URL https://jitsi.example.com/jitsi will be opened in the firefox browser to join this meeting.
The type of this entry must be set to `browser`.

```
[jitsi]
type = browser
url = https://jitsi.example.com/jitsi
browser = firefox
```

New entries can also be created using the `add` subcommand.
The command `add browser jitsi https://jitsi.example.com/jitsi firefox` will create the config entry as seen above.
Similarly the command `add zoom test 123456789 123456` will create the entry shown as an example for a zoom meeting.


## Settings

Default settings are also stored in the config file.
All settings are in the `.default` section.
Sections beginning with a dot are not listed in the interactive list of saved meetings.
Two default settings can be set: a default browser and the base URL of a default Jitsi server.
If these settings are set new Jitsi meetings can be launched with the subcommand `new jitsi <room-name>`.

```
[.default]
browser = firefox
jitsi = https://jitsi.example.com
```