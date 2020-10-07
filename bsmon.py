from blinkstick import blinkstick
import psutil, syslog, time, socket

def is_integer(n):
    try:
        int(n)
    except ValueError:
        return False
    else:
        return True


bstick = blinkstick.find_first()

if bstick is None:
    syslog.syslog(syslog.LOG_ERR, 'Blinkstick not found, exiting...')
else:    
    syslog.syslog('Blinkstick found.')

    # Get last char of hostname and figure out if int or char
    hostname = socket.gethostname()
    syslog.syslog('Hostname is ' + hostname)

    if is_integer(hostname[-1]):
        offset = float(hostname[-1]) / 10
    else:
        offset = 0
    
    syslog.syslog('Offset is ' + str(offset) + ' seconds')

    #go into a forever loop
    syslog.syslog('Entering monitoring loop.')
    while True:

        t = time.localtime()
        now = time.strftime("%S", t)
        
        if now == "00":
            # sleep for a fraction of a second = node number
            if offset <> 0:
                time.sleep(offset)
            
            # Set blinkstick colors
            bstick.set_color(index=0,red=0,green=0,blue=255)
            bstick.set_color(index=1,red=0,green=0,blue=255)

            # Sleep for 0.5 seconds to let colors dwell before they are returned to resource indication
            if offset <> 0:
                time.sleep(0.5)

        else:
            cpu = psutil.cpu_percent(interval=1)
            mem = psutil.virtual_memory().percent
            cpu_intensity = int(255 * cpu / 100)
            mem_intensity = int(255 * mem / 100)

            bstick.set_color(index=0,red=cpu_intensity,green=255 - cpu_intensity,blue=0)
            bstick.set_color(index=1,red=mem_intensity,green=255 - mem_intensity,blue=0)

syslog.syslog("Exiting normally.")
