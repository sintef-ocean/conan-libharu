cmake_minimum_required(VERSION 3.13)
project(LibharuTest C)

include(CTest)
include(${CMAKE_BINARY_DIR}/conan_paths.cmake)

find_package(libharu MODULE REQUIRED)

add_executable(png-libharu test.c)
target_link_libraries(png-libharu libharu::libharu)

file(COPY ${CMAKE_CURRENT_SOURCE_DIR}/basn3p04.png DESTINATION ${CMAKE_CURRENT_BINARY_DIR}/bin)

enable_testing()
add_test(NAME test-libharu
  WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/bin
  COMMAND png-libharu)
