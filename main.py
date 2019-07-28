import os
from argparse import ArgumentParser
import logging as log
import re
from xml.dom.minidom import parse
from mido import Message, MetaMessage, MidiFile, MidiTrack, bpm2tempo
from predictGeneralMidi import getGeneralMidiNumber

# Process command line arguments
parser = ArgumentParser()
parser.add_argument("-f", "--file", dest="filename",
                    help="source FILE you would like to convert. Use Linux-style path conventions (like  ~/Ardour Folder/My Session.ardour) or Windows (like C:/Users/username/Ardour Folder/My Session.ardour).", metavar="FILE")
parser.add_argument("-m", "--musescore",
                    action="store_true", dest="musescore", default=False,
                    help="works around a quirk in MuseScore MIDI import. MuseScore assumes any piano part should have two tracks, so this setting adds a second track (containing a single note) after any piano track.")
parser.add_argument("-op", "--omitparens",
                    action="store_true", dest="omitparens", default=False,
                    help="omits any text in the track name that is inside parentheses () or square brackets [].")
parser.add_argument("-v", "--verbose",
                    action="store_true", dest="verbose", default=False,
                    help="show MIDI messages and other debugging information.")


args = parser.parse_args()

ardourFile = args.filename
if not ardourFile:
    print("Please enter the path to your Ardour file. (E.g. ~/Ardour Folder/My Session.ardour ")
    ardourFile = os.path.abspath(os.path.expanduser(input(": ")))

if args.verbose:
    def vprint(*args, **kwargs):
        print(*args, **kwargs)
else:
    vprint = lambda *a, **k: None #do-nothing function

# Get import and export folder locations
dom = parse(ardourFile)
sessionName = dom.getElementsByTagName("Session")[0].getAttribute("name")

dir = os.path.dirname(ardourFile)
importFolder = os.path.join(dir,"interchange",sessionName,"midifiles")
exportFolder = os.path.join(dir,"export")
vprint(importFolder,exportFolder)

# Iterate through the MIDI tracks in Ardour (called "Routes" in the XML file)
# Gets Ardour track id's and saves track names
mid = MidiFile(type=1,ticks_per_beat=19200)
trackRef = {} #ardour-track-id : midi-track-id
i=0
for route in dom.getElementsByTagName("Route"):
    if route.getAttribute("default-type") == "midi":
        rname = route.getAttribute("name")
        if args.omitparens:
            p = re.compile("(.*)(\(.*\))(.*)")
            rname = p.sub(r"\1\3",rname).strip()
        mid.add_track(name=rname)
        mid.tracks[i].append(MetaMessage("instrument_name",name=rname))
        programNumber = getGeneralMidiNumber(rname)
        if programNumber == -10:
            mid.tracks[i].append(MetaMessage("channel_prefix", channel=10,time=0))
            if args.musescore:
                mid.tracks[i].append(Message("program_change", program=56,time=0)) #avoids the double staff for program=0 in MuseScore
        else:
            mid.tracks[i].append(Message("program_change", program=programNumber,time=0))
        beatsPerMinute = int(dom.getElementsByTagName("Tempo")[0].getAttribute("beats-per-minute"))
        mid.tracks[i].append(MetaMessage("set_tempo",tempo=bpm2tempo(beatsPerMinute)))
        meterNumerator = int(dom.getElementsByTagName("Meter")[0].getAttribute("divisions-per-bar"))
        meterDenominator = int(dom.getElementsByTagName("Meter")[0].getAttribute("note-type"))
        mid.tracks[i].append(MetaMessage("time_signature",numerator=meterNumerator, denominator=meterDenominator))
        trackRef[route.getAttribute("id")] = i
        i = i+1
        if args.musescore and programNumber==0:
            mid.add_track(name=rname+"-secondTrack")
            mid.tracks[i].append(MetaMessage("instrument_name",name=rname))
            mid.tracks[i].append(Message("program_change", program=programNumber,time=0))
            mid.tracks[i].append(Message("note_on", channel=0, note=60, velocity=3, time=0))
            mid.tracks[i].append(MetaMessage("lyrics",text="DeleteThisNote",time=0))
            mid.tracks[i].append(Message("note_off", channel=0, note=60, velocity=3, time=9599))#eighth note, middle C
            trackRef["secondTrack"] = i
            i = i+1

