import re

# def in (trackName,searchName,programNumber):
#     re.search(searchName,trackName,re.IGNORECASE)
#     return True

def getGeneralMidiNumber(name):
    p = 0 #program number
        """
        Piano

            1 Acoustic Grand Piano
            2 Bright Acoustic Piano
            3 Electric Grand Piano
            4 Honky-tonk Piano
            5 Electric Piano 1
            6 Electric Piano 2
            7 Harpsichord
            8 Clavinet"""
    if re.search(r'Piano',name,re.I):
        p = 0
        if re.search(r'Bright',name,re.I):
            p = 1
        elif re.search(r'Electric',name,re.I):
            if re.search(r'Grand',name,re.I):
                p = 2
            elif re.search(r'2',name,re.I):
                p = 5
            else:
                p = 4
        elif re.search(r'Honky-? ?tonk',name,re.I):
            p = 3
        elif re.search(r'Harpsichord',name,re.I):
            p = 6
        elif re.search(r'Clavinet',name,re.I):
            p = 7
    elif re.search(r'Pizzicato',name,re.I):
        p = 45
        """
        Chromatic Percussion

            9 Celesta
            10 Glockenspiel
            11 Music Box
            12 Vibraphone
            13 Marimba
            14 Xylophone
            15 Tubular Bells
            16 Dulcimer"""
    elif re.search(r'Celesta',name,re.I):
        p = 8
    elif re.search(r'Glockenspiel',name,re.I):
        p = 9
    elif re.search(r'Music Box',name,re.I):
        p = 10
    elif re.search(r'Vibraphone',name,re.I):
        p = 12
    elif re.search(r'Marimba',name,re.I):
        p = 13
    elif re.search(r'Xylophone',name,re.I):
        p = 14
    elif re.search(r'Tubular Bells',name,re.I):
        p = 15
    elif re.search(r'Dulcimer',name,re.I):
        p = 11
        """
        Organ

            17 Drawbar Organ
            18 Percussive Organ
            19 Rock Organ
            20 Church Organ
            21 Reed Organ
            22 Accordion
            23 Harmonica
            24 Tango Accordion"""
    elif re.search(r'Organ',name,re.I):
        p = 19
            if re.search(r'Drawbar',name,re.I):
                p = 16
            elif re.search(r'Percussive',name,re.I):
                p = 17
            elif re.search(r'Rock',name,re.I):
                p = 18
            elif re.search(r'Reed',name,re.I):
                p = 20
    elif re.search(r'Accordion',name,re.I):
        p = 21
        if re.search(r'Tango',name,re.I):
            p = 23
    elif re.search(r'Harmonica',name,re.I):
        p = 22
        """
        Guitar

            25 Acoustic Guitar (nylon)
            26 Acoustic Guitar (steel)
            27 Electric Guitar (jazz)
            28 Electric Guitar (clean)
            29 Electric Guitar (muted)
            30 Overdriven Guitar
            31 Distortion Guitar
            32 Guitar Harmonics"""
    elif re.search(r'Guitar',name,re.I):
        p = 24 #nylon
        if re.search(r'steel',name,re.I):
            p = 25
        elif re.search(r'jazz',name,re.I):
            p = 26
        elif re.search(r'clean',name,re.I):
            p = 27
        elif re.search(r'muted',name,re.I):
            p = 28
        elif re.search(r'Overdriven',name,re.I):
            p = 29
        elif re.search(r'Distortion',name,re.I):
            p = 30
        elif re.search(r'Harmonics',name,re.I):
            p = 31
        """
        Bass

            33 Acoustic Bass
            34 Electric Bass (finger)
            35 Electric Bass (pick)
            36 Fretless Bass
            37 Slap Bass 1
            38 Slap Bass 2
            39 Synth Bass 1
            40 Synth Bass 2"""
    elif re.search(r'Bass',name,re.I):
        p = 33#electric (finger)
        if re.search(r'acoustic',name,re.I):
            p = 32
        elif re.search(r'pick',name,re.I):
            p = 34
        elif re.search(r'Fretless',name,re.I):
            p = 35
        elif re.search(r'slap',name,re.I):
            p = 36 #slap bass 1
            if re.search(r'2',name,re.I) or re.search(r'II',name,re.I):
                p = 37
        elif re.search(r'synth',name,re.I):
            p = 38
            if re.search(r'2',name,re.I) or re.search(r'II',name,re.I):
        """
        Strings

            41 Violin
            42 Viola
            43 Cello
            44 Contrabass
            45 Tremolo Strings
            46 Pizzicato Strings
            47 Orchestral Harp
            48 Timpani"""
    elif re.search(r'Tremolo',name,re.I):
        p = 44
    elif re.search(r'Pizzicato',name,re.I):
        p = 45
    elif re.search(r'Violin',name,re.I):
        p = 40
    elif re.search(r'Viola',name,re.I):
        p = 41
    elif re.search(r'Cello',name,re.I):
        p = 42
    elif re.search(r'Contrabass',name,re.I):
        p = 43
    elif re.search(r'Harp',name,re.I):
        p = 46
    elif re.search(r'Timpani',name,re.I):
        p = 47
        """
        Ensemble

            49 String Ensemble 1
            50 String Ensemble 2
            51 Synth Strings 1
            52 Synth Strings 2
            53 Choir Aahs
            54 Voice Oohs
            55 Synth Choir
            56 Orchestra Hit"""
    elif re.search(r'Synth String',name,re.I):
        p = 50
        if re.search(r'2',name,re.I) or re.search(r'II',name,re.I):
            p = 51
    elif re.search(r'String Ensemble',name,re.I) or re.search(r'Strings',name,re.I):
        p = 48
        if re.search(r'2',name,re.I) or re.search(r'II',name,re.I):
            p = 49
    elif re.search(r'Choir',name,re.I) or re.search(r'Voice',name,re.I):
        p = 52
        if re.search(r'Ooh',name,re.I):
            p = 53
        elif re.search(r'Synth',name,re.I):
            p = 54
    elif re.search(r'Orchestra Hit',name,re.I):
        p = 55
        """
        Brass

            57 Trumpet
            58 Trombone
            59 Tuba
            60 Muted Trumpet
            61 French Horn
            62 Brass Section
            63 Synth Brass 1
            64 Synth Brass 2"""
    elif re.search(r'Trumpet',name,re.I):
        p = 56
        if re.search(r'Mute',name,re.I):
            p=59
    elif re.search(r'Trombone',name,re.I):
        p = 57
    elif re.search(r'Tuba',name,re.I):
        p = 58
    elif re.search(r'Horn',name,re.I) and not re.search(r'English',name,re.I):
        p = 60
    elif re.search(r'Brass',name,re.I):
        p = 61
        if re.search(r'Synth',name,re.I):
            p = 62
            if re.search(r'II',name,re.I) or re.search(r'2',name,re.I):
                p = 63
        """
        Reed

            65 Soprano Sax
            66 Alto Sax
            67 Tenor Sax
            68 Baritone Sax
            69 Oboe
            70 English Horn
            71 Bassoon
            72 Clarinet"""
    elif re.search(r'Sax',name,re.I):
        p = 66 #alto sax
        if re.search(r'Soprano',name,re.I):
            p = 64
        elif re.search(r'Tenor',name,re.I):
            p = 66
        elif re.search(r'Bari',name,re.I):
            p = 67
    elif re.search(r'Oboe',name,re.I):
        p = 68
    elif re.search(r'English Horn',name,re.I) or re.search(r'Cors? Anglais',name,re.I):
        p = 69
    elif re.search(r'Basson',name,re.I):
        p = 70
    elif re.search(r'Clarinet',name,re.I):
        p = 71
        """
        Pipe

            73 Piccolo
            74 Flute
            75 Recorder
            76 Pan Flute
            77 Blown bottle
            78 Shakuhachi
            79 Whistle
            80 Ocarina"""
    elif re.search(r'Piccolo',name,re.I) and not re.search(r'Trumpet',name,re.I):
        p = 72
    elif re.search(r'Flute',name,re.I):
        p = 73
        if re.search(r'Pan',name,re.I):
            p = 75
    elif re.search(r'Recorder',name,re.I):
        p = 74
    elif re.search(r'Blown bottle',name,re.I):
        p = 76
    elif re.search(r'Shakuhachi',name,re.I):
        p = 77
    elif re.search(r'Whistle',name,re.I):
        p = 78
    elif re.search(r'Ocarina',name,re.I):
        p = 79
        """
        Synth Lead

            81 Lead 1 (square)
            82 Lead 2 (sawtooth)
            83 Lead 3 (calliope)
            84 Lead 4 (chiff)
            85 Lead 5 (charang)
            86 Lead 6 (voice)
            87 Lead 7 (fifths)
            88 Lead 8 (bass + lead)"""
    elif re.search(r'Synth Lead',name,re.I):
        p = 80 #lead 1 (square)
        if re.search(r'2',name,re.I) or re.search(r'sawtooth',name,re.I):
            p = 81
        elif re.search(r'3',name,re.I) or re.search(r'calliope',name,re.I):
            p = 82
        elif re.search(r'4',name,re.I) or re.search(r'chiff',name,re.I):
            p = 83
        elif re.search(r'5',name,re.I) or re.search(r'charang',name,re.I):
            p = 84
        elif re.search(r'6',name,re.I) or re.search(r'voice',name,re.I):
            p = 85
        elif re.search(r'7',name,re.I) or re.search(r'fifths',name,re.I):
            p = 86
        elif re.search(r'8',name,re.I) or re.search(r'bass',name,re.I) or re.search(r'lead',name,re.I):
            p = 87
    return p




"""
Synth Pad

    89 Pad 1 (new age)
    90 Pad 2 (warm)
    91 Pad 3 (polysynth)
    92 Pad 4 (choir)
    93 Pad 5 (bowed)
    94 Pad 6 (metallic)
    95 Pad 7 (halo)
    96 Pad 8 (sweep)

Synth Effects

    97 FX 1 (rain)
    98 FX 2 (soundtrack)
    99 FX 3 (crystal)
    100 FX 4 (atmosphere)
    101 FX 5 (brightness)
    102 FX 6 (goblins)
    103 FX 7 (echoes)
    104 FX 8 (sci-fi)

Ethnic

    105 Sitar
    106 Banjo
    107 Shamisen
    108 Koto
    109 Kalimba
    110 Bagpipe
    111 Fiddle
    112 Shanai

Percussive

    113 Tinkle Bell
    114 Agogo
    115 Steel Drums
    116 Woodblock
    117 Taiko Drum
    118 Melodic Tom
    119 Synth Drum
    120 Reverse Cymbal

Sound effects

    121 Guitar Fret Noise
    122 Breath Noise
    123 Seashore
    124 Bird Tweet
    125 Telephone Ring
    126 Helicopter
    127 Applause
    128 Gunshot
"""
