# cool-midi-router
A cool MIDI router written in Python

This is a simple Python program that allows you to route MIDI data from one MIDI device to another.

### Known issues:
- As of March 7th, 2023, the 'python-rtmidi' still cannot be installed via pip on Python 3.11.  To install this dependency, I had to switch my interpreter back to 3.10
- If you have really long MIDI device names, they may bleed out of the edge of the window (which cannot presently be resized).  I may fix this someday.
- If you pick 2 different MIDI devices for input and output, click the "Route MIDI Data" button, and the text at the bottom doesn't turn green to show the routing, this may mean that one of the chosen MIDI devices is inaccessible due to being open in another program.  To fix this, close all programs that are accessing that MIDI device before running Cool MIDI Router
- For some reason, on Windows, stopping the MIDI routing sends out “All Notes Off” and “Reset All Controllers” messages for all channels.  I have no idea why, since the mido documentation implies that you need to explicitly ask it to do that.  Maybe it's due to the way Windows handles MIDI.  Maybe it's a python-rtmidi thing.  I have no idea but I'm looking for a solution.
