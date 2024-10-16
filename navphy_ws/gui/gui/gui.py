# SDP Team 12
# Author: Samuel Almeida
# Date created: 3/28/24
# Date last modified: 3/28/24
# A ROS node which runs the GUI for our robot

import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from std_msgs.msg import Float32,Int32

import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
import subprocess
import json
import time
import threading
from threading import Thread
import os
import signal

class RosGUI(Node):
    navigate = 0
    start_macro = 0
    def __init__(self):
        super().__init__('gui')
        # self.publisher_ = self.create_publisher(String, 'topic', 10)
        # timer_period = 0.5  # seconds
        # self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0
        recording_timer_period = 1
        self.target_id = 0
        self.get_time_left = self.create_subscription(
            Float32,
            '/recording_time',
            self.update_recording_time,
        10)
        self.get_time_left = self.create_subscription(
            Float32,
            '/recording_max_time',
            self.update_max_recording_time,
        10)
        self.get_target = self.create_subscription(
            Int32,
            '/target_id',
            self.update_target_id,
        10)

        self.can_navigate_pub = self.create_publisher(Int32, "/can_navigate", 1)
        self.start_macro_pub = self.create_publisher(Int32, "/can_start_macros", 1)

        self.recording_time = 0
        self.max_recording_time = 10
        self.navigate_ros = Int32()
        self.start_macro_ros = Int32()
        self.navigate_ros.data = 0
        self.create_timer(.6,self.can_navigate)
        self.create_timer(.6,self.can_start_macros)

    def update_recording_time(self,msg):
        self.recording_time = msg.data
        # print("Hi")
    def update_max_recording_time(self,msg):
        # print("hi")
        self.max_recording_time = msg.data

    def update_target_id(self,msg):
        # print("hi")
        self.target_id = msg.data

    def can_navigate(self):
        self.navigate_ros.data = self.navigate
        self.can_navigate_pub.publish(self.navigate_ros)

    def can_start_macros(self):
        self.start_macro_ros.data = self.start_macro
        self.start_macro_pub.publish(self.start_macro_ros)

    # Add widgets here (e.g., labels, buttons, etc.)


    # def timer_callback(self):
    #     msg = String()
    #     msg.data = 'Hello World: %d' % self.i
    #     self.publisher_.publish(msg)
    #     self.get_logger().info('Publishing: "%s"' % msg.data)
    #     self.i += 1

def main(args=None):
    rclpy.init(args=args)

    gui = RosGUI()

    t1 = Thread(target=start_ros,args=[gui]).start()
    t2 = Thread(target=create_gui,args=[gui]).start()

    print("GUI startup completed successfully!")

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)

if __name__ == '__main__':
    main()

def start_ros(node : Node):
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
    
def create_gui(node : Node):
    gui = GUI(node)
    return gui

