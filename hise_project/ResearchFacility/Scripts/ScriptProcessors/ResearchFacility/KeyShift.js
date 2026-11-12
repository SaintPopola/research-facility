/* ============================================================================
   Sweet Melody - KeyShift (realtime MIDI processor, runs BEFORE Interface)

   The on-screen keyboard (and the Mac keyboard mapped to it) sends on MIDI
   channel 16. This script moves only those notes by Globals.keyShift octaves
   ("[" / "]" in the Interface). The channel is left alone (the samplers take every
   channel, and the uniform voice handler must see the same event it allocated).

   Mac-keyboard notes come from JUCE's MidiKeyboardComponent, which maps the
   QWERTY row to MIDI 60-76 (base octave 5, CustomKeyboard.cpp:236). Only
   that zone shifts, so mouse clicks elsewhere on the piano still play the
   key that was clicked. Every note-off reuses the shift its note-on got
   (matched by event id), so changing octave while holding keys can never
   leave a stuck note.
   ============================================================================ */

Globals.keyShift = 0;
Globals.loopMode = false;      // set by the Interface: LOOPS page active
Globals.loopLatch = false;     // LATCH toggle: a press starts a loop, the next press of that key stops it
Globals.latchEpoch = 0;        // bumped by the Interface after all-notes-off, so stale latches clear
Globals.latchMask = 0;         // bit (note - 60) set while that lane loop is latched; the Interface lights keys from it

// LOOPS latch (needs this non-deferred script: the Interface defers its MIDI callbacks).
// A latched press becomes an artificial note whose key-up is dropped; HISE re-inserts an
// artificial note-on whose note-off was ignored, so Synth.noteOffByEventId stops it later.
const var LATCH = [];
const var LATCH_STOP = [];
for (si = 0; si < 128; si++) { LATCH.push(-1); LATCH_STOP.push(0); }
const var LBIT = [];
for (si = 0; si < 16; si++) LBIT.push(Math.pow(2, si));
reg latchEpoch = 0;
reg lzNote = 0;

inline function inLoopZone(n)
{
    return Globals.loopMode && Globals.loopLatch && n >= 60 && n <= 75;
}

const var SHIFT_OF = [];
for (si = 0; si < 1024; si++) SHIFT_OF.push(0);

reg ksNote = 0;
reg ksOff = 0;
reg ksTarget = 0;

function onNoteOn()
{
    if (Message.getChannel() == 16)
    {
        ksNote = Message.getNoteNumber();
        ksOff = 0;
        // Mac keys always send velocity 127 (JUCE MidiKeyboardComponent default);
        // mouse clicks take velocity from click height, so they play the key clicked
        if (ksNote >= 60 && ksNote <= 76 && Message.getVelocity() == 127)
            ksOff = Globals.keyShift * 12;
        ksTarget = ksNote + ksOff;
        if (ksTarget < 0) ksTarget = 0;
        if (ksTarget > 127) ksTarget = 127;
        SHIFT_OF[Message.getEventId() % 1024] = ksTarget - ksNote;
        Message.setNoteNumber(ksTarget);
    }
    if (Globals.latchEpoch != latchEpoch)
    {
        for (si = 0; si < 128; si++) { LATCH[si] = -1; LATCH_STOP[si] = 0; }
        latchEpoch = Globals.latchEpoch;
        Globals.latchMask = 0;
    }
    lzNote = Message.getNoteNumber();
    if (inLoopZone(lzNote))
    {
        if (LATCH[lzNote] >= 0)
        {
            Synth.noteOffByEventId(LATCH[lzNote]);      // second press: stop the latched loop
            LATCH[lzNote] = -1;
            LATCH_STOP[lzNote] = 1;
            Globals.latchMask = Globals.latchMask - LBIT[lzNote - 60];
            Message.ignoreEvent(true);
        }
        else
        {
            LATCH[lzNote] = Message.makeArtificial();     // first press: keep it going
            Globals.latchMask = Globals.latchMask + LBIT[lzNote - 60];
        }
    }
}

function onNoteOff()
{
    if (Message.getChannel() == 16)
    {
        ksOff = SHIFT_OF[Message.getEventId() % 1024];
        Message.setNoteNumber(Message.getNoteNumber() + ksOff);
    }
    lzNote = Message.getNoteNumber();
    if (inLoopZone(lzNote))
    {
        if (LATCH_STOP[lzNote] == 1)
        {
            LATCH_STOP[lzNote] = 0;                     // key-up of the stopping press
            Message.ignoreEvent(true);
        }
        else if (LATCH[lzNote] >= 0)
        {
            Message.makeArtificial();                   // key-up of a latched loop: drop it
            Message.ignoreEvent(true);
        }
    }
}

function onController()
{
}

function onTimer()
{
}

function onControl(number, value)
{
}
