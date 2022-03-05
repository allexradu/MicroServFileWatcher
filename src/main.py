import sys
import time

from watchdog.observers import Observer

from events import FileEventHandler


class FileWatcher:
    def __init__(self, file_src_path, regex, sub_folders, buffer_time):
        self.__src_path = file_src_path
        self.__event_handler = FileEventHandler(regex, sub_folders, buffer_time)
        self.__event_observer = Observer()

    def run(self, ):
        self.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def start(self):
        self.__schedule()
        self.__event_observer.start()

    def stop(self):
        self.__event_observer.stop()
        self.__event_observer.join()

    def __schedule(self):
        self.__event_observer.schedule(
            self.__event_handler,
            self.__src_path,
            recursive = True
        )


if __name__ == "__main__":

    def execute():
        BUFFER_TIME = 10
        if len(sys.argv) < 5 or len(sys.argv) > 5:
            return print(f"Error: Run MicroSRV FileWatcher with 3 arguments. Current arguments: {len(sys.argv) - 1}")
        common_folder = sys.argv[1]
        print('Common Folder:', common_folder)
        file_extensions = sys.argv[2].split('|')
        print('File Extensions:', file_extensions)
        sub_folders = sys.argv[3].split('|')
        print('Sub folders:', sub_folders)

        regex_extensions = []
        for ext in file_extensions:
            reg = f"({'|'.join(sub_folders)})" + r"\/" + common_folder + r"\/.*\." + ext
            regex_extensions.append(reg)
        reg_string = r".*(" + "|".join(regex_extensions) + r")"
        REGEX = [reg_string]
        print('RegEx:', REGEX)

        src_path = sys.argv[4] if len(sys.argv) > 1 else '.'
        print('Watch Path:', src_path)
        inp = input('Press y if configurations are okay: ')
        if inp.strip().lower() == 'y':
            FileWatcher(src_path, REGEX, sub_folders, BUFFER_TIME).run()
        else:
            return print('Try again.')


    execute()
