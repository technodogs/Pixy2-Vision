import threading
from networktables import NetworkTables
import time
import netifaces as ni
import psutil as ps

# Configure network and NetworkTables (Amend to 10.37.07.2) #

cond = threading.Condition()
notified = [False]

def log(logMessage):
  print("Pi_Info: " + logMessage)

def connectionListener(connected, info):
    print(info, '; Connected=%s' % connected)
    with cond:
        notified[0] = True
        cond.notify()

def getIPAddress(interface='eth0'):
    '''
    Get the IP address for the given interface (eth0 if not specified)
    '''
    ip = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
    return str(ip)

def getProcessRunning(processName='motion',commandLine=''):
    pids = ps.pids()
    procs = [ps.Process(x) for x in pids] # get the process objects
    names = [x.name() for x in procs]
    cmdlines = [x.cmdline() for x in procs]
    #import pdb;pdb.set_trace()
    if(commandLine != ''):
        #use the command line
        #probably have to loop through all sub-lists
        for cmd in cmdlines:
            if isinstance(cmd, list):
                for cmdstring in cmd:
                    if commandLine in cmdstring:
                        return True
            elif isinstance(cmd, str):
                return commandLine in cmdlines
    else:
        #use the process name
        return processName in names

def getCPUPercent():
    pct = ps.cpu_percent()
    return str(pct) # convert to a string

def getRAMPercent():
    pct = ps.virtual_memory()._asdict()['percent']
    return str(pct) # convert to a string

while True: # This loop should run forever.

    try:
        NetworkTables.initialize(server='10.37.7.2') # Connect to the NetworkTables server running on the roboRIO
        NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)

        with cond:
            log("Waiting")
            if not notified[0]:
                cond.wait()
                
        log("Connected!")
        datatable = NetworkTables.getTable('Pi_Data')
        datatable.putString("ip_address", getIPAddress())
        isPixyRunning = getProcessRunning(processName='python2', commandLine='LineDetection_rio.py')
        isMotionRunning = getProcessRunning(processName='python', commandLine='')
        #import pdb;pdb.set_trace()
        datatable.putBoolean("pixy_running", isPixyRunning)
        datatable.putBoolean("motion_running", isMotionRunning)
        datatable.putString('cpu_utilization', getCPUPercent())
        datatable.putString('ram_utilization', getRAMPercent())

        #configtable = NetworkTables.getTable('Pi_Config')
        # Use the config table to read things FROM the network tables to configure the pi

    except Exception as e:
        log("An ERROR occurred.")
        log(str(e))
    time.sleep(1) # in either case, only update once per second.
