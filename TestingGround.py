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

l_lapCount=0

########## ENGINE ##########

l_speed=0
l_rpm=0
l_boost=0

########## FUEL ##########

l_fuel=0
l_avgFuelConsumption = 0
l_tempFuelConsumption=0
l_avgFuelConsumptionPerLap=0
l_prevLapFuelConsumption=0
l_fuelRangeKM=0
l_fuelRangeLaps=0
l_fuelRangeTime=0

########## MISC ##########

l_odometer = 0

###############################
########## VARIABLES ##########
###############################

########## ENGINE ##########

speed=0
rpm=0
boost=0

########## FUEL ##########

fuel=0
fuelConsumption = 0
avgFuelConsumptionPerLap=0
prevLapFuelConsumption=0
currentFuelConsumption=0
fuelState=0
fuelStateTemp=0
economyOdometer=0
fuelConsumedState=0
fuelConsumedStateTemp=0
fuelRangeKM=0
fuelRangeLaps=0
fuelRangeTime=0
drivenTimer=0
fuelDriven=0
fuelDrivenState=0

########## MISC ##########

odometer = 0
lapCount=0
lapTimeSum=0
avgLapTime=0

########## TIMERS ##########

updateTimer=0
economyTimer=0
prevLapFuelColorTimer=0

def acMain(ac_version):
    global l_lapCount
    global l_speed
    global l_rpm
    global l_boost
    global l_fuel
    global l_odometer
    global l_avgFuelConsumption
    global l_tempFuelConsumption
    global l_avgFuelConsumptionPerLap
    global l_prevLapFuelConsumption
    global l_fuelRangeKM
    global l_fuelRangeLaps
    global l_fuelRangeTime

    ac.initFont(0, "Roboto", 1, 1)


    appWindow = ac.newApp("TestingGround")
    ac.setSize(appWindow, 300, 250)
    ac.setBackgroundOpacity(appWindow, 1)

    ac.log("Hello, log test")
    ac.console("Hello, console test")

    l_lapCount = ac.addLabel(appWindow, "Laps: 0")
    ac.setPosition(l_lapCount, 3, 30)
    setRoboto(l_lapCount, 15)

    l_speed = ac.addLabel(appWindow, "Speed: 0")
    ac.setPosition(l_speed, 3, 45)
    setRoboto(l_speed, 15)
    
    l_rpm = ac.addLabel(appWindow, "RPM: 0")
    ac.setPosition(l_rpm, 3, 60)
    setRoboto(l_rpm, 15)

    l_boost = ac.addLabel(appWindow, "Boost: 0")
    ac.setPosition(l_boost, 3, 75)
    setRoboto(l_boost, 15)

    l_odometer = ac.addLabel(appWindow, "Distance: 0")
    ac.setPosition(l_odometer, 3, 90)
    setRoboto(l_odometer, 15)
   
    l_fuel = ac.addLabel(appWindow, "Fuel: 0")
    ac.setPosition(l_fuel, 3, 105)
    setRoboto(l_fuel, 15)

    l_avgFuelConsumption = ac.addLabel(appWindow, "Fuel consumption: Distance too short")
    ac.setPosition(l_avgFuelConsumption, 3, 120)
    setRoboto(l_avgFuelConsumption, 15)

    l_tempFuelConsumption = ac.addLabel(appWindow, "Fuel consumption: 0.0l/100km")
    ac.setPosition(l_tempFuelConsumption, 3, 135)
    setRoboto(l_tempFuelConsumption, 15)

    l_avgFuelConsumptionPerLap = ac.addLabel(appWindow, "Fuel per lap: 0.0l")
    ac.setPosition(l_avgFuelConsumptionPerLap, 3, 150)
    setRoboto(l_avgFuelConsumptionPerLap, 15)

    l_prevLapFuelConsumption = ac.addLabel(appWindow, "Previous lap fuel consumption: 0.0l")
    ac.setPosition(l_prevLapFuelConsumption, 3, 165)
    setRoboto(l_prevLapFuelConsumption, 15)

    l_fuelRangeKM = ac.addLabel(appWindow, "Fuel range: 0km")
    ac.setPosition(l_fuelRangeKM, 3, 180)
    setRoboto(l_fuelRangeKM, 15)

    l_fuelRangeLaps = ac.addLabel(appWindow, "Fuel range: 0 laps")
    ac.setPosition(l_fuelRangeLaps, 3, 195)
    setRoboto(l_fuelRangeLaps, 15)

    l_fuelRangeTime = ac.addLabel(appWindow, "Fuel range: 0 minutes")
    ac.setPosition(l_fuelRangeTime, 3, 210)
    setRoboto(l_fuelRangeTime, 15)

    return "TestingGround"

