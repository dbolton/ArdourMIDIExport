# Change log

## 0.3
* export initial tempo and meter
* predict General Midi program numbers for all orchestral strings
* added command line argument for MuseScore (to work around MIDI import of piano tracks)
* added command line argument to omit track name text that is inside parentheses () or square brackets []
* ignore note_on events at the very end of a region
* send note_off events for any notes on at the end of a region

## 0.2
* fixed import of tracks that start later in piece rather than at very beginning
* fixed import of tracks with multiple regions (regions need to be non-overlapping)
* changed program number to match instrument (partial support)
* added command line argument for file path
* added command line argument for verbose output

## 0.1
* initial MIDI export
