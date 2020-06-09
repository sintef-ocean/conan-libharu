#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools

class LibharuConan(ConanFile):
    name = "libharu"
    version = "2.3.0"
    license = "zlib-acknowledgement"
    url = "https://github.com/joakimono/conan-libharu"
    homepage = "http://libharu.org"
    author = "Joakim Haugen (joakim.haugen@gmail.com)"
    description = "libHaru is a free, cross platform, open source library for generating PDF files."
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = ("cmake_paths", "cmake_find_package")
    requires = ("zlib/[>=1.2.11]@conan/stable", "libpng/[>=1.6.34]@bincrafters/stable")
    exports = ["lib_license/LICENSE", "Findlibharu.cmake"]
    source_subfolder = "libharu"
    build_subfolder = "build_subfolder"

    def requirements(self):
        self.options["zlib"].shared = False
        self.options["libpng"].shared = False

    def source(self):
        self.run("git clone --depth 1 -b RELEASE_2_3_0 https://github.com/libharu/libharu.git")

        tools.replace_in_file("{}/CMakeLists.txt".format(self.source_subfolder),
                              "project(libharu C)",
                              '''cmake_minimum_required(VERSION 3.13)
                              project(libharu C)
                              include(${CMAKE_BINARY_DIR}/../conan_paths.cmake)''')
        tools.replace_in_file("{}/CMakeLists.txt".format(self.source_subfolder),
                              "cmake_minimum_required(VERSION 2.4.8 FATAL_ERROR)",
                              '''set(CMAKE_POSITION_INDEPENDENT_CODE TRUE)''')
        tools.replace_in_file("{}/CMakeLists.txt".format(self.source_subfolder),
                              "set(LIBHPDF_SHARED ON)",
                              '''set(LIBHPDF_SHARED ON)
                                set(LIBHPDF_STATIC OFF)
                              else(BUILD_SHARED_LIBS)
                                set(LIBHPDF_SHARED OFF)
                                set(LIBHPDF_STATIC ON)''')
        tools.replace_in_file("{}/CMakeLists.txt".format(self.source_subfolder),
                              "set(LIBHPDF_MINOR 2)", "set(LIBHPDF_MINOR 3)")
        tools.replace_in_file("{}/CMakeLists.txt".format(self.source_subfolder),
                              "set(CMAKE_MODULE_PATH",
                              "set(CMAKE_MODULE_PATH ${CONAN_LIBPNG_ROOT}")

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder=self.source_subfolder, build_folder=self.build_subfolder)
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("lib_license/LICENSE", dst="licenses", src=self.source_folder,
                  ignore_case=True, keep_path=False)
        self.copy("Findlibharu.cmake", dst=".", src=self.source_folder, keep_path=False)

    def package_info(self):
        if self.settings.compiler == "Visual Studio":
            self.cpp_info.libs = ['libhpdf']
        else:
            self.cpp_info.libs = ['hpdf']
        if not self.options.shared:
            self.cpp_info.libs[0] += 's'
        if self.settings.compiler == "Visual Studio":
            if self.settings.build_type == "Debug":
                self.cpp_info.libs[0] += 'd'
            if self.options.shared:
                self.cpp_info.defines = ["HPDF_DLL"] # mingw/cygwin also?

    def configure(self):
        del self.settings.compiler.libcxx
