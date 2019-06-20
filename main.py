import os
from argparse import ArgumentParser
from xml.dom.minidom import parse
from mido import Message, MetaMessage, MidiFile, MidiTrack
from predictGeneralMidi import getGeneralMidiNumber

# Get Ardour file path
parser = ArgumentParser()
parser.add_argument("-f", "--file", dest="filename",
                    help="Optionally include the Ardour source file from the command line. Use Linux-style path conventions (like  ~/Ardour Folder/My Session.ardour) or Windows (like C:/Users/username/Ardour Folder/My Session.ardour).", metavar="FILE")
# parser.add_argument("-q", "--quiet",
#                     action="store_false", dest="verbose", default=True,
#                     help="don't print status messages to stdout")

args = parser.parse_args()

ardourFile = args.filename
if not ardourFile:
    print("Please enter the path to your Ardour file. (E.g. ~/Ardour Folder/My Session.ardour ")
    ardourFile = os.path.abspath(os.path.expanduser(input(": ")))

# Get import and export folder locations
dom = parse(ardourFile)
sessionName = dom.getElementsByTagName("Session")[0].getAttribute("name")

dir = os.path.dirname(ardourFile)
importFolder = os.path.join(dir,"interchange",sessionName,"midifiles")
exportFolder = os.path.join(dir,"export")
print(importFolder,exportFolder)

# Iterate through the MIDI tracks in Ardour (called "Routes" in the XML file)
# Gets Ardour track id's and saves track names
mid = MidiFile(type=1,ticks_per_beat=19200)
trackRef = {} #ardour-track-id : midi-track-id
i=0
for route in dom.getElementsByTagName("Route"):
    if route.getAttribute("default-type") == "midi":
        rname = route.getAttribute("name")
        mid.add_track(name=rname)
        mid.tracks[i].append(MetaMessage("instrument_name",name=rname))
        mid.tracks[i].append(Message('program_change', program=getGeneralMidiNumber(rname),time=0))
        trackRef[route.getAttribute("id")] = i
        i = i+1

print(trackRef)

# Iterate through the MIDI source files referenced by Ardour
# Gets file names and file id's
sourceRef = {} #source id : file name
for source in dom.getElementsByTagName("Source"):
    if source.getAttribute("type") == "midi":
        sourceRef[source.getAttribute("id")] = source.getAttribute("name")

print(sourceRef)

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
        print('\n\nTrack',trackNum)
        trackTotalTime = 0 #for tracking message times between regions
        previousRegionEndTime = 0
        for region in playlist.getElementsByTagName("Region"):
            print(os.path.join(importFolder,sourceRef[region.getAttribute("source-0")]))
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

                    #print('end track at tick:',lengthBeats*19200+startBeats*19200)
                    firstTime = int((trackTotalTime-previousRegionEndTime) + (sourceMidiTotalTime-startBeats*19200))
                    if sourceMidiTotalTime >= startBeats*19200 and sourceMidiTotalTime <= (lengthBeats+startBeats)*19200 and firstTime >= 0:
                        if firstPass:
                            print('trackTotalTime',convertToMeasuresAndBeats(trackTotalTime))
                            print('sourceMidiTotalTime',convertToMeasuresAndBeats(sourceMidiTotalTime))
                            print('startBeats',convertToMeasuresAndBeats(startBeats))
                            firstTime = int((trackTotalTime-previousRegionEndTime) + (sourceMidiTotalTime-startBeats*19200))
                            #print('position',position,'+ totalTime',totalTime,'- start',start,'=',firstTime,convertToMeasuresAndBeats(firstTime))
                            editedMsg = msg.copy(time=firstTime)
                            trackTotalTime = firstTime+previousRegionEndTime
                            firstPass = False
                            #if (firstTime<0):
                            #    print("CAN'T HAVE NEGATIVE\n\n\n")
                        else:
                            editedMsg = msg.copy(time=msg.time)
                            trackTotalTime += msg.time
                        print(editedMsg,convertToMeasuresAndBeats(trackTotalTime))
                        mid.tracks[trackNum].append(editedMsg)
            previousRegionEndTime = trackTotalTime


mid.save(os.path.join(exportFolder,"ArdourMidiExport.mid"))
print("\nFile saved to your Ardour file's export folder")
