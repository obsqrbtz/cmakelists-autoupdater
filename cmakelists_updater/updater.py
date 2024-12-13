import os
import sys
import time
import yaml
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class CMakeListsUpdater(FileSystemEventHandler):
    def __init__(self, source_dirs, cmake_file, ignore_list=None, global_ignore_list=None):
        self.source_dirs = source_dirs
        self.cmake_file = cmake_file
        self.ignore_list = ignore_list if ignore_list else []
        self.global_ignore_list = global_ignore_list if global_ignore_list else []
        self.update_cmakelists()

    def update_cmakelists(self):
        headers = []
        sources = []

        for directory in self.source_dirs:
            for root, dirs, files in os.walk(directory):
                for dir in dirs:
                    if dir in self.ignore_list + self.global_ignore_list:
                        dirs.remove(dir)
                for file in files:
                    if any(ignored in os.path.relpath(os.path.join(root, file), start=os.path.dirname(self.cmake_file)) for ignored in self.ignore_list + self.global_ignore_list):
                        continue

                    if file.endswith(('.h', '.hpp')):
                        headers.append(os.path.relpath(os.path.join(root, file), start=os.path.dirname(self.cmake_file)))
                    elif file.endswith('.cpp'):
                        sources.append(os.path.relpath(os.path.join(root, file), start=os.path.dirname(self.cmake_file)))

        headers_section = "SET(HEADERS\n" + "\n".join(f"    {header.replace(os.sep, '/')}" for header in headers) + "\n)\n"
        sources_section = "SET(SOURCES\n" + "\n".join(f"    {source.replace(os.sep, '/')}" for source in sources) + "\n    ${HEADERS}\n)\n"

        with open(self.cmake_file, 'r') as file:
            content = file.readlines()

        new_content = []
        skip = False
        for line in content:
            if line.upper().startswith("SET(HEADERS"):
                new_content.append(headers_section)
                skip = True
            elif line.upper().startswith("SET(SOURCES"):
                new_content.append(sources_section) 
                skip = True
            elif skip:
                if line.endswith(")\n"):
                    skip = False
            else:
                new_content.append(line)

        with open(self.cmake_file, 'w') as file:
            file.writelines(new_content)

        print(f"CMakeLists.txt updated: {self.cmake_file}")
    
    def on_created(self, event):
        if not event.is_directory and not any(ignored in event.src_path for ignored in self.ignore_list + self.global_ignore_list):
            self.update_cmakelists()
    
    def on_deleted(self, event):
        if not event.is_directory and not any(ignored in event.src_path for ignored in self.ignore_list + self.global_ignore_list):
            self.update_cmakelists()

def main():
    if len(sys.argv) < 2:
        print("Usage: cmakelists_updater <config_file>")
        sys.exit(1)

    config_file = sys.argv[1]

    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)

    global_ignore_list = config.get('global_ignore_list', [])

    observer = Observer()

    for cmake_file, settings in config.get('cmake_files', {}).items():
        source_dirs = [os.path.abspath(dir) for dir in settings.get('source_dirs', [])]
        ignore_list = settings.get('ignore_list', [])

        event_handler = CMakeListsUpdater(source_dirs, cmake_file, ignore_list, global_ignore_list)
        
        for directory in source_dirs:
            observer.schedule(event_handler, directory, recursive=True)

    observer.start()
    
    print("Monitoring for changes in:\n" + "\n".join(f"- {os.path.abspath(cmake_file)}" for cmake_file in config.get('cmake_files', {}).keys()))

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()