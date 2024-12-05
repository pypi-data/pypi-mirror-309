#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import rclpy
from rclpy.node import Node
from a2rl_bs_msgs.msg import ControllerStatus, ControllerDebug, Localization, EgoState, VectornavIns, FlyeagleEyePlannerReport
from eav24_bsu_msgs.msg import Wheels_Speed_01, HL_Msg_01, HL_Msg_02, HL_Msg_03, ICE_Status_01, ICE_Status_02, PSA_Status_01, Tyre_Surface_Temp_Front
from sensor_msgs.msg import PointCloud2
import time
import os
import yaml
import json
import threading
import numpy as np
import ros2_numpy
import cv2
from spirems import Publisher, Subscriber, def_msg, cvimg2sms
import psutil


"""
依赖项安装：
pip install spirems, ros2-numpy, psutil, pynvjpeg
"""


def cpu_monit(sms_msg):
    cpu_cnt = psutil.cpu_count()
    cpu_percent = psutil.cpu_percent(interval=0.1)
    sms_msg['cpu'] = cpu_percent
    # cpu_freq = psutil.cpu_freq(percpu=False)

    virtual_memory = psutil.virtual_memory()
    sms_msg['mem'] = virtual_memory.used / 1024 / 1024 / 1024

    disk_usage = psutil.disk_usage('/')
    sms_msg['disk'] = disk_usage.used / 1024 / 1024 / 1024 / 1024

    sensors_temperatures = psutil.sensors_temperatures()
    if 'coretemp' in sensors_temperatures:
        sms_msg['cpu_temp'] = sensors_temperatures['coretemp'][0].current
    elif 'k10temp' in sensors_temperatures:
        sms_msg['cpu_temp'] = sensors_temperatures['k10temp'][0].current

    return sms_msg


# ==============================================================================
#                                                                   SCALE_TO_255
# ==============================================================================
def scale_to_255(a, min, max, dtype=np.uint8):
    """ Scales an array of values from specified min, max range to 0-255
        Optionally specify the data type of the output (default is uint8)
    """
    return (((a - min) / float(max - min)) * 255).astype(dtype)


# ==============================================================================
#                                                         POINT_CLOUD_2_BIRDSEYE
# ==============================================================================
def point_cloud_2_birdseye(points,
                           res=0.1,
                           side_range=(-40., 40.),  # left-most to right-most
                           fwd_range=(-30., 30.), # back-most to forward-most
                           height_range=(-2., 2.),  # bottom-most to upper-most
                           ):
    """ Creates an 2D birds eye view representation of the point cloud data.

    Args:
        points:     (numpy array)
                    N rows of points data
                    Each point should be specified by at least 3 elements x,y,z
        res:        (float)
                    Desired resolution in metres to use. Each output pixel will
                    represent an square region res x res in size.
        side_range: (tuple of two floats)
                    (-left, right) in metres
                    left and right limits of rectangle to look at.
        fwd_range:  (tuple of two floats)
                    (-behind, front) in metres
                    back and front limits of rectangle to look at.
        height_range: (tuple of two floats)
                    (min, max) heights (in metres) relative to the origin.
                    All height values will be clipped to this min and max value,
                    such that anything below min will be truncated to min, and
                    the same for values above max.
    Returns:
        2D numpy array representing an image of the birds eye view.
    """
    # EXTRACT THE POINTS FOR EACH AXIS
    x_points = points[:, 0]
    y_points = points[:, 1]
    z_points = points[:, 2]

    # FILTER - To return only indices of points within desired cube
    # Three filters for: Front-to-back, side-to-side, and height ranges
    # Note left side is positive y axis in LIDAR coordinates
    f_filt = np.logical_and((x_points > fwd_range[0]), (x_points < fwd_range[1]))
    s_filt = np.logical_and((y_points > -side_range[1]), (y_points < -side_range[0]))
    filter = np.logical_and(f_filt, s_filt)
    indices = np.argwhere(filter).flatten()

    # KEEPERS
    x_points = x_points[indices]
    y_points = y_points[indices]
    z_points = z_points[indices]

    # CONVERT TO PIXEL POSITION VALUES - Based on resolution
    x_img = (-y_points / res).astype(np.int32)  # x axis is -y in LIDAR
    y_img = (-x_points / res).astype(np.int32)  # y axis is -x in LIDAR

    # SHIFT PIXELS TO HAVE MINIMUM BE (0,0)
    # floor & ceil used to prevent anything being rounded to below 0 after shift
    x_img -= int(np.floor(side_range[0] / res))
    y_img += int(np.ceil(fwd_range[1] / res))

    # CLIP HEIGHT VALUES - to between min and max heights
    pixel_values = np.clip(a=z_points,
                           a_min=height_range[0],
                           a_max=height_range[1])

    # RESCALE THE HEIGHT VALUES - to be between the range 0-255
    pixel_values = scale_to_255(pixel_values,
                                min=height_range[0],
                                max=height_range[1])

    # INITIALIZE EMPTY ARRAY - of the dimensions we want
    x_max = 1 + int((side_range[1] - side_range[0]) / res)
    y_max = 1 + int((fwd_range[1] - fwd_range[0]) / res)
    im = np.zeros([y_max, x_max, 3], dtype=np.uint8)

    # FILL PIXEL VALUES IN IMAGE ARRAY
    im[y_img, x_img, 1] = pixel_values
    im[y_img, x_img, 2] = pixel_values

    return im


