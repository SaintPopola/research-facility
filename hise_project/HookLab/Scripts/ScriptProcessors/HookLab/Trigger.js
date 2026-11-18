/* Hook Lab preview trigger (realtime, not deferred).
   The Interface runs on the UI thread and must not create note events; it sets
   Globals.hlPlay (true / false) and bumps Globals.hlPlayEpoch. This timer starts or stops
   the Audio Loop Player's preview note on the audio side. */
if (!isDefined(Globals.hlPlayEpoch)) Globals.hlPlayEpoch = 0;
if (!isDefined(Globals.hlPlay)) Globals.hlPlay = false;
reg lastEpoch = 0;
reg playingId = -1;
Synth.startTimer(0.02);
function onNoteOn()
{
}
function onNoteOff()
{
}
function onController()
{
}
function onTimer()
{
    if (Globals.hlPlayEpoch != lastEpoch)
    {
        lastEpoch = Globals.hlPlayEpoch;
        if (playingId >= 0) Synth.noteOffByEventId(playingId);
        playingId = -1;
        if (Globals.hlPlay) playingId = Synth.playNote(60, 100);
    }
}
function onControl(number, value)
{
}
