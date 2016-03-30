import sys
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

class MyHandler(PatternMatchingEventHandler):
    patterns=["*.ppm"]         # Pass the string with the user defined number image

    def process(self, event):
        """
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """

        print(str(event.src_path) + ' ' + str(event.event_type))

        if event.event_type == 'deleted':
            print("The raw file has been deleted: Ready!")
        elif event.event_type == 'created':
            print("New data: Processing!")
            # do something
        else:
            print("What fuck is happening?!")

    def on_deleted(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)

if __name__ == '__main__':
    args = sys.argv[1:]
    observer = Observer()
    observer.schedule(MyHandler(), path=args[0] if args else '.')
    observer.start()

    print("Osservo!")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
