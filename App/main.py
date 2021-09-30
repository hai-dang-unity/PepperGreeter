import argparse
import datetime
import sys
import time
import qi

from basic_awareness import HumanTrackedEventWatcher

from opendomain_responder import basic_qa

TOPIC_NAME = "face_detect_greeter.top"

class PepperChatBot(object):

    def __init__(self, app, human_tracked_event_watcher):
        super(PepperChatBot, self).__init__()
        try:
            app.start()
        except RuntimeError:
            print("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " +
                  str(args.port) + ".\n")

            sys.exit(1)

        session = app.session
        self.subscribers_list = []

        # SUBSCRIBING SERVICES
        self.memory_service = session.service("ALMemory")
        self.motion_service = session.service("ALMotion")
        self.posture_service = session.service("ALRobotPosture")
        self.video_service = session.service("ALVideoDevice")
        self.tts = session.service("ALTextToSpeech")
        self.speaking_movement = session.service("ALSpeakingMovement")
        self.dialog_service = session.service("ALDialog")
        # self.tablet_service = session.service("ALTabletService")
        self.human_watcher = human_tracked_event_watcher

    def create_callbacks(self):

        self.connect_callback("developer_name_event",
                              self.developer_name_event)

        # self.connect_callback("Dialog/LastInput",
        #                       self.last_dialog_event)

        self.connect_callback("unknown_input_event",
                              self.who_question_event)

        self.connect_callback("specific_question_event",
                              self.specific_question_event)

        # self.tablet_service.onInputText.connect(self.got_button_event)

        return

    def connect_callback(self, event_name, callback_func):
        print("Callback connection")
        subscriber = self.memory_service.subscriber(event_name)
        subscriber.signal.connect(callback_func)
        self.subscribers_list.append(subscriber)

        return

    def _makePepperSpeak(self, userMsg):
        # MAKING PEPPER SPEAK
        # future = self.animation_player_service.run("animations/Stand/Gestures/Give_3", _async=True)
        sentence = "\RSPD=" + str(100) + "\ "  # Speed
        sentence += "\VCT=" + str(100) + "\ "  # Voice Shaping
        sentence += userMsg
        sentence += "\RST\ "
        self.tts.say(str(sentence))
        # future.value()

    def got_button_event(self, buttonId, value):
        if buttonId == 1:
            self.userName = value
            if value == '':
                self.userName = "NULL"
        if buttonId == 0:  # Cancel is pressed
            self.userName = "NULL"
        # self._clearTablet()
        return

    # def _clearTablet(self):
    #     # Hide the web view
    #     self.tablet_service.hideImage()
    #     self.tablet_service.hideDialog()
    #
    #     return

    def developer_name_event(self, value):
        # setting Memory Variable
        self.memory_service.insertData("developerName", "sky net")
        return

    def who_question_event(self, value):
        print("Question : ", value)
        # ans = basic_qa.answerQues(value)
        # if ans:
        #     print("Answer : ", ans)
        #     self._makePepperSpeak(ans)
        self._makePepperSpeak("I did not get that")
        return

    def specific_question_event(self, value):
        print("Value : ", value)
        msg = ''
        if value == 'TIME':
            msg = "Present time is " + time.ctime().split()[3]

        if value == 'DAY':
            msg = "The day today is " + datetime.datetime.today().strftime('%A')

        if value == 'DATE':
            msg = "The date today is " + datetime.datetime.today().strftime('%D')

        if value == 'MONTH':
            msg = "The present month is " + datetime.datetime.today().strftime('%B')

        if value == 'YEAR':
            msg = "The present year is " + time.ctime().split()[4]

        if msg:
            self._makePepperSpeak(msg)

        return

    def _addTopic(self):
        print("Starting topic adding process")

        # Controlling hand gestures and movement while speaking
        self.speaking_movement.setEnabled(True)

        self.dialog_service.setLanguage("English")
        # Loading the topic given by the user (absolute path is required)

        topic_path = "/home/nao/chat/{}".format(TOPIC_NAME)

        topf_path = topic_path.decode('utf-8')
        self.topic_name = self.dialog_service.loadTopic(
            topf_path.encode('utf-8'))

        # Activating the loaded topic
        self.dialog_service.activateTopic(self.topic_name)

        # Starting the dialog engine - we need to type an arbitrary string as the identifier
        # We subscribe only ONCE, regardless of the number of topics we have activated
        self.dialog_service.subscribe('face_detector_example')

        print("\nSpeak to the robot using rules. Robot is ready")

        return

    def _cleanUp(self):
        print("Starting Clean Up process")
        self.human_watcher.stop_basic_awareness()

        # Stopping any movement if there
        self.motion_service.stopMove()
        # stopping the dialog engine
        self.dialog_service.unsubscribe('face_detector_example')
        # Deactivating the topic
        self.dialog_service.deactivateTopic(self.topic_name)

        # now that the dialog engine is stopped and there are no more activated topics,
        # we can unload our topic and free the associated memory
        self.dialog_service.unloadTopic(self.topic_name)

        # self._clearTablet()
        self.posture_service.goToPosture("StandInit", 0.1)

        return

    def run(self):
        # start
        print("Waiting for the robot to be in wake up position")
        self.motion_service.wakeUp()
        self.posture_service.goToPosture("StandInit", 0.1)
        time.sleep(1)

        self.create_callbacks()
        self._addTopic()

        self.human_watcher.start_basic_awareness()

        try:
            # self.startGreeterProgram()
            print("Starting pepper program chat bot app")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Interrupted by user, shutting down")
            self._cleanUp()
            print("Waiting for the robot to be in rest position")
            self.motion_service.rest()
            sys.exit(0)

        return


# class Gestures:
#     def __init(self):
#         print("init")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",  # default="10.9.45.11",
                        help="Robot IP address. On robot or Local Naoqi: use \
                            '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()

    # Initialize qi framework.
    connection_url = "tcp://" + args.ip + ":" + str(args.port)
    app = qi.Application(["PepperChatBot",
                          "--qi-url=" + connection_url])

    human_tracked_event_watcher = HumanTrackedEventWatcher(app)
    event_watcher = PepperChatBot(app, human_tracked_event_watcher)
    event_watcher.run()
