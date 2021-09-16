import qi
import argparse
import motion
import sys
import time

def userArmArticular(motion_service, tts):
    # Arms motion from user have always the priority than walk arms motion

    JointNamesL = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowYaw", "LElbowRoll"]
    # JointNamesR = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll"]

    # [    hand{-:up,+:down} | shoulder{-:right side horizontal movement,+:left side horizontal movement}
    #    | Palm rotation{+:clockwise,-:anti-clockwise} |   Elbow movement{+:right to left,-:left to right}  ]
    # these hand movements will only work if rotation are possible in those directions


    # JointNamesH = ["HeadPitch","HeadYaw"] # range ([-1,1],[-0.5,0.5]) // HeadPitch :{(-)up,(+)down} , HeadYaw :{(-)left,(+)right}

    ArmL1 = [-50,  30, 0, -15, 0]
    ArmL1 = [ x * motion.TO_RAD for x in ArmL1]

    # ArmR1 = [-50,  30, 0, 40]
    # ArmR1 = [ x * motion.TO_RAD for x in ArmR1]
    #
    # ArmR2 = [-40,  50, 0, 80]
    # ArmR2 = [ x * motion.TO_RAD for x in ArmR2]

    pFractionMaxSpeed = 0.5

    # HeadA = [0.1,0.3] # dont make more than 0.1 for these combinations as it can bang its head with the arm

    motion_service.angleInterpolationWithSpeed(JointNamesL, ArmL1, pFractionMaxSpeed)
    # motion_service.angleInterpolationWithSpeed(JointNamesR, ArmR1, pFractionMaxSpeed)
    # motion_service.angleInterpolationWithSpeed(JointNamesR, ArmR2, pFractionMaxSpeed)
    # motion_service.angleInterpolationWithSpeed(JointNamesH, HeadA, pFractionMaxSpeed)
    tts.say("Hi there !")

    return


def hello(motion_service, tts):
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
    # motion = ALProxy("ALMotion", robotIp, 9559)
    # motion.setExternalCollisionProtectionEnabled("Arms", False)
    # tts = ALProxy("ALTextToSpeech", robotIp, port)
    # tts.setParameter("speed", 100)
    # tts.setLanguage("English")
    motion_service.angleInterpolation(names, keys, times, True)
    tts.say("Hello, welcome to the 390 Lab Space! Here our team of business people, engineers, and scientists are hard \
    at work bringing the future to you! As we like to say here, if googling was a sport, we'd be in the Olympics!")
    motion_service.setAngles(names2, angles, 0.3)
    return

def main(session):
    """
    Use the goToPosture Method to PoseZero.
    Set all the motors of the body to zero.
    """
    # Get the services ALMotion, ALRobotPosture & ALTextToSpeech.

    motion_service = session.service("ALMotion")
    posture_service = session.service("ALRobotPosture")
    tts = session.service("ALTextToSpeech")

    # Wake up robot
    motion_service.wakeUp()

    posture_service.goToPosture("StandInit", 0.5)
    # userArmArticular(motion_service, tts)
    hello(motion_service, tts)

    print(" --- Over --- ")
    time.sleep(3)
    # Go to rest position
    motion_service.rest()

    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.1.5",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    main(session)
