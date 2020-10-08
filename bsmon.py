from blinkstick import blinkstick
import psutil, syslog, time, socket

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
    syslog.syslog('Hostname is ' + hostname)

    # Get last char of hostname and attept to convert to int; return 0 if non int, else return int
    if is_integer(hostname[-1]):
        return float(hostname[-1]) / 10
    else:
        return 0


# Blink LED 0 three 3 times to indicate service/application start
def blink_startup(b):
    b.set_color(index=0,red=0,green=0,blue=0)
    b.set_color(index=1,red=0,green=0,blue=0)
    b.blink(index=0,red=0,green=0,blue=255,repeats=3)


# Blink LED 1 to indicate node number
def blink_node_num(b,n):
    b.set_color(index=0,red=0,green=0,blue=0)
    b.set_color(index=1,red=0,green=0,blue=0)
    b.blink(index=1,red=255,green=255,blue=255,repeats=n)


def main():
    bstick = blinkstick.find_first()

    if bstick is None:
        syslog.syslog(syslog.LOG_ERR, 'Blinkstick not found, exiting...')
        exit()
    else:    
        syslog.syslog('Blinkstick found.')

    offset = get_k8s_node_num()
    syslog.syslog('Offset is ' + str(offset) + ' seconds')

    blink_startup(bstick)
    if offset <> 0:
        blink_node_num(bstick,int(offset*10)

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


if __name__ == "__main__":
    # execute only if run as a script
    main()