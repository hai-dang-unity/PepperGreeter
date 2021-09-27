from naoqi import ALProxy
import time
import random
# import thread
import socket
from multiprocessing import Value,Queue

class PepperAction:


    def __init__(self, pepper):
        self.robotIp = pepper.ip
        self.port = pepper.port

    def wait(self):
        motion = ALProxy("ALMotion", self.robotIp, self.port)
        names = ['HeadYaw', 'HeadPitch']
        times = [[0.7], [0.7]]

        motion.angleInterpolation(names, [0.0, -0.16], times, True)
        time.sleep(3)
        motion.setAngles(names, [0.0, -0.26179], 0.2)

        return str(0)

    # def touch_sensor(opt):
    #     host =  # ip and port of mbed_usb.py with FSR touch sensor
    #     port = 12395
    #     s = socket.socket()
    #     s.connect((host, port))
    #     s.send(opt)
    #     l = s.recv(1024)
    #     s.close()
    #     print('reward=' + str(l))
    #     return str(l)

    def hello(self):
        names = list()
        times = list()
        keys = list()

        names.append("LElbowRoll")
        times.append([1, 1.5, 2, 2.5])
        keys.append([-1.02102, -0.537561, -1.02102, -0.537561])

        names.append("LElbowYaw")
        times.append([1, 2.5])
        keys.append([-0.66497, -0.66497])

        names.append("LHand")
        times.append([2.5])
        keys.append([0.66])

        names.append("LShoulderPitch")
        times.append([1, 2.5])
        keys.append([-0.707571, -0.707571])

        names.append("LShoulderRoll")
        times.append([1, 2.5])
        keys.append([0.558505, 0.558505])

        names.append("LWristYaw")
        times.append([1, 2.5])
        keys.append([-0.0191986, -0.0191986])
        names2 = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
        angles = [-0.479966, -0.561996, 0.66, 1.30202, 0.195477, -0.637045]
        motion = ALProxy("ALMotion", self.robotIp, 9559)
        motion.setExternalCollisionProtectionEnabled("Arms", False)
        tts = ALProxy("ALTextToSpeech", self.robotIp, self.port)
        tts.setParameter("speed", 100)
        tts.setLanguage("English")
        motion.angleInterpolation(names, keys, times, True)
        tts.say("Hello")
        motion.setAngles(names2, angles, 0.3)

        return str(0)

    def wave_hello(self, msg):
        names = list()
        times = list()
        keys = list()

        names.append("LElbowRoll")
        times.append([1, 1.5, 2, 2.5])
        keys.append([-1.02102, -0.537561, -1.02102, -0.537561])

        names.append("LElbowYaw")
        times.append([1, 2.5])
        keys.append([-0.66497, -0.66497])

        names.append("LHand")
        times.append([2.5])
        keys.append([0.66])

        names.append("LShoulderPitch")
        times.append([1, 2.5])
        keys.append([-0.707571, -0.707571])

        names.append("LShoulderRoll")
        times.append([1, 2.5])
        keys.append([0.558505, 0.558505])

        names.append("LWristYaw")
        times.append([1, 2.5])
        keys.append([-0.0191986, -0.0191986])
        names2 = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
        angles = [-0.479966, -0.561996, 0.66, 1.30202, 0.195477, -0.637045]

        self.motion.angleInterpolation(names, keys, times, True)
        self.pepper_speak(msg)
        self.motion.setAngles(names2, angles, 0.3)
        return

    def pepper_speak(self, msg):

        sentence = "\RSPD="+ str( 100 ) + "\ "
        sentence += "\VCT="+ str( 100 ) + "\ "
        sentence += msg
        sentence +=  "\RST\ "
        self.tts.say(str(sentence))

        return

    def shake_hand(self):
        names = list()
        times = list()
        keys = list()
        r = 0
        names.append("RHand")
        times.append([2])
        keys.append([0.98])

        names.append("RShoulderPitch")
        times.append([2])
        keys.append([-0.2058])

        names2 = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
        angles = [0.479966, 0.561996, 0.66, 1.30202, -0.195477, 0.637045]

        names3 = ["RHand"]
        angles2 = [0.5]

        motion = ALProxy("ALMotion", self.robotIp, 9559)
        motion.setExternalCollisionProtectionEnabled("Arms", False)
        tts = ALProxy("ALTextToSpeech", self.robotIp, self.port)
        tts.setParameter("speed", 60)
        tts.setLanguage("English")
        motion.setExternalCollisionProtectionEnabled("Arms", False)
        motion.angleInterpolation(names, keys, times, True)
        # r = touch_sensor(str(1))
        # if int(r) > 4:
        #     tts.say("Nice to meet you")
        #     thread.start_new_thread(touch_sensor, (str(2),))
        #     motion.setAngles(names3, angles2, 0.4)
        #     time.sleep(2)

        tts.say("Nice to meet you")
        motion.setAngles(names3, angles2, 0.4)
        time.sleep(2)

        motion.setAngles(names2, angles, 0.4)
        return r

