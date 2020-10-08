from blinkstick import blinkstick
from syslog import syslog
from time import sleep, strftime, localtime
import psutil, socket

# Helper function - figures out if passed value could be converted to an integer
def is_integer(n):
    try:
        int(n)
    except ValueError:
        return False
    else:
        return True


# Determines node number if hostname is formatted as k8s node
def get_k8s_node_num():
    # Get last char of hostname and figure out if int or char
    hostname = socket.gethostname()
    syslog('Hostname is ' + hostname)

    # Get last char of hostname and attept to convert to int; return 0 if non int, else return int
    if is_integer(hostname[-1]):
        return float(hostname[-1]) / 10
    else:
        return 0


# Blink front LED three times to indicate service/application start
def blink_startup(b):
    b.set_color(index=0,red=0,green=0,blue=0)
    b.set_color(index=1,red=0,green=0,blue=0)
    b.blink(index=0,red=0,green=0,blue=255,repeats=3)


# Blink back LED to indicate node number
def blink_node_num(b,n):
    b.set_color(index=0,red=0,green=0,blue=0)
    b.set_color(index=1,red=0,green=0,blue=0)
    b.blink(index=1,red=255,green=255,blue=255,repeats=n)


def resource_indication(bstick,offset):
    #go into a forever loop
    syslog('Entering monitoring loop.')
    while True:

        t = localtime()
        now = strftime("%S", t)
        
        if now == "00":
            # sleep for a fraction of a second = node number
            if offset <> 0:
                sleep(offset)
            
            # Set blinkstick colors
            bstick.set_color(index=0,red=0,green=0,blue=255)
            bstick.set_color(index=1,red=0,green=0,blue=255)

            # Sleep for 0.5 seconds to let colors dwell before they are returned to resource indication
            if offset <> 0:
                sleep(0.5)

        else:
            cpu = psutil.cpu_percent(interval=1)
            mem = psutil.virtual_memory().percent
            cpu_intensity = int(255 * cpu / 100)
            mem_intensity = int(255 * mem / 100)

            bstick.set_color(index=0,red=cpu_intensity,green=255 - cpu_intensity,blue=0)
            bstick.set_color(index=1,red=mem_intensity,green=255 - mem_intensity,blue=0)


# Christmas das blinkenlights instead of indicating resource utilization
# Green/Red lights only
def christmas_indication_gr(bstick,offset):
    from random import randint

    syslog('Entering christmas g/r mode.')

    # Enter randomize starting state
    i = 0
    while (i <= 1):
        light_color = randint(1,3)
        if light_color == 1:
            r = 255
            g = 0
        elif light_color == 2:
            r = 0
            g = 255
        else:
            r = 0
            g = 0
        bstick.set_color(index=i,red=r,green=g,blue=0)
        i += 1

    #go into a forever loop
    while True:
        light_color = randint(1,3)
        light_duration = randint(1,12)
        light_index = randint(0,1)
        if light_color == 1:
            r = 255
            g = 0
        elif light_color == 2:
            r = 0
            g = 255
        else:
            r = 0
            g = 0
        bstick.set_color(index=light_index,red=r,green=g,blue=0)
        sleep(light_duration)


def halloween_indication(bstick, offset):
    from random import randint

    syslog('Entering haloween p/o mode.')

    # Enter randomize starting state
    i = 0
    while (i <= 1):
        light_color = randint(1,3)
        # purple
        if light_color == 1:
            r = 140
            g = 0
            b = 255
        # orange
        elif light_color == 2:
            r = 255
            g = 128
            b = 0
        # off
        else:
            r = 0
            g = 0
            b = 0
        bstick.set_color(index=i,red=r,green=g,blue=b)
        i += 1

    #go into a forever loop
    while True:
        light_color = randint(1,3)
        light_duration = randint(1,12)
        light_index = randint(0,1)
        # purple
        if light_color == 1:
            r = 140
            g = 0
            b = 255
        # orange
        elif light_color == 2:
            r = 255
            g = 128
            b = 0
        # off
        else:
            r = 0
            g = 0
            b = 0
        bstick.set_color(index=light_index,red=r,green=g,blue=b)
        sleep(light_duration)


def main():
    bstick = blinkstick.find_first()

    if bstick is None:
        syslog(syslog.LOG_ERR, 'Blinkstick not found, exiting...')
        exit()
    else:    
        syslog('Blinkstick found.')

    offset = get_k8s_node_num()
    syslog('Offset is ' + str(offset) + ' seconds')

    blink_startup(bstick)
    if offset <> 0:
        blink_node_num(bstick,int(offset*10))

    #resource_indication(bstick,offset)
    #christmas_indication_gr(bstick,offset)
    halloween_indication(bstick,offset)

    syslog("Exiting normally.")


if __name__ == "__main__":
    # execute only if run as a script
    main()