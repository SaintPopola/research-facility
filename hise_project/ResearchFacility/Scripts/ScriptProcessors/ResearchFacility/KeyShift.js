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
}

function onNoteOff()
{
    if (Message.getChannel() == 16)
    {
        ksOff = SHIFT_OF[Message.getEventId() % 1024];
        Message.setNoteNumber(Message.getNoteNumber() + ksOff);
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
