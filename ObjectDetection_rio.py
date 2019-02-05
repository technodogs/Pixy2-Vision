import pixy 
from ctypes import *
from pixy import *
import threading
from networktables import NetworkTables

# Configure network and NetworkTables (Amend to 10.37.07.2) #

cond = threading.Condition()
notified = [False]

def connectionListener(connected, info):
    print(info, '; Connected=%s' % connected)
    with cond:
        notified[0] = True
        cond.notify()

NetworkTables.initialize(server='10.37.7.2')
NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)

with cond:
    print("Waiting")
    if not notified[0]:
        cond.wait()

table = NetworkTables.getTable('PixyData')
#numberEntry = table.getEntry('Num1')

# Insert additional processing code here #
print("Connected!")


# Pixy2 Object Detection mode #

pixy.init ()
pixy.change_prog ("color_connected_components");

# Sync time #

# Pixy2 Object API #

class Blocks (Structure):
  _fields_ = [ ("m_signature", c_uint),
    ("m_x", c_uint),
    ("m_y", c_uint),
    ("m_width", c_uint),
    ("m_height", c_uint),
    ("m_angle", c_uint),
    ("m_index", c_uint),
    ("m_age", c_uint) ]

blocks = BlockArray(100)
frame = 0

# Send data to NetworkTables #

while 1:
  count = pixy.ccc_get_blocks (100, blocks)

  if count > 0:
    print('frame %3d:' % (frame))
    
    frame = frame + 1
    m_signature_list = []
    m_x_list = []
    m_y_list = []
    m_width_list = []
    m_height_list = []
    m_angle_list = []
    m_index_list = []
    m_age_list = []

    for index in range (0, count):
      print('[BLOCK: SIG=%d X=%3d Y=%3d WIDTH=%3d HEIGHT=%3d]' % (blocks[index].m_signature, blocks[index].m_x, blocks[index].m_y, blocks[index].m_width, blocks[index].m_height))
      #SENDTONETWORKTABLES#
      m_signature_list.append(blocks[index].m_signature)
      m_x_list.append(blocks[index].m_x)
      m_y_list.append(blocks[index].m_y)
      m_width_list.append(blocks[index].m_width)
      m_height_list.append(blocks[index].m_height)
      m_angle_list.append(blocks[index].m_angle)
      m_index_list.append(blocks[index].m_index)
      m_age_list.append(blocks[index].m_age)


      # table.putNumber('signature', blocks[index].m_signature)
      # table.putNumber('x_pos', blocks[index].m_x)
      # table.putNumber('y_pos', blocks[index].m_y)
      # table.putNumber('width', blocks[index].m_width)
      # table.putNumber('height', blocks[index].m_height)
      # table.putNumber('angle', blocks[index].m_angle)
      # table.putNumber('index', blocks[index].m_index)
      # table.putNumber('age', blocks[index].m_age)
      # table.putNumber('frame', frame)

    table.putNumberArray('signature', m_signature_list )
    table.putNumberArray('x_pos', m_x_list)
    table.putNumberArray('y_pos', m_y_list)
    table.putNumberArray('width', m_width_list)
    table.putNumberArray('height', m_height_list)
    table.putNumberArray('angle', m_angle_list)
    table.putNumberArray('index', m_index_list)
    table.putNumberArray('age', m_age_list)

