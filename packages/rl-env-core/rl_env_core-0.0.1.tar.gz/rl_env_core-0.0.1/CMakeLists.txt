cmake_minimum_required(VERSION 3.4...3.18)
project(core LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)

include(CheckCXXSourceCompiles)
check_cxx_source_compiles("
  #include <format>
  int main() { return 0; }
" HAS_FORMAT)
if(NOT HAS_FORMAT)
  message(FATAL_ERROR "Your compiler does not support <format>. Please update your compiler.")
endif()

set(PYBIND11_FINDPYTHON ON)
add_subdirectory(pybind11)
pybind11_add_module(core src/main.cpp)

# EXAMPLE_VERSION_INFO is defined by setup.py and passed into the C++ code as a
# define (VERSION_INFO) here.
target_compile_definitions(core
                           PRIVATE VERSION_INFO=${EXAMPLE_VERSION_INFO})

target_include_directories(core PRIVATE glm)

if(MSVC)
  target_compile_options(core PRIVATE /W4)
else()
  target_compile_options(core PRIVATE -Wall -Wextra -Wpedantic)
endif()
