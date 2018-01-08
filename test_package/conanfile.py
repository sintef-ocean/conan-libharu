from conans import ConanFile, CMake
import os

class LibharuTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch", "os_build", "arch_build"
    generators = "cmake"
    options = {"shared": [True, False]}
    default_options = "shared=False"

    def requirements(self):
        self.options["libharu"].shared = self.options.shared

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        cmake.test()

    def imports(self):
        pass # should be resolved with linking

    def test(self):
        print("SUCCESS")
