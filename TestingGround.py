import sys
import ac
import acsys

l_lapcount=0
lapcount=0
l_speed=0
speed=0

def acMain(ac_version):
    global l_lapcount
    global l_speed

    appWindow = ac.newApp("testingGround")
    ac.setSize(appWindow, 200, 200)

    ac.log("Hello, log test")
    ac.console("Hello, console test")

    l_lapcount = ac.addLabel(appWindow, "Laps: 0")
    ac.setPosition(l_lapcount, 3, 30)

    l_speed = ac.addLabel(appWindow, "Speed: 0")
    ac.setPosition(l_speed, 3, 60)

    return "testingGround"

def acUpdate(deltaT):
    global l_lapcount, lapcount, l_speed, speed
    laps = ac.getCarState(0, acsys.CS.LapCount)
    if laps > lapcount:
        lapcount=laps
        ac.setText(l_lapcount, "Laps: {}".format(lapcount))
    
    speed = ac.getCarState(0, acsys.CS.SpeedKMH)
    ac.setText(l_speed, "Speed: {:.1f}".format(speed))