import os
import re
import sys
import time
from enum import Enum
from os import walk
from shutil import copyfile, rmtree
from sys import exit

from watchdog.events import RegexMatchingEventHandler


class EventType(Enum):
    ON_CREATED = 'ON_CREATED'
    ON_MODIFIED = 'ON_MODIFIED'
    ON_MOVED = 'ON_MOVED'
    ON_DELETED = 'ON_DELETED'


class FileEventHandler(RegexMatchingEventHandler):

    def __init__(self, regex, sub_folders, buffer_time):
        self.__regex = regex
        self.__sub_folders = sub_folders
        self.__time = time.time()
        self.__first_run = True
        self.__slash = "\\" if sys.platform == 'win32' else '/'
        self.__buffer_time = buffer_time
        super().__init__(self.__regex)

    def on_created(self, event):
        self.process(event, EventType.ON_CREATED)

    def on_modified(self, event):
        self.process(event, EventType.ON_MODIFIED)

    def on_moved(self, event):
        self.process(event, EventType.ON_MOVED)

    def on_deleted(self, event):
        self.process(event, EventType.ON_DELETED)

    def check_time(self):
        if time.time() - self.__time >= self.__buffer_time:
            self.__time = time.time()
            return True
        else:
            return False

    def copy_files(self, event, current_folder, pre, post, moved = False):
        if self.check_time() or self.__first_run or moved:
            self.__first_run = False
            for sub_folder in self.__sub_folders:
                if sub_folder != current_folder:
                    new_file = os.path.join(pre, sub_folder, post)
                    folder = f'{self.__slash}'.join(new_file.split(self.__slash)[:-1])
                    try:
                        os.makedirs(folder)
                    except FileExistsError:
                        pass

                    try:
                        path = event.dest_path if moved else event.src_path
                        print('COPY FILE: ' + path + ' -> ' + new_file)
                        copyfile(path, new_file)
                    except IOError as e:
                        print("Unable to copy file. %s" % e)
                        exit(1)
                    except:
                        print("Unexpected error:", sys.exc_info())
                        exit(1)

    def delete_files(self, event, current_source_folder, pre, post):
        if self.check_time() or self.__first_run:
            self.__first_run = False
            for sub_folder in self.__sub_folders:
                new_file = os.path.join(pre, sub_folder, post)
                if sub_folder != current_source_folder:
                    folder = f'{self.__slash}'.join(new_file.split(self.__slash)[:-1])

                    try:
                        print('DELETE FILE: ' + event.src_path + ' -> ' + new_file)
                        os.remove(new_file)
                    except OSError as e:
                        print("Error: %s - %s." % (e.filename, e.strerror))

                    filenames = next(walk(folder), (None, None, []))[2]
                    print(filenames)
                    if not filenames:
                        try:
                            rmtree(folder)
                        except (Exception,) as err:
                            print('cannot delete folder: ', folder, err)
                            pass

    def find_index(self, split_path):
        if split_path:
            for part in split_path:
                for folder in self.__sub_folders:
                    if part == folder:
                        return split_path.index(part)

    def process(self, event, event_type):
        source_file_split = event.src_path.split(self.__slash)

        filename, ext = os.path.splitext(event.src_path)
        source_index = self.find_index(source_file_split)
        current_source_folder = source_file_split[source_index]

        pre = f'{self.__slash}'.join(source_file_split[:source_index])
        post = f'{self.__slash}'.join(source_file_split[source_index + 1:])

        if ext[-1] != '~':
            match event_type:
                case EventType.ON_CREATED:
                    print('1. ON_CREATED', event.src_path)
                    self.copy_files(event, current_source_folder, pre, post)
                case EventType.ON_MODIFIED:
                    print('2. ON_MODIFIED', event.src_path)
                    self.copy_files(event, current_source_folder, pre, post)

                case EventType.ON_MOVED:
                    pattern = re.compile(self.__regex[0])
                    dest_file_split = event.dest_path.split(self.__slash)
                    dest_matched = pattern.match(event.dest_path)
                    source_matched = pattern.match(event.src_path)
                    dest_index = self.find_index(dest_file_split)
                    current_dest_folder = dest_file_split[source_index]
                    dest_pre = f'{self.__slash}'.join(dest_file_split[:dest_index])
                    dest_post = f'{self.__slash}'.join(dest_file_split[dest_index + 1:])

                    print('3. ON_MOVED', event.src_path, event.dest_path)
                    if source_matched:
                        self.delete_files(event, current_source_folder, pre, post)
                    if dest_matched:
                        self.copy_files(event, current_dest_folder, dest_pre, dest_post, True)

                    print('source_matched', source_matched)
                    print('dest_matched', dest_matched)
                    pass
                case EventType.ON_DELETED:
                    print('4. ON_DELETED', event.src_path)
                    self.delete_files(event, current_source_folder, pre, post)
