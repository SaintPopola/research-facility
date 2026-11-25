/* Sweet Melody: the SOUND plays on every page (DAW audit 1, realtime MIDI processor in this
   synth's own MIDI chain). A Set recorded while the plug-in sat on LOOPS or SAMPLES used to play
   silent: those pages bypassed the sound. Now the sound only gives up the notes another engine
   owns: auditions on channel 15, the Loop Lines zone (60-75) in LOOPS, and the PLAY KEYS range
   in SAMPLES. Note-offs always pass, so a mode change can never leave a note hanging. */
if (!isDefined(Globals.loopMode)) Globals.loopMode = false;
if (!isDefined(Globals.smpMode)) Globals.smpMode = false;
if (!isDefined(Globals.playLo)) Globals.playLo = -1;
if (!isDefined(Globals.playHi)) Globals.playHi = -1;
reg siNote = 0;
function onNoteOn()
{
    siNote = Message.getNoteNumber();
    if (Message.getChannel() == 15)
        Message.ignoreEvent(true);
    else if (Globals.loopMode == true && siNote >= 60 && siNote <= 75)
        Message.ignoreEvent(true);
    else if (Globals.smpMode == true && Globals.playLo >= 0 && siNote >= Globals.playLo && siNote <= Globals.playHi)
        Message.ignoreEvent(true);
}
function onNoteOff()
{
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
