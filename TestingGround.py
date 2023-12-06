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

############################
########## LABELS ##########
############################

l_lapcount=0

########## ENGINE ##########

l_speed=0
l_rpm=0
l_boost=0

########## FUEL ##########

l_fuel=0
l_fuelconsumption = 0
l_currentFuelConsumption=0
l_fuelperlap=0
l_prevlapfuelconsumption=0

########## MISC ##########

l_odometer = 0

###############################
########## VARIABLES ##########
###############################

lapcount=0

########## ENGINE ##########

speed=0
rpm=0
boost=0

########## FUEL ##########

fuel=0
fuelconsumption = 0
fuelperlap=0
prevlapfuel=0
currentFuelConsumption=0
prevlapfuelconsumption=0
fuelstate=0
fuelstatetemp=0
economyodometer=0
fuelconsumedtemp=0
fuelconsumed=0

########## MISC ##########

odometer = 0

########## TIMERS ##########

updateTimer=0
economyTimer=0

def acMain(ac_version):
    global l_lapcount
    global l_speed
    global l_rpm
    global l_boost
    global l_fuel
    global l_odometer
    global l_fuelconsumption
    global l_currentFuelConsumption
    global l_fuelperlap
    global l_prevlapfuelconsumption

    ac.initFont(0, "Roboto", 1, 1)


    appWindow = ac.newApp("TestingGround")
    ac.setSize(appWindow, 300, 200)

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

    l_odometer = ac.addLabel(appWindow, "Distance: 0")
    ac.setPosition(l_odometer, 3, 90)
   
    l_fuel = ac.addLabel(appWindow, "Fuel: 0")
    ac.setPosition(l_fuel, 3, 105)

    l_fuelconsumption = ac.addLabel(appWindow, "Fuel consumption: Distance too short")
    ac.setPosition(l_fuelconsumption, 3, 120)

    l_currentFuelConsumption = ac.addLabel(appWindow, "Fuel consumption: Distance too short")
    ac.setPosition(l_currentFuelConsumption, 3, 135)

    l_fuelperlap = ac.addLabel(appWindow, "Fuel per lap: 0.0l")
    ac.setPosition(l_fuelperlap, 3, 150)

    l_prevlapfuelconsumption = ac.addLabel(appWindow, "Previous lap fuel consumption: 0.0l")
    ac.setPosition(l_prevlapfuelconsumption, 3, 165)

    return "TestingGround"

def acUpdate(deltaT):
    global l_lapcount, l_speed,l_rpm, l_boost, l_fuel, l_odometer, l_fuelconsumption, l_currentFuelConsumption, l_fuelperlap, l_prevlapfuelconsumption
    global lapcount, speed, rpm, boost, fuel, odometer, fuelconsumption, currentFuelConsumption, fuelperlap, prevlapfuel, prevlapfuelconsumption
    global fuelstate, fuelconsumed, fuelconsumedtemp, fuelstatetemp, economyodometer
    global economyTimer, updateTimer
    updateTimer += deltaT
    economyTimer += deltaT
    
    
    laps = ac.getCarState(0, acsys.CS.LapCount)
    if laps > lapcount:
        lapcount=laps
        fuelperlap = fuelconsumed/lapcount
        ac.setText(l_lapcount, "Laps: {}".format(lapcount))
        ac.setText(l_fuelperlap, "Fuel per lap: {:.2f}l".format(fuelperlap))
        
        if laps == 1:
          prevlapfuelconsumption = fuelconsumed
          ac.setText(l_prevlapfuelconsumption, "Previous lap fuel consumption: {:.2f}l".format(prevlapfuelconsumption))
          prevlapfuel = info.physics.fuel
        else:
          prevlapfuelconsumption = prevlapfuel - info.physics.fuel
          ac.setText(l_prevlapfuelconsumption, "Previous lap fuel consumption: {:.2f}l".format(prevlapfuelconsumption))
          prevlapfuel = info.physics.fuel

           
    
    if updateTimer > 0.1:
      speed = ac.getCarState(0, acsys.CS.SpeedKMH)
      ac.setText(l_speed, "Speed: {:.1f}".format(speed))
       
    if updateTimer > 0.1:
      rpm = ac.getCarState(0, acsys.CS.RPM)
      ac.setText(l_rpm, "RPM: {:.0f}".format(rpm))
    
    boost = ac.getCarState(0, acsys.CS.TurboBoost)
    ac.setText(l_boost, "Boost: {:.2f}".format(boost))  
    
    odometer += deltaT * ac.getCarState(0, acsys.CS.SpeedKMH) / 3600
    ac.setText(l_odometer, "Distance {:.2f}".format(odometer))

    fuel = info.physics.fuel
    ac.setText(l_fuel, "Fuel: {:.2f}".format(fuel))

    if fuelstate == 0 or fuel > fuelstate:
      fuelstate = info.physics.fuel
      fuelstatetemp = info.physics.fuel
    elif fuel <= fuelstate:
      fuelconsumed += fuelstate - fuel
      fuelconsumption = fuelconsumed / (odometer/100)
      economyodometer += deltaT * ac.getCarState(0, acsys.CS.SpeedKMH) / 3600
      if economyTimer > 1 and economyodometer > 0.0001:
        fuelconsumedtemp = fuelstatetemp - fuel
        currentFuelConsumption = fuelconsumedtemp / (economyodometer/100)
        if currentFuelConsumption > 99.9:
          ac.setText(l_currentFuelConsumption,"Current fuel consumption: 99.9+l/100km".format(currentFuelConsumption))
        else:
          ac.setText(l_currentFuelConsumption,"Current fuel consumption: {:.2f}l/100km".format(currentFuelConsumption))
        fuelstatetemp = fuel
        economyodometer = 0
        if odometer > 0.5:
          ac.setText(l_fuelconsumption,"Fuel consumption: {:.2f}l/100km".format(fuelconsumption))
      elif economyTimer > 1:
         fuelconsumedtemp = fuelstatetemp - fuel
         ac.setText(l_currentFuelConsumption,"Current fuel consumption: {:.1f}l/h]".format(fuelconsumedtemp*3600))
         fuelstatetemp = fuel
         economyodometer = 0
      fuelstate = fuel

    if updateTimer > 0.1:
       updateTimer = 0
    if economyTimer > 1:
       economyTimer = 0