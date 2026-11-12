/* ============================================================================
   Sweet Melody - SampleRouter (realtime MIDI processor, after KeyShift, before
   Interface; docs/21 SAMPLES)

   Auditions arrive on MIDI channel 15 (Synth.playNoteFromUI in the Interface).
   While the host plays, a note-on is delayed to the next bar (loops) or the next
   beat (one-shots), so a loop starts on Live's bar line. With the transport
   stopped it plays at once. Only the START is quantized: the sampler has no
   phase lock, so a tempo ramp or a loop jump in the host can drift an audition.

   Position: a 1/16 grid callback (sync, audio thread) records the last grid
   index and when it happened; a note-on then measures how far past that tick it
   is (Engine.getUptime includes the event timestamp inside MIDI callbacks).
   Bars count from ppq 0, so 4/4 is assumed.
   ============================================================================ */

Synth.setFixNoteOnAfterNoteOff(true);   // a stop can arrive before its delayed start

Globals.smpSnap = 0;      // set by the Interface: 16 = next bar, 4 = next beat, 0 = no quantize
Globals.smpDelay = 0.0;   // seconds the last audition was delayed (read by the Interface playhead)
Globals.smpEvt = 0;       // counts quantized auditions

reg gIdx = -1;
reg gUp = 0.0;
reg isRun = 0;
reg s16 = 0.0;
reg pos = 0.0;
reg tgt = 0.0;
reg dly = 0;

const var RouterClock = Engine.createTransportHandler();
RouterClock.setSyncMode(RouterClock.ExternalOnly);
RouterClock.setEnableGrid(true, 11);          // 11 = TempoSyncer::Sixteenth (no extended tempo values)

inline function onRouterGrid(gridIndex, timestamp, firstGrid)
{
    gIdx = gridIndex;
    gUp = Engine.getUptime() + timestamp / Engine.getSampleRate();
}
RouterClock.setOnGridChange(true, onRouterGrid);

inline function onRouterRun(playing)
{
    isRun = playing ? 1 : 0;
    if (!playing) gIdx = -1;
}
RouterClock.setOnTransportChange(true, onRouterRun);

function onNoteOn()
{
    if (Message.getChannel() != 15) return;
    Globals.smpDelay = 0.0;
    if (isRun == 1 && gIdx >= 0 && Globals.smpSnap > 0 && Engine.getHostBpm() > 0)
    {
        s16 = 15.0 / Engine.getHostBpm();                          // seconds per 1/16
        pos = gIdx + (Engine.getUptime() - gUp) / s16;
        tgt = Math.ceil(pos / Globals.smpSnap - 0.02) * Globals.smpSnap;   // a hair early still counts as on the line
        if (tgt < pos) tgt = pos;
        dly = Math.round((tgt - pos) * s16 * Engine.getSampleRate());
        if (dly > 0)
        {
            Message.delayEvent(dly);
            Globals.smpDelay = dly / Engine.getSampleRate();
        }
    }
    Globals.smpEvt = Globals.smpEvt + 1;
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
