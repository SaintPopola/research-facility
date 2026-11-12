/* Sweet Melody SAMPLES (docs/21): PLAY KEYS. The chosen sound is mapped across the
   keyboard; auditions (MIDI channel 15) belong to the other two samplers. */
function onNoteOn()
{
    if (Message.getChannel() == 15) Message.ignoreEvent(true);
}
function onNoteOff()
{
    if (Message.getChannel() == 15) Message.ignoreEvent(true);
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
