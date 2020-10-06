from blinkstick import blinkstick
import psutil, syslog

bstick = blinkstick.find_first()

if bstick is None:
    syslog.syslog(syslog.LOG_ERR, 'Blinkstick not found, exiting...')
else:    
    syslog.syslog('Blinkstick found, entering monitoring loop.')

    #go into a forever loop
    while True:
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory().percent
        cpu_intensity = int(255 * cpu / 100)
        mem_intensity = int(255 * mem / 100)

        bstick.set_color(index=0,red=cpu_intensity,green=255 - cpu_intensity,blue=0)
        bstick.set_color(index=1,red=mem_intensity,green=255 - mem_intensity,blue=0)

syslog.syslog("Exiting normally.")
