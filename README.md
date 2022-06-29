# iplayerttmltosrt

BBC iPlayer stores subtitles in a strange ttml format. This is a program to translate their ttml subs to the more useful srt format which services such as Plex and Kodi can read.

For ttml subs downloaded from Netflix, HBO etc. see https://github.com/yuppity/ttml2srt.

This is deigned to be run from the command line as follows

```bash
./ttml2srt.py subtitle_from_iplayer.ttml
```