import eel

eel.init("web")

def screenControl():
    while True:
        print("I'm a thread")
        eel.sleep(1.0) 

eel.spawn(screenControl)

eel.start("index.html", cmdline_args=["--kiosk"])

