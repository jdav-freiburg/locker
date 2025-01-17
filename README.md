# Fjaelllada - RFID controlled lockers 

> The following documentation is still work in progress, 
> for example documentation for the `depot_bay` flavor is very incomplete.

RFID accesible hardware lockers.  
Fjaelllada comes in two flavours:
* `depot_bay`: The big locker station used downstairs
* `seil_locker`: Single lock locker used upstairs for the ropes.

## Hardware

### depot_bay
_todo_

### seil_locker
See the [depot-oben-eda](depot-oben-eda) folder for kicad Drawings
Open the project file with [KiCad](https://www.kicad.org/) (used version is 8) to view the schematic and board design
for the small transistor board for opening the solenoid.

The pinout for the Raspberry Pi is as follows (BCM numbering!):

Pull up `SWITCH` to turn on the solenoid, don't hold too long because it tends to overheat quite fast. (<= 500 ms)
`CHECK` is high-z when the locker is open and GND when it is closed. To prevent floating state
pull up the GPIO pin to which `CHECK` is connected.

| Board Pin | RaspberryPi Pin |
| :-------- | :-------------- |
| SWITCH    | GPIO21          |
| CHECK     | GPIO20          |
| GND       | GND             |

For pinout info see [pinout.xyz/](https://pinout.xyz/)

## Software
See the [Software Docs](software/README.md) for details.

## Deployment

There is seperate [guide](Deployment.md) for how to deploy the software from scratch.
