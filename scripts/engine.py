from openal import *
import time


class Engine:
    def __init__(self):
        source = oalOpen("audio/PlopXD.mp3")

        source.play()

        while source.get_state() == AL_PLAYING:
            # wait until the file is done playing
            time.sleep(1)

        oalQuit()
