from blinkstick import blinkstick
import psutil

bstick = blinkstick.find_first()

if bstick is None:
    print ("No BlinkSticks found...")
else:
    print ("Displaying CPU usage (Green = 0%, Amber = 50%, Red = 100%)")
    print ("Press Ctrl+C to exit")
    
    #go into a forever loop
    while True:
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory().percent
        cpu_intensity = int(255 * cpu / 100)
        mem_intensity = int(255 * mem / 100)

        bstick.set_color(index=0,red=cpu_intensity,green=255 - cpu_intensity,blue=0)
        bstick.set_color(index=1,red=mem_intensity,green=255 - mem_intensity,blue=0)