class A2RLTeamFlyEagleMonitNode(Node, threading.Thread):
    def __init__(self):
        Node.__init__(self, 'A2RLTeamFlyEagleMonitNode')
        threading.Thread.__init__(self)

        self.latest_a2rl_vn_ins_msg = None
        self.latest_a2rl_vn_ins_lock = threading.Lock()
        self.latest_sensor_lidar_front_msg = None
        self.latest_sensor_lidar_front_lock = threading.Lock()
        self.latest_sensor_lidar_left_msg = None
        self.latest_sensor_lidar_left_lock = threading.Lock()
        self.latest_sensor_lidar_right_msg = None
        self.latest_sensor_lidar_right_lock = threading.Lock()
        self.latest_controller_debug_msg = None
        self.latest_controller_debug_lock = threading.Lock()
        self.latest_controller_status_msg = None
        self.latest_controller_status_lock = threading.Lock()
        self.latest_ego_loc_msg = None
        self.latest_ego_loc_lock = threading.Lock()
        self.latest_ego_state_msg = None
        self.latest_ego_state_lock = threading.Lock()
        self.latest_hlmsg_01_msg = None
        self.latest_hlmsg_01_lock = threading.Lock()
        self.latest_hlmsg_02_msg = None
        self.latest_hlmsg_02_lock = threading.Lock()
        self.latest_hlmsg_03_msg = None
        self.latest_hlmsg_03_lock = threading.Lock()
        self.latest_ice_status_01_msg = None
        self.latest_ice_status_01_lock = threading.Lock()
        self.latest_ice_status_02_msg = None
        self.latest_ice_status_02_lock = threading.Lock()
        self.latest_psa_status_01_msg = None
        self.latest_psa_status_01_lock = threading.Lock()
        self.latest_tyre_surface_temp_front_msg = None
        self.latest_tyre_surface_temp_front_lock = threading.Lock()
        self.latest_tyre_surface_temp_rear_msg = None
        self.latest_tyre_surface_temp_rear_lock = threading.Lock()

        self.a2rl_vn_ins_sub = self.create_subscription(
            VectornavIns,
            "/a2rl/vn/ins",
            self.a2rl_vn_ins_callback,
            10
        )
        self.sensor_lidar_front_sub = self.create_subscription(
            PointCloud2,
            "/sensor/lidar_front/points",
            self.sensor_lidar_front_callback,
            10
        )
        self.sensor_lidar_left_sub = self.create_subscription(
            PointCloud2,
            "/sensor/lidar_left/points",
            self.sensor_lidar_left_callback,
            10
        )
        self.sensor_lidar_right_sub = self.create_subscription(
            PointCloud2,
            "/sensor/lidar_right/points",
            self.sensor_lidar_right_callback,
            10
        )
        self.controller_debug_sub = self.create_subscription(
            ControllerDebug,
            "/a2rl/controller/debug",
            self.controller_debug_callback,
            10
        )
        self.controller_status_sub = self.create_subscription(
            ControllerStatus,
            "/a2rl/controller/status",
            self.controller_status_callback,
            10
        )
        self.ego_loc_sub = self.create_subscription(
            Localization,
            "/a2rl/observer/ego_loc/low_freq",
            self.ego_loc_callback,
            10
        )
        self.ego_state_sub = self.create_subscription(
            EgoState,
            "/a2rl/observer/ego_state/low_freq",
            self.ego_state_callback,
            10
        )
        self.hlmsg_01_sub = self.create_subscription(
            HL_Msg_01,
            "/a2rl/eav24_bsu/hl_msg_01",
            self.hlmsg_01_callback,
            10
        )
        self.hlmsg_02_sub = self.create_subscription(
            HL_Msg_02,
            "/a2rl/eav24_bsu/hl_msg_02",
            self.hlmsg_02_callback,
            10
        )
        self.hlmsg_03_sub = self.create_subscription(
            HL_Msg_03,
            "/a2rl/eav24_bsu/hl_msg_03",
            self.hlmsg_03_callback,
            10
        )
        self.ice_status_01_sub = self.create_subscription(
            ICE_Status_01,
            "/a2rl/eav24_bsu/ice_status_01",
            self.ice_status_01_callback,
            10
        )
        self.ice_status_02_sub = self.create_subscription(
            ICE_Status_02,
            "/a2rl/eav24_bsu/ice_status_02",
            self.ice_status_02_callback,
            10
        )
        self.psa_status_01_sub = self.create_subscription(
            PSA_Status_01,
            "/a2rl/eav24_bsu/psa_status_01",
            self.psa_status_01_callback,
            10
        )
        self.tyre_surface_temp_front_sub = self.create_subscription(
            Tyre_Surface_Temp_Front,
            "/a2rl/eav24_bsu/tyre_surface_temp_front",
            self.tyre_surface_temp_front_callback,
            10
        )
        self.tyre_surface_temp_rear_sub = self.create_subscription(
            Tyre_Surface_Temp_Front,
            "/a2rl/eav24_bsu/tyre_surface_temp_rear",
            self.tyre_surface_temp_rear_callback,
            10
        )
        self.init_sms_msg()
        self.sms_msg_pub = Publisher("/flyeagle/status", "std_msgs::Null")
        self.sms_lidar_pub = Publisher("/flyeagle/lidar_map", "sensor_msgs::CompressedImage")
        self.start()

    def a2rl_vn_ins_callback(self, msg):
        with self.latest_a2rl_vn_ins_lock:
            self.latest_a2rl_vn_ins_msg = msg
    
    def sensor_lidar_front_callback(self, msg):
        with self.latest_sensor_lidar_front_lock:
            self.latest_sensor_lidar_front_msg = msg
    
    def sensor_lidar_left_callback(self, msg):
        with self.latest_sensor_lidar_left_lock:
            self.latest_sensor_lidar_left_msg = msg
    
    def sensor_lidar_right_callback(self, msg):
        with self.latest_sensor_lidar_right_lock:
            self.latest_sensor_lidar_right_msg = msg
    
    def controller_debug_callback(self, msg):
        with self.latest_controller_debug_lock:
            self.latest_controller_debug_msg = msg
    
    def controller_status_callback(self, msg):
        with self.latest_controller_status_lock:
            self.latest_controller_status_msg = msg

    def ego_loc_callback(self, msg):
        self.latest_ego_loc_msg = msg

    def ego_state_callback(self, msg):
        self.latest_ego_state_msg = msg

    def hlmsg_01_callback(self, msg):
        self.latest_hlmsg_01_msg = msg

    def hlmsg_02_callback(self, msg):
        self.latest_hlmsg_02_msg = msg

    def hlmsg_03_callback(self, msg):
        self.latest_hlmsg_03_msg = msg

    def ice_status_01_callback(self, msg):
        with self.latest_ice_status_01_lock:
            self.latest_ice_status_01_msg = msg

    def ice_status_02_callback(self, msg):
        with self.latest_ice_status_02_lock:
            self.latest_ice_status_02_msg = msg

    def psa_status_01_callback(self, msg):
        with self.latest_psa_status_01_lock:
            self.latest_psa_status_01_msg = msg
    
    def tyre_surface_temp_front_callback(self, msg):
        with latest_tyre_surface_temp_front_lock:
            self.latest_tyre_surface_temp_front_msg = msg
    
    def tyre_surface_temp_rear_callback(self, msg):
        with latest_tyre_surface_temp_rear_lock:
            self.latest_tyre_surface_temp_rear_msg = msg
    
    def init_sms_msg(self):
        self.sms_msg = def_msg('std_msgs::Null')
        self.sms_msg['position_enu_ins'] = [0, 0, 0]
        self.sms_msg['velocity_body_ins'] = [0, 0, 0]
        self.sms_msg['acceleration_ins'] = [0, 0, 0]
        self.sms_msg['orientation_ypr'] = [0, 0, 0]
        self.sms_msg['ice_actual_gear'] = 1
        self.sms_msg['ice_actual_throttle'] = 0.0
        self.sms_msg['ice_engine_speed_rpm'] = 0.0
        self.sms_msg['ice_water_temp_deg_c'] = 0.0
        self.sms_msg['ice_oil_temp_deg_c'] = 0.0
        self.sms_msg['lateral_error'] = 0.0
        self.sms_msg['yaw_error'] = 0.0
        self.sms_msg['speed_error'] = 0.0
        self.sms_msg['front_brake'] = 0.0
        self.sms_msg['rear_brake'] = 0.0
        self.sms_msg['slip_f'] = 0.0
        self.sms_msg['slip_r'] = 0.0
        self.sms_msg['safe_stop_mode'] = 0
        self.sms_msg['reason_for_safestop'] = ''
        self.sms_msg['psa_actual_pos_rad'] = 0.0
        self.sms_msg['tyre_temp_fl'] = [0, 0, 0]
        self.sms_msg['tyre_temp_fr'] = [0, 0, 0]
        self.sms_msg['tyre_temp_rl'] = [0, 0, 0]
        self.sms_msg['tyre_temp_rr'] = [0, 0, 0]

    def run(self):
        lidar1_on = False
        lidar2_on = False
        lidar3_on = False
        while True:
            t1 = time.time()
            with self.latest_a2rl_vn_ins_lock:
                if self.latest_a2rl_vn_ins_msg is not None:
                    msg = self.latest_a2rl_vn_ins_msg
                    self.sms_msg['position_enu_ins'] = [msg.position_enu_ins.x, msg.position_enu_ins.y, msg.position_enu_ins.z]
                    self.sms_msg['velocity_body_ins'] = [msg.velocity_body_ins.x, msg.velocity_body_ins.y, msg.velocity_body_ins.z]
                    self.sms_msg['acceleration_ins'] = [msg.acceleration_ins.x, msg.acceleration_ins.y, msg.acceleration_ins.z]
                    self.sms_msg['orientation_ypr'] = [msg.orientation_ypr.x, msg.orientation_ypr.y, msg.orientation_ypr.z]
            with self.latest_sensor_lidar_front_lock:
                if self.latest_sensor_lidar_front_msg is not None:
                    msg = self.latest_sensor_lidar_front_msg
                    pcd_front = ros2_numpy.numpify(msg)['xyz']
                    lidar1_on = True
            with self.latest_sensor_lidar_left_lock:
                if self.latest_sensor_lidar_left_msg is not None:
                    msg = self.latest_sensor_lidar_left_msg
                    pcd_left = ros2_numpy.numpify(msg)['xyz']
                    lidar2_on = True
            with self.latest_sensor_lidar_right_lock:
                if self.latest_sensor_lidar_right_msg is not None:
                    msg = self.latest_sensor_lidar_right_msg
                    pcd_right = ros2_numpy.numpify(msg)['xyz']
                    lidar3_on = True
            with self.latest_ice_status_01_lock:
                if self.latest_ice_status_01_msg is not None:
                    msg = self.latest_ice_status_01_msg
                    self.sms_msg['ice_actual_gear'] = msg.ice_actual_gear
                    self.sms_msg['ice_actual_throttle'] = msg.ice_actual_throttle
            with self.latest_ice_status_02_lock:
                if self.latest_ice_status_02_msg is not None:
                    msg = self.latest_ice_status_02_msg
                    self.sms_msg['ice_engine_speed_rpm'] = msg.ice_engine_speed_rpm
                    self.sms_msg['ice_water_temp_deg_c'] = msg.ice_water_temp_deg_c
                    self.sms_msg['ice_oil_temp_deg_c'] = msg.ice_oil_temp_deg_c
            with self.latest_controller_debug_lock:
                if self.latest_controller_debug_msg is not None:
                    msg = self.latest_controller_debug_msg
                    self.sms_msg['lateral_error'] = msg.lateral_error
                    self.sms_msg['yaw_error'] = msg.yaw_error
                    self.sms_msg['speed_error'] = msg.speed_error
            with self.latest_controller_status_lock:
                if self.latest_controller_status_msg is not None:
                    msg = self.latest_controller_status_msg
                    self.sms_msg['front_brake'] = msg.front_brake
                    self.sms_msg['rear_brake'] = msg.rear_brake
                    self.sms_msg['slip_f'] = msg.slip_f
                    self.sms_msg['slip_r'] = msg.slip_r
                    self.sms_msg['safe_stop_mode'] = msg.safe_stop_mode
                    self.sms_msg['reason_for_safestop'] = msg.reason_for_safestop
            with self.latest_tyre_surface_temp_front_lock:
                if self.latest_tyre_surface_temp_front_msg is not None:
                    msg = self.latest_tyre_surface_temp_front_msg
                    self.sms_msg['tyre_temp_fl'] = [msg.outer_fl, msg.center_fl, msg.inner_fl]
                    self.sms_msg['tyre_temp_fr'] = [msg.outer_fr, msg.center_fr, msg.inner_fr]
            with self.latest_tyre_surface_temp_rear_lock:
                if self.latest_tyre_surface_temp_rear_msg is not None:
                    msg = self.latest_tyre_surface_temp_rear_msg
                    self.sms_msg['tyre_temp_rl'] = [msg.outer_rl, msg.center_rl, msg.inner_rl]
                    self.sms_msg['tyre_temp_rr'] = [msg.outer_rr, msg.center_rr, msg.inner_rr]
            with self.latest_psa_status_01_lock:
                if self.latest_psa_status_01_msg is not None:
                    msg = self.latest_psa_status_01_msg
                    self.sms_msg['psa_actual_pos_rad'] = msg.psa_actual_pos_rad
            if lidar1_on and lidar2_on and lidar3_on:
                pcd = np.concatenate((pcd_front, pcd_left, pcd_right), axis=0)
                img = point_cloud_2_birdseye(pcd)
                sms_img = cvimg2sms(img)
                self.sms_lidar_pub.publish(sms_img)
                # cv2.imshow('img', img)
                # cv2.waitKey(5)
            
            self.sms_msg = cpu_monit(self.sms_msg)
            self.sms_msg_pub.publish(self.sms_msg)
            # print(json.dumps(self.sms_msg, indent=4))


def main(args=None):
    rclpy.init(args=args)
    node = A2RLTeamFlyEagleMonitNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