class GUI:
    def __init__(self, node : Node):
        self.node = node
        self.window = tk.Tk()
        self.window.geometry("600x250")

        btn1 = ttk.Button(text="Launch Target Tracking", command=lambda:self.launch(0))
        btn1.grid(row=0,column=0)

        btn2 = ttk.Button(text="Launch Nav", command=lambda:self.launch(1))
        btn2.grid(row=2,column=0)

        btn3 = ttk.Button(text="Launch Test", command=lambda:self.launch(2))
        btn3.grid(row=4,column=0)

        inputL = ttk.Entry(textvariable="Enter list of targets,marker size (mm), and recording time(s) like this => [(1,100,10),(59,40,60),(2,10,10)]",width=50)
        inputL.grid(row=6,column=1,columnspan=2)
        # inputL.insert(0,string="Enter list of targets like this => [1,59,2]")

        btn3 = ttk.Button(text="Add Targets", command=lambda:self.launch(3,inputL.get()))
        btn3.grid(row=6,column=0)

        btn4 = ttk.Button(text="Clear targets", command=lambda:self.launch(4))
        btn4.grid(row=8,column=0)

        btn5 = ttk.Button(text="Use Mic", command=lambda:self.launch(5))
        btn5.grid(row=10,column=0)

        btn5 = ttk.Button(text="Toggle Navigation", command=lambda:self.update_navigate())
        btn5.grid(row=13,column=0)

        btn6 = ttk.Button(text="Toggle Macros", command=lambda:self.update_macros())
        btn6.grid(row=15,column=0)

        # btn6 = ttk.Button(text="Update Recording Time", command=lambda:subprocess.Popen(['ros2','param','set','/target_pub','recording_timeout',str(inputR.get())]))
        # btn6.grid(row=12,column=0)

        self.progress_label_var = StringVar()
        self.progress_label = ttk.Label(textvariable=self.progress_label_var)
        self.progress_label_var.set("Recording progress at 0.0%")
        self.progress_label.grid(row=18,column=0)
        self.progress_var = DoubleVar()
        self.progress = ttk.Progressbar(variable=self.progress_var,maximum=1)
        self.progress.grid(row=18,column=1,columnspan=5)

        # btn6 = ttk.Button(text="Quit", command=lambda:os.kill(os.getpid(), signal.SIGINT))
        # btn6.grid(row=16,column=0)

        # Add widgets here (e.g., labels, buttons, etc.)
        
        # Start the GUI event loop
        print("Initializing system...")
        # subprocess.run("./scripts/system_init.sh")
        open("targets.txt", "w").close() # clear text file

        self.update_progress()

        self.window.mainloop()

    def update_progress(self):
        # print("updating")
        # self.progress.value = 100
        # print(self.node.recording_time,self.node.max_recording_time)
        progress = abs(round(float(self.node.recording_time)/float(self.node.max_recording_time),2))
        self.progress_var.set(abs(float(self.node.recording_time)/float(self.node.max_recording_time)))
        self.progress_label_var.set(f"Recording progress at: {progress*100}% for target: {self.node.target_id}",)
        self.window.after(1000, self.update_progress)
    
    def update_navigate(self):
        self.node.navigate = 1 - self.node.navigate
    
    def update_macros(self):
        self.node.start_macro = 1 - self.node.start_macro
        
    def launch(self, arg: int, target_list = [9999]):
        match arg:
            case 0:
                # global tracking_pid
                # tracking_cmd_list = ["ros2", "launch", "basic_mobile_robot", "target_tracking.launch.py"]
                tracking_pid = subprocess.Popen("./scripts/run_target_tracking.sh")
                print("Running target tracking")
                # p2 = subprocess.run(["pgrep", "pub"])
            case 1:
                # global nav_pid
                nav_pid = subprocess.Popen("./scripts/run_navigation.sh")
                print("Running nav")
                # nav_pid = p.pid
            case 2:
                # global test_pid
                test_pid= subprocess.Popen("./scripts/run_test.sh")
                print("Running teleop testing with SLAM")
                # test_pid = p.pid
            case 3:
                # just make this case update the text file that you have or change the node with the input "target_list"
                t_list = None
                try: t_list = json.loads(target_list)
                except json.decoder.JSONDecodeError as E:
                    print("Update failed: incorrect list format, please type in list notation. EX: [1,2]")
                    print(target_list)
                if type(t_list) == list:
                    if os.stat("targets.txt").st_size == 0:
                            try:
                                with open("targets.txt", "+w") as f:
                                    # print('AAAH')
                                    json.dump(t_list,f)
                            except json.decoder.JSONDecodeError as j:
                                print("Update failed: incorrect list format, please type in list notation. EX: [1,2]")
                    else:
                        with open("targets.txt") as f:
                            targetL = json.load(f)
                            temp = targetL.copy()
                            targetL += t_list
                        try:
                            with open("targets.txt","+w") as f:
                                json.dump(targetL,f)
                        except json.decoder.JSONDecodeError as j:
                            json.dump(temp)
                            print("Update failed: incorrect list format, please type in list notation. EX: [1,2]")

                    print("Updated list", t_list, type(t_list))
                else:
                    print("Update failed: incorrect list format, please type in list notation. EX: [1,2]")
            case 4:
                print("Clearing all targets from log file...")
                open("targets.txt", "w").close() # clear text file
            case 5:
                p = subprocess.Popen("./scripts/mic.sh")
                print("Using microphone input")