vprint(trackRef)

# Iterate through the MIDI source files referenced by Ardour
# Gets file names and file id's
sourceRef = {} #source id : file name
for source in dom.getElementsByTagName("Source"):
    if source.getAttribute("type") == "midi":
        sourceRef[source.getAttribute("id")] = source.getAttribute("name")

vprint(sourceRef)

noteOnRef = {} #Reference for which notes are on (1) or off (0) so that all notes can be turnned off at the end of the region
for i in range(0, 127):
    noteOnRef[i] = 0

def convertToMeasuresAndBeats(trackTotalTime):
    #beatsPerSecond = 112
    beatLength = 19200
    beatsPerMeasure = 4
    currentMeasure = int(trackTotalTime/beatLength/beatsPerMeasure+1)
    currentBeat = "{0:.4f}".format(trackTotalTime/beatLength%beatsPerMeasure+1)
    return "| trackTotalTime " + str(trackTotalTime) + " measure " + str(currentMeasure) + " beat " + str(currentBeat)

# Iterate through the playlists in Ardour (each snippet of midi data) and save to a single, combined MIDI file
for playlist in dom.getElementsByTagName("Playlist"):
    if playlist.getAttribute("type") == "midi":
        trackNum = trackRef[playlist.getAttribute("orig-track-id")]
        vprint('\n\nTrack',trackNum)
        trackTotalTime = 0 #for tracking message times between regions
        previousRegionEndTime = 0
        for region in playlist.getElementsByTagName("Region"):
            vprint(os.path.join(importFolder,sourceRef[region.getAttribute("source-0")]))
            sourceMidi = MidiFile(os.path.join(importFolder,sourceRef[region.getAttribute("source-0")]))
            startBeats = float(region.getAttribute("start-beats")) #beat that the MIDI source file starts on for this region
            lengthBeats = float(region.getAttribute("length-beats")) #lengh of the region in beats
            beat = float(region.getAttribute("beat")) #beats between the start of the music and the start of the region
            trackTotalTime += beat*19200-previousRegionEndTime
            firstPass = True
            sourceMidiTotalTime = 0
            for msg in sourceMidi.tracks[0]:
                if not msg.is_meta:
                    sourceMidiTotalTime += msg.time
                    firstTime = int((trackTotalTime-previousRegionEndTime) + (sourceMidiTotalTime-startBeats*19200))
                    if sourceMidiTotalTime >= startBeats*19200 and sourceMidiTotalTime <= (lengthBeats+startBeats)*19200:
                        if msg.type == "note_on":
                            noteOnRef[msg.note] = 1
                        elif msg.type == "note_off":
                            noteOnRef[msg.note] = 0
                        if firstTime < 0:
                            print("\n\nERROR: Overlapping regions on Track",mid.tracks[trackNum].name,convertToMeasuresAndBeats(firstTime+previousRegionEndTime),'\n\n\n\n')
                        if firstPass:
                            vprint('trackTotalTime',convertToMeasuresAndBeats(trackTotalTime))
                            vprint('sourceMidiTotalTime',convertToMeasuresAndBeats(sourceMidiTotalTime))
                            vprint('startBeats',convertToMeasuresAndBeats(startBeats))
                            firstTime = int((trackTotalTime-previousRegionEndTime) + (sourceMidiTotalTime-startBeats*19200))
                            editedMsg = msg.copy(time=firstTime)
                            trackTotalTime = firstTime+previousRegionEndTime
                            firstPass = False
                        else:
                            editedMsg = msg.copy(time=msg.time)
                            trackTotalTime += msg.time
                        if sourceMidiTotalTime < (lengthBeats+startBeats)*19200 or msg.type == 'note_off': #ignore note_on events at very end
                            vprint(editedMsg,convertToMeasuresAndBeats(trackTotalTime))
                            mid.tracks[trackNum].append(editedMsg)
                    else:
                        for i in range(0, 127):
                            if noteOnRef[i] == 1:
                                mid.tracks[trackNum].append(Message('note_off',note=i))
                                noteOnRef[i] = 0
            previousRegionEndTime = trackTotalTime


exportFile = os.path.join(exportFolder,"ArdourMidiExport.mid")
mid.save(exportFile)
print("\nMIDI exported\n",exportFile)
