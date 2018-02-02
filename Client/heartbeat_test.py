from pulsesensor import Pulsesensor
import time



def GetHeartData(user):
    p = Pulsesensor()
    p.startAsyncBPM()
    try:
        while True:
            bpm = p.BPM
            if bpm > 0:
                user.setHeartRate(bpm)

            time.sleep(1)
    except:
        p.stopAsyncBPM()
