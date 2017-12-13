import socket

import rospy

import libnmea_navsat_driver.driver

if __name__ == '__main__':
    rospy.init_node('nmea_serial_driver')

    tcp_port = rospy.get_param('~tcp_port', 8000)
    tcp_ip = rospy.get_param('~tcp_ip', '192.168.42.1')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((tcp_ip,tcp_port))
    sentence = ''
    new_sentence = False
    frame_id = libnmea_navsat_driver.driver.RosNMEADriver.get_frame_id()

    try:
        driver = libnmea_navsat_driver.driver.RosNMEADriver()
        while not rospy.is_shutdown():
            data = sock.recv(1)
            if data == '$' and not new_sentence:
                new_sentence = True
                sentence += data
            elif data == '\r':
                try:
                    driver.add_sentence(sentence, frame_id)
                    new_sentence = False
                    sentence = ''
                except ValueError as e:
                    rospy.logwarn("Value error, likely due to missing fields in the NMEA message. Error was: %s. Please report this issue at github.com/ros-drivers/nmea_navsat_driver, including a bag file with the NMEA sentences that caused it." % e)
            elif new_sentence:
                sentence += data

    except rospy.ROSInterruptException:
        sock.close() #Close GPS serial port