def setRoboto(labelName, size):
    ac.setFontSize(labelName, size)
    ac.setCustomFont(labelName, "Roboto", 1, 1)
    ac.setFontColor(labelName, 0.86, 0.86, 0.86, 1)

def acUpdate(deltaT):
    global l_lapCount, l_speed,l_rpm, l_boost, l_fuel, l_odometer, l_avgFuelConsumption, l_tempFuelConsumption, l_avgFuelConsumptionPerLap, l_prevLapFuelConsumption, l_fuelRangeKM, l_fuelRangeLaps, l_fuelRangeTime
    global lapCount, speed, rpm, boost, fuel, odometer, fuelConsumption, currentFuelConsumption, avgFuelConsumptionPerLap, prevLapFuelConsumption, prevLapFuelConsumption, fuelRangeKM, fuelRangeLaps, fuelRangeTime
    global fuelState, fuelConsumedStateTemp, fuelConsumedState, fuelStateTemp, economyOdometer, fuelRangeTime, fuelDriven, fuelDrivenState
    global economyTimer, updateTimer, prevLapFuelColorTimer, drivenTimer
    
    updateTimer += deltaT
    economyTimer += deltaT
    prevLapFuelColorTimer += deltaT

    odometer += deltaT * ac.getCarState(0, acsys.CS.SpeedKMH) / 3600
    laps = ac.getCarState(0, acsys.CS.LapCount)
    fuel = info.physics.fuel
    speed = ac.getCarState(0, acsys.CS.SpeedKMH)
    boost = ac.getCarState(0, acsys.CS.TurboBoost)
    rpm = ac.getCarState(0, acsys.CS.RPM)
    
    if laps > lapCount:
        lapCount=laps
        avgFuelConsumptionPerLap = fuelConsumedStateTemp/lapCount
        ac.setText(l_lapCount, "Laps: {}".format(lapCount))
        ac.setText(l_avgFuelConsumptionPerLap, "Fuel per lap: {:.2f}l".format(avgFuelConsumptionPerLap))
        
        if laps == 1:
          prevLapFuelConsumption = fuelConsumedStateTemp
          ac.setText(l_prevLapFuelConsumption, "Previous lap fuel consumption: {:.2f}l".format(prevLapFuelConsumption))
          prevLapFuelConsumption = info.physics.fuel
        else:
          prevLapFuelConsumption = prevLapFuelConsumption - info.physics.fuel
          ac.setText(l_prevLapFuelConsumption, "Previous lap fuel consumption: {:.2f}l".format(prevLapFuelConsumption))
          prevLapFuelColorTimer = 0
          if avgFuelConsumptionPerLap >= prevLapFuelConsumption:
            ac.setFontColor(l_prevLapFuelConsumption, 0, 0.86, 0, 1)
          elif avgFuelConsumptionPerLap*1.1 < prevLapFuelConsumption:
            ac.setFontColor(l_prevLapFuelConsumption, 0.86, 0, 0, 1)
          else:
            ac.setFontColor(l_prevLapFuelConsumption, 0.86, 0.86, 0, 1)
          prevLapFuelConsumption = info.physics.fuel

    if fuel < avgFuelConsumptionPerLap * 1.1:
      ac.setFontColor(l_fuel, 0.86, 0, 0, 1)
    elif fuel < avgFuelConsumptionPerLap * 2.2:
      ac.setFontColor(l_fuel, 0.86, 0.86, 0, 1)
    else:
      ac.setFontColor(l_fuel, 0.86, 0.86, 0.86, 1)
 
    if fuelState == 0 or fuel > fuelState or fuelState - fuel > 0.01:
      fuelState = fuel
      fuelStateTemp = fuel
    elif fuel <= fuelState:
      fuelConsumedStateTemp += fuelState - fuel
      fuelConsumption = fuelConsumedStateTemp / (odometer/100)
      economyOdometer += deltaT * ac.getCarState(0, acsys.CS.SpeedKMH) / 3600
      if economyTimer > 1 and economyOdometer > 0.0001:
        fuelConsumedState = fuelStateTemp - fuel
        currentFuelConsumption = fuelConsumedState / (economyOdometer/100)
        if currentFuelConsumption > 999.9:
          ac.setText(l_tempFuelConsumption,"Current fuel consumption: 999.9+l/100km")
          ac.setFontColor(l_tempFuelConsumption, 1,0,0,1)
        else:
          ac.setText(l_tempFuelConsumption,"Current fuel consumption: {:.2f}l/100km".format(currentFuelConsumption))
          ac.setFontColor(l_tempFuelConsumption, 0.86, 0.86, 0.86, 1)
        fuelStateTemp = fuel
        economyOdometer = 0
        if odometer > 0.5:
          ac.setText(l_avgFuelConsumption,"Fuel consumption: {:.2f}l/100km".format(fuelConsumption))
      elif economyTimer > 1 and odometer > 0.5:
        fuelConsumedState = fuelStateTemp - fuel
        if economyOdometer > 0.0001:
          ac.setText(l_avgFuelConsumption,"Fuel consumption: {:.2f}l/100km".format(fuelConsumption))
        else:
          ac.setText(l_tempFuelConsumption,"Current fuel consumption: {:.1f}l/h".format(fuelConsumedState*3600))
          ac.setText(l_avgFuelConsumption,"Fuel consumption: {:.2f}l/100km".format(fuelConsumption))
          ac.setFontColor(l_tempFuelConsumption, 0.86, 0.86, 0.86, 1)
        fuelStateTemp = fuel
        economyOdometer = 0 
      elif economyTimer > 1:
         fuelConsumedState = fuelStateTemp - fuel
         ac.setText(l_tempFuelConsumption,"Current fuel consumption: {:.1f}l/h".format(fuelConsumedState*3600))
         ac.setFontColor(l_tempFuelConsumption, 0.86, 0.86, 0.86, 1)
         fuelStateTemp = fuel
         economyOdometer = 0
      fuelState = fuel
    
    if fuelDrivenState == 0 or fuel > fuelDrivenState or fuelDrivenState - fuel > 0.01:
      fuelDrivenState = info.physics.fuel
    elif speed > 0.1:
      drivenTimer += deltaT
      fuelDriven += fuelDrivenState - fuel
      fuelRangeTime = fuel / (fuelDriven / (drivenTimer / 60))
      if updateTimer > 0.1:
        ac.setText(l_fuelRangeTime,"Fuel range: {:.2f} minutes".format(fuelRangeTime))
      fuelDrivenState=fuel
    elif fuelDriven != 0 and drivenTimer != 0:
      fuelRangeTime = fuel / (fuelDriven / (drivenTimer / 60))
      if updateTimer > 0.1:
        ac.setText(l_fuelRangeTime,"Fuel range: {:.2f} minutes".format(fuelRangeTime))
      fuelDrivenState=fuel
    elif fuelDriven == 0 and drivenTimer == 0:
      if updateTimer > 0.1:
        ac.setText(l_fuelRangeTime,"Fuel range: No data")

    if avgFuelConsumptionPerLap == 0:
      fuelRangeLaps = 0
    else:
      fuelRangeLaps = fuel / avgFuelConsumptionPerLap
    if fuelConsumption == 0:
      fuelRangeKM = 0.001
    else:
      fuelRangeKM = (fuel / fuelConsumption) * 100

  
    
    if updateTimer > 0.1:
      ac.setText(l_speed, "Speed: {:.1f}".format(speed))

      ac.setText(l_rpm, "RPM: {:.0f}".format(rpm))

      ac.setText(l_boost, "Boost: {:.2f}".format(boost))  

      ac.setText(l_fuelRangeKM, "Fuel range: {:.2f}km".format(fuelRangeKM))

      ac.setText(l_odometer, "Distance {:.2f}".format(odometer))

      ac.setText(l_fuel, "Fuel: {:.2f}".format(fuel))

      ac.setText(l_fuelRangeLaps, "Fuel range: {:.2f} laps".format(fuelRangeLaps))
  
       

    if updateTimer > 0.1:
       updateTimer = 0
    if economyTimer > 1:
       economyTimer = 0
    if prevLapFuelColorTimer > 10:
       ac.setFontColor(l_prevLapFuelConsumption, 0.86, 0.86, 0.86, 1)
       prevLapFuelColorTimer = 0