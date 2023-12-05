import sys
import ac
import acsys
import os
import platform
if platform.architecture()[0] == "64bit":
  sysdir='apps/python/TestingGround/third_party/stdlib64'
else:
  sysdir='apps/python/TestingGround/third_party/stdlib'
sys.path.insert(0, sysdir)
os.environ['PATH'] = os.environ['PATH'] + ";."

from sim_info import info

l_lapcount=0
lapcount=0

l_speed=0
speed=0

l_rpm=0
rpm=0

l_boost=0
boost=0

l_fuel=0
fuel=0

l_fuelconsumption = 0
fuelconsumption = 0

l_odometer = 0
odometer = 0

updateTimer=0


def acMain(ac_version):
    global l_lapcount
    global l_speed
    global l_rpm
    global l_boost
    global l_fuel
    global l_odometer

    appWindow = ac.newApp("TestingGround")
    ac.setSize(appWindow, 200, 200)

    ac.log("Hello, log test")
    ac.console("Hello, console test")

    l_lapcount = ac.addLabel(appWindow, "Laps: 0")
    ac.setPosition(l_lapcount, 3, 30)

    l_speed = ac.addLabel(appWindow, "Speed: 0")
    ac.setPosition(l_speed, 3, 45)
    
    l_rpm = ac.addLabel(appWindow, "RPM: 0")
    ac.setPosition(l_rpm, 3, 60)

    l_boost = ac.addLabel(appWindow, "Boost: 0")
    ac.setPosition(l_boost, 3, 75)

    l_fuel = ac.addLabel(appWindow, "Fuel: 0")
    ac.setPosition(l_fuel, 3, 90)

    l_odometer = ac.addLabel(appWindow, "Distance: 0")
    ac.setPosition(l_odometer, 3, 105)

    return "TestingGround"

def acUpdate(deltaT):
    global l_lapcount, lapcount, l_speed, speed, l_rpm, rpm, l_boost, boost, l_fuel, fuel, l_odometer, odometer
    global updateTimer
    updateTimer += deltaT
    
    laps = ac.getCarState(0, acsys.CS.LapCount)
    if laps > lapcount:
        lapcount=laps
        ac.setText(l_lapcount, "Laps: {}".format(lapcount))
    
    if updateTimer > 0.1:
      speed = ac.getCarState(0, acsys.CS.SpeedKMH)
      ac.setText(l_speed, "Speed: {:.1f}".format(speed))
       
    if updateTimer > 0.1:
      rpm = ac.getCarState(0, acsys.CS.RPM)
      ac.setText(l_rpm, "RPM: {:.0f}".format(rpm))
    
    boost = ac.getCarState(0, acsys.CS.TurboBoost)
    ac.setText(l_boost, "Boost: {:.2f}".format(boost))  
    
    fuel = info.physics.fuel
    ac.setText(l_fuel, "Fuel: {:.2f}".format(fuel))

    odometer += deltaT * speed / 3600
    ac.setText(l_odometer, "Distance {:.2f}".format(odometer))


    if updateTimer > 0.1:
       updateTimer = 0