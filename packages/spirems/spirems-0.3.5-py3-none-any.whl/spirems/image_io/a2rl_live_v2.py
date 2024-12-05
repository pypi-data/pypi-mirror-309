#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from spirems.subscriber import Subscriber
from spirems.publisher import Publisher
from spirems.image_io.adaptor import sms2cvimg
from spirems import def_msg
from spirems.image_io.visual_helper import draw_charts_v2, load_a2rl_logo, track_boundary_parse, draw_track_map_v2
import cv2
import numpy as np
import threading
import time
import argparse
from datetime import datetime


img2 = np.ones((720, 1280, 3), dtype=np.uint8) * 200
img2_lock = threading.Lock()
img2_ready = False


def callback_f(msg):
    global img2, img2_ready
    with img2_lock:
        img2 = sms2cvimg(msg)
        img2_ready = True


a2rl_visual = None


def callback_monit(msg):
    global a2rl_visual
    a2rl_visual = msg


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f', '--full',
        action='store_true',
        help='Full Screen')
    parser.add_argument(
        '-i', '--ip',
        type=str,
        default='127.0.0.1',
        help='SpireMS Core IP')
    parser.add_argument(
        '-p', '--port',
        type=int,
        default=9094,
        help='SpireMS Core Port')
    args = parser.parse_args()

    sub = Subscriber('/flyeagle/lidar_map', 'sensor_msgs::CompressedImage', callback_f,
                     ip=args.ip, port=args.port)  # 47.91.115.171
    sub2 = Subscriber('/flyeagle/status', 'std_msgs::Null', callback_monit,
                      ip=args.ip, port=args.port)  # 47.91.115.171

    left_line, right_line, (map_w, map_h) = track_boundary_parse()
    running = True
    # default_img = load_a2rl_logo()
    default_img = np.ones((720, 1280, 3), dtype=np.uint8) * 30  # cv2.resize(default_img, (1280, 720))
    img = default_img

    if args.full:
        cv2.namedWindow('img', cv2.WINDOW_NORMAL)
        cv2.setWindowProperty('img', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    time_str = datetime.now().strftime("FlyEagleLive_%Y-%m-%d_%H-%M-%S.avi")
    out = cv2.VideoWriter(time_str, cv2.VideoWriter_fourcc(*'MJPG'), 27, (1280, 720))
    frame_cnt = 0
    t_cnt = 0.0
    while running:
        t1 = time.time()
        """
        if img2_on and img2_ready and img2 is not None:
            img = img2.copy()
            img = cv2.resize(img, (1280, 720))
        """
        img_show = draw_charts_v2(img, a2rl_visual)
        img_show = draw_track_map_v2(img_show, left_line, right_line, (map_w, map_h), a2rl_visual)
        with img2_lock:
            if img2_ready and img2 is not None:
                img2_resize = cv2.resize(img2, (688, 559))
                # img_map = img_show[:559, 296: 984, :]
                # img_map = cv2.addWeighted(img_map, 0.5, img2_resize, 0.5, 0)
                img_show[:559, 296: 984, :] = img2_resize

        cv2.imshow('img', img_show)
        c = cv2.waitKey(5)
        out.write(img_show)
        t2 = time.time()
        frame_cnt += 1
        if frame_cnt > 100:
            t_cnt += (t2 - t1)
            print("Run at {:.2f} Hz".format((frame_cnt - 100) / t_cnt))
