import qi
import argparse
import motion
import sys
import time


class HumanTrackedEventWatcher(object):
    """ A class to react to HumanTracked and PeopleLeft events """

    def __init__(self, app):
        """
        Initialisation of qi framework and event detection.
        """
        super(HumanTrackedEventWatcher, self).__init__()

        try:
            app.start()
        except RuntimeError:
            print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " +
                   str(args.port) + ".\n")

            sys.exit(1)

        session = app.session
        self.subscribers_list = []
        self.is_speech_reco_started = True

        # SUBSCRIBING SERVICES
        self.tts             = session.service("ALTextToSpeech")
        self.memory          = session.service("ALMemory")
        self.motion          = session.service("ALMotion")
        self.speech_reco     = session.service("ALSpeechRecognition")
        self.basic_awareness = session.service("ALBasicAwareness")
        self.posture_service = session.service("ALRobotPosture")

    def create_callbacks(self):

        self.connect_callback("ALBasicAwareness/HumanTracked",
                              self.on_human_tracked)
        self.connect_callback("ALBasicAwareness/HumanLost",
                              self.on_people_left)
        return

    def connect_callback(self, event_name, callback_func):
        """ connect a callback for a given event """
        print("Callback connection")

        subscriber = self.memory.subscriber(event_name)
        subscriber.signal.connect(callback_func)
        self.subscribers_list.append(subscriber)

        return

    def on_human_tracked(self, value):
        """ callback for event HumanTracked """
        print ("Got HumanTracked: detected person with ID:", str(value))
        if value >= 0:  # found a new person
            # self.pepper_speak("Ohh I found a new person, let me tag you with id  {}".format(value))
            position_human = self.get_people_perception_data(value)
            [x, y, z] = position_human
            print("The tracked person with ID", value, "is at the position:", \
                "x=", x, "/ y=",  y, "/ z=", z)
            self.wave_hello("Hello, welcome to the J P Morgan Innovation Showcase Space!")


        return

    def on_people_left(self, value):
        """ callback for event PeopleLeft """
        print("Got PeopleLeft: lost person", str(value))
        # self.pepper_speak("Ohh No ! I lost the person")
        print("Oh No! I lost the person")
        self.pepper_speak("Okay,  have a great day!")

    def pepper_speak(self, msg):

        sentence = "\RSPD="+ str( 100 ) + "\ "
        sentence += "\VCT="+ str( 100 ) + "\ "
        sentence += msg
        sentence +=  "\RST\ "
        self.tts.say(str(sentence))

        return

    def get_people_perception_data(self, id_person_tracked):
        """
            return information related to the person who has the id
            "id_person_tracked" from People Perception
        """
        memory_key = "PeoplePerception/Person/" + str(id_person_tracked) + \
                     "/PositionInWorldFrame"
        return self.memory.getData(memory_key)



    def run(self):
        """
            this example uses the setEngagementMode, startAwareness and
            stopAwareness methods
        """
        # start
        print("Waiting for the robot to be in wake up position")
        self.motion.wakeUp()

        self.posture_service.goToPosture("StandInit", 0.5)

        self.create_callbacks()

        print("Starting BasicAwareness with the fully engaged mode")
        self.basic_awareness.setEngagementMode("FullyEngaged")
        self.basic_awareness.setEnabled(True)

        # loop on, wait for events until manual interruption
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Interrupted by user, shutting down")
            # stop
            print("Stopping BasicAwareness")
            self.basic_awareness.setEnabled(False)

            print("Waiting for the robot to be in rest position")
            self.motion.rest()

            sys.exit(0)

        return

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default ="127.0.0.1",  #default="10.9.45.11",
                        help="Robot IP address. On robot or Local Naoqi: use \
                        '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()

    # Initialize qi framework.
    connection_url = "tcp://" + args.ip + ":" + str(args.port)
    app = qi.Application(["HumanTrackedEventWatcher",
                          "--qi-url=" + connection_url])

    human_tracked_event_watcher = HumanTrackedEventWatcher(app)
    human_tracked_event_watcher.run()
