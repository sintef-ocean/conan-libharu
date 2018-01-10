from conans import ConanFile, CMake, tools
import svn.remote


class LibharuConan(ConanFile):
    name = "libharu"
    version = "2.3.0"
    license = "MIT"
    url = "https://github.com/joakimono/conan-libharu"
    homepage = "http://libharu.org"
    author = "Joakim Haugen (joakim.haugen@gmail.com)"
    description = "libHaru is a free, cross platform, open source library for generating PDF files."
    settings = "os", "compiler", "build_type", "arch", "os_build", "arch_build"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    requires = "zlib/[>=1.2.11]@conan/stable", "libpng/[>=1.6.34]@bincrafters/stable"

    def requirements(self):
        self.options["zlib"].shared = self.options.shared
        self.options["libpng"].shared = self.options.shared
  
    def source(self):

        self.run("git clone --depth 1 -b RELEASE_2_3_0 https://github.com/libharu/libharu.git")
        
        lic = svn.remote.RemoteClient("https://github.com/libharu/libharu/trunk")
        lic_text = lic.cat("LICENCE")
        tools.save("LICENSE", lic_text)
        
        tools.replace_in_file("libharu/CMakeLists.txt", "project(libharu C)",
                              '''project(libharu C)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')
        tools.replace_in_file("libharu/CMakeLists.txt",
                              "cmake_minimum_required(VERSION 2.4.8 FATAL_ERROR)",
                              "cmake_minimum_required(VERSION 3.1.2)")
        tools.replace_in_file("libharu/CMakeLists.txt",
                              "set(LIBHPDF_MINOR 2)", "set(LIBHPDF_MINOR 3)")

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="libharu",
                        defs = {"LIBHPDF_SHARED": self.options.shared, "LIBHPDF_STATIC": not self.options.shared})
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("LICENSE", dst="licenses", src=self.source_folder,
                  ignore_case=True, keep_path=False)

    def package_info(self):
        if self.settings.os == "Windows":
            self.cpp_info.libs = ['libhpdf']
        else:
            self.cpp_info.libs = ['hpdf']
        if not self.options.shared:
            self.cpp_info.libs[0] += 's'
        if self.settings.os == "Windows":
            if self.settings.build_type == "Debug":
                self.cpp_info.libs[0] += 'd'

    def configure(self):
        del self.settings.compiler.libcxx
