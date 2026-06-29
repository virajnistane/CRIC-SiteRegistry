cmake_minimum_required(VERSION 3.18)
project(site_scorer LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# --------------------------------------------------------------------------
# Find Python interpreter and development headers.
# Uses the same Python that uv is managing.
# --------------------------------------------------------------------------
find_package(Python REQUIRED COMPONENTS Interpreter Development)

# --------------------------------------------------------------------------
# Find pybind11.
# The Python package exposes a CMake config at its own site-packages path.
# We ask Python itself for that path so CMake always finds the right one.
# --------------------------------------------------------------------------
execute_process(
    COMMAND "${Python_EXECUTABLE}" -c
            "import pybind11; print(pybind11.get_cmake_dir())"
    OUTPUT_VARIABLE PYBIND11_CMAKE_DIR
    OUTPUT_STRIP_TRAILING_WHITESPACE
    RESULT_VARIABLE PYBIND11_FOUND_RESULT
)

if(NOT PYBIND11_FOUND_RESULT EQUAL 0)
    message(FATAL_ERROR
        "Could not find pybind11 cmake directory.\n"
        "Run: uv add --group cpp pybind11")
endif()

list(APPEND CMAKE_PREFIX_PATH "${PYBIND11_CMAKE_DIR}")
find_package(pybind11 REQUIRED)

# --------------------------------------------------------------------------
# The extension module
# --------------------------------------------------------------------------
pybind11_add_module(site_scorer site_scorer.cpp)

target_compile_options(site_scorer PRIVATE -O2 -Wall -Wextra)

# --------------------------------------------------------------------------
# Install the .so next to desktop/ so Python can import it without PYTHONPATH
# --------------------------------------------------------------------------
install(
    TARGETS site_scorer
    LIBRARY DESTINATION "${CMAKE_SOURCE_DIR}"
)