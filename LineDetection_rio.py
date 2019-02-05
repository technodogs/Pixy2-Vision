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


# pixy2 Line Detection #

pixy.init ()
pixy.change_prog ("line")

# Sync time #


# Pixy2 Line API #

class Vector (Structure):
  _fields_ = [
    ("m_x0", c_uint),
    ("m_y0", c_uint),
    ("m_x1", c_uint),
    ("m_y1", c_uint),
    ("m_index", c_uint),
    ("m_flags", c_uint) ]

class IntersectionLine (Structure):
  _fields_ = [
    ("m_index", c_uint),
    ("m_reserved", c_uint),
    ("m_angle", c_uint) ]

vectors = VectorArray(100)
intersections = IntersectionLineArray(100)
frame = 0

# Send data to NetworkTables #

while 1:
  line_get_all_features()
  i_count = line_get_intersections (100, intersections)
  v_count = line_get_vectors (100, vectors)

  if i_count > 0 or v_count > 0:
    print('frame %3d:' % (frame))
    frame = frame + 1
    m_Intsctn_index_list = []
    m_Intsctn_angle_list = []
    m_Intsctn_frame_list = []

    m_Line_index_list = []
    m_Line_x0pos_list = []
    m_Line_y0pos_list = []
    m_Line_x1pos_list = []
    m_Line_y1pos_list = []
    m_Line_width_list = []
    m_Line_length_list = []
    m_Line_flags_list = []
    
    for index in range (0, i_count):
      print('[INTERSECTION: INDEX=%d ANGLE=%d]' % (intersections[index].m_index, intersections[index].m_angle))
      #SENDTONETWORKTABLES#
      m_Intsctn_index_list.append(intersections[index].m_Intsctn_index)
      m_Intsctn_angle_list.append(intersections[index].m_Intsctn_angle)
      m_Intsctn_frame_list.append(intersections[index].m_Intsctn_frame)
        

    for index in range (0, v_count):
      print('[VECTOR: INDEX=%d X0=%3d Y0=%3d X1=%3d Y1=%3d]' % (vectors[index].m_index, vectors[index].m_x0, vectors[index].m_y0, vectors[index].m_x1, vectors[index].m_y1))
      #SENDTONETWORKTABLES#
      linewidth = vectors[index].m_x1 - vectors[index].m_x0
      linelength = vectors[index].m_y1 - vectors[index].m_x0
      m_Line_index_list.append(vectors[index].m_Line_index)
      m_Line_x0pos_list.append(vectors[index].m_Line_x0pos)
      m_Line_y0pos_list.append(vectors[index].m_Line_y0pos)
      m_Line_x1pos_list.append(vectors[index].m_Line_x1pos)
      m_Line_y1pos_list.append(vectors[index].m_Line_y1pos)
      m_Line_width_list.append(vectors[index].linewidth)
      m_Line_length_list.append(vectors[index].linelength)
      m_Line_flags_list.append(vectors[index].m_Line_flags)

      #table.putNumber('Line_index', vectors[index].m_index)
      #table.putNumber('Line_x0pos', vectors[index].m_x0)
      #table.putNumber('Line_y0pos', vectors[index].m_y0)
      #table.putNumber('Line_x1pos', vectors[index].m_x1)
      #table.putNumber('Line_y1pos', vectors[index].m_y1)
      #table.putNumber('Line_width', linewidth)
      #table.putNumber('Line_length', linelength)               
      #table.putNumber('Line_flags', vectors[index].m_flags)
          
    # table.putNumberArray('signature', m_signature_list )
    table.putNumberArray('index' ,m_Line_index_list)
    table.putNumberArray('x0' ,m_Line_x0pos_list)
    table.putNumberArray('yo' ,m_Line_y0pos_list)
    table.putNumberArray('x1' ,m_Line_x1pos_list)
    table.putNumberArray('y1' ,m_Line_y1pos_list)
    table.putNumberArray('width' ,m_Line_width_list)
    table.putNumberArray('length' ,m_Line_length_list)
    table.putNumberArray('flags' ,m_Line_flags_list)
    
