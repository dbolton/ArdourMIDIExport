## What is Ardour MIDI Export
This project exports all MIDI tracks from Ardour into a single MIDI file.

[Ardour](https://ardour.org/) is great for recording and editing MIDI. However, you cannot create sheet music in Ardour.

This project lets your quickly compose in Ardour, but then export to notation software via MIDI.

## How to use
1. Install [python](https://python.org) and add to your path.
2. From the command run: `pip install mido` (see [mido instructions](https://mido.readthedocs.io/en/latest/installing.html) for details).
3. Run `python main.py`
4. Open the MIDI file in your favorite notation software.

## Limitations
* Export ignores any tempo changes (due to the complexity of extracting that information from Ardour)
* Export fails on any overlapping regions. For accurate results, remove any overlapping regions in your Ardour session before exporting. (Technically only overlapping notes or MIDI events between two regions are a problem.)
* Almost all MIDI data (beyond pitches, rhythms, and track names) is open to interpretation by your notation software. If you haven't quantized in Ardour, even the rhythms are open to interpretation.
