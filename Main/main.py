import qi
import argparse
import HumanTrackedEventWatcher


class Application:
    def __init__(self):
        print("init")

    def main(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--ip", type=str, default="127.0.0.1",  # default="10.9.45.11",
                            help="Robot IP address. On robot or Local Naoqi: use \
                            '127.0.0.1'.")
        parser.add_argument("--port", type=int, default=9559,
                            help="Naoqi port number")

        args = parser.parse_args()

        # Initialize qi framework.
        connection_url = "tcp://" + args.ip + ":" + str(args.port)
        app = qi.Application(["HumanTrackedEventWatcher",
                              "--qi-url=" + connection_url])

        human_tracked_event_watcher = HumanTrackedEventWatcher(app,args)
        human_tracked_event_watcher.run()


class Gestures:
    def __init(self):
        print("init")




if __name__ == "__main__":
    app = Application ()