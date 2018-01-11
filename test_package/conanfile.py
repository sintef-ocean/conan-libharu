from conans import ConanFile, CMake, tools

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
        if not tools.cross_building(self.settings):
            cmake.test()

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")
        self.copy('*.so*', dst='bin', src='lib')

    def test(self):
        if not tools.cross_building(self.settings):
            print("SUCCESS")
        else:
            print("NOT_RUN (cross-building)");
