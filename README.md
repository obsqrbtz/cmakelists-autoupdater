# CMakeLists Updater

[![PyPI version](https://img.shields.io/pypi/v/cmakelists-updater)](https://pypi.org/project/cmakelists-updater/)
![License](https://img.shields.io/pypi/l/cmakelists-updater)
![Python versions](https://img.shields.io/pypi/pyversions/cmakelists-updater)

CMakeLists Updater detects new or deleted `.h`, `.hpp`, and `.cpp` files and updates `SET(HEADERS)` and `SET(SOURCES)` sections in the `CMakeLists.txt` file. It also supports a global ignore list for files and directories that should not be monitored.

## Installation

Install the package using `pip`:

```bash
pip install cmakelists-updater
```

## Configuration

Create a YAML configuration file (e.g., `config.yaml`) with the following structure:

```yaml
global_ignore_list:
    - build
    - .git
    - .vscode
cmake_files:
  path/to/first/CMakeLists.txt:
    source_dirs:
      - path/to/first/src
      - path/to/first/include
    ignore_list:
      - ignored_dir
      - ignored_file.cpp
  path/to/second/CMakeLists.txt:
    source_dirs:
      - path/to/second/src
      - path/to/second/include
    ignore_list:
      - ignored_dir
      - ignored_file.cpp
```

- **`cmake_files`**: A mapping of CMake files to their respective settings.
- **`source_dirs`**: A list of directories to monitor for source file changes.
- **`ignore_list`**: (Optional) A list of directories or files to exclude from monitoring for each CMake file.
- **`global_ignore_list`**: (Optional) A list of directories or files to exclude from monitoring across all CMake files.

## Usage 

### Terminal

Run the `cmakelists-updater` command, providing the path to your configuration file:

```bash
cmakelists-updater config.yaml
```

### VS Code task

Add `.vscode/tasks.json` file to your project root with the following contents:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Run CMakeLists Updater",
      "type": "shell",
      "command": "cmakelists-updater",
      "args": ["config.yaml"],
      "problemMatcher": [],
      "presentation": {
        "reveal": "silent",
        "panel": "shared",
        "clear": true
      },
      "options": {
        "env": {
          "PYTHONUNBUFFERED": "1"
        }
      },
      "runOptions": {
        "runOn": "folderOpen"
      }
    }
  ]
}
```

### CMake command

Check if cmake-autoupdater is installed and execute it if found:

```cmake
set(AUTO_UPDATER_STARTED FALSE CACHE BOOL "" FORCE)

find_program(CMAKELISTS_UPDATER_EXEC cmakelists-updater)

if(NOT AUTO_UPDATER_STARTED AND CMAKELISTS_UPDATER_EXEC)
  execute_process(
    COMMAND ${CMAKELISTS_UPDATER_EXEC} "config.yaml"
    WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
  )
  set(AUTO_UPDATER_STARTED TRUE CACHE BOOL "" FORCE)
endif()
```

## Example

Assume the following directory structure:

```
project/
--src/
----main.cpp
----utils.cpp
----utils.hpp
--include/
----project.hpp
--CMakeLists.txt
```

In order to get the script working, first make sure that CMakeLists has `HEADERS` and `SOURCES` variables set and are used in `add_executable`/`add_library`:

```cmake
SET(HEADERS
    include/project.hpp
)

SET(SOURCES
    src/utils.hpp
    src/utils.cpp
    src/main.cpp
    ${HEADERS}
)

add_executable(${PROJECT_NAME}
    ${HEADERS}
    ${SOURCES}
    any_external_dep.hpp)
```

Place a `config.yaml` file into the project root. It might look like:

```yaml
cmake_files:
  CMakeLists.txt:
    source_dirs:
      - src
      - include
    ignore_list:
      - build
```

Run the following command from the project root to start monitoring and updating the `CMakeLists.txt`:

```bash
cmakelists-updater config.yaml
```