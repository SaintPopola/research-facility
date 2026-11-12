/* Sweet Melody SAMPLES (docs/21): this sampler only plays auditions, which the
   Interface sends on MIDI channel 15. Every other channel is ignored here. */
function onNoteOn()
{
    if (Message.getChannel() != 15) Message.ignoreEvent(true);
}
function onNoteOff()
{
    if (Message.getChannel() != 15) Message.ignoreEvent(true);
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
