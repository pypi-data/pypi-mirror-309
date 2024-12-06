# JulianPy
JulianPy is a API made by Themeatly2 and Harsizcool to interface with Julian's Editor games in a very basic, but efficient way.

## Todo:
- Add basic controls (like keyboard inputs, chat, etc.) -  Done
- Add tools (like hasWifi()) - Done
- Add websocket communication
- Add other things (like Community API, Marketplace API, etc.)

## Example
```
import julianpy
import time

id = "https://s.julianseditor.com/3An5lL".replace("https://s.julianseditor.com/", "")
julian = julianpy.Astronaut(id)

julian.holdKey("d", 1)
time.sleep(1)
julian.sendMessage("Hello from Python!")
time.sleep(3)
julian.die()

```