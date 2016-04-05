import sys
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from libraries import params        # General parameters
from libraries import process       # Process library: specific of the project

class MyHandler(PatternMatchingEventHandler):
    patterns = params.patterns      # Pass the string with the user defined number image through a parameters file

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
            print("The raw file has been deleted: ")
            process.deleted(str(event.src_path))
        elif event.event_type == 'created':
            print("New data: ")
            process.created(str(event.src_path))
        else:
            print("What fuck is happening?!")

    def on_deleted(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)

def FWatch(checkPath):
    observer = Observer()
    observer.schedule(MyHandler(), path=checkPath)
    observer.start()

    print("Osservo!")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
