from conans import ConanFile, AutoToolsBuildEnvironment, tools, CMake
from distutils.dir_util import copy_tree
import os
import shutil

class HttpParserConan(ConanFile):
    name = "http_parser"
    version = "2.8.0"
    description = "http request/response parser for c"
    homepage = "https://github.com/nodejs/http-parser"
    url = "https://github.com/theirix/conan-http-parser"
    license = "MIT"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    exports = "%s.patch" % name
    exports_sources = "CMakeLists.txt", "cmake/*"
    source_subfolder = "sources"

    def configure(self):
        del self.settings.compiler.libcxx

    def source(self):
        tools.get("https://github.com/nodejs/http-parser/archive/v%s.tar.gz" % self.version)
        os.rename('http-parser-%s' % self.version, self.source_subfolder)
        shutil.copy2("CMakeLists.txt", self.source_subfolder)
        copy_tree("cmake", "%s/cmake" % self.source_subfolder)

    def build(self):
        # tools.patch(patch_file=os.path.join(self.build_folder, 'http-parser.patch'),
        #             base_path=self.name)

        # if self.settings.os == "Linux" or self.settings.os == "Macos":
        #     env_build = AutoToolsBuildEnvironment(self)

        #     target = 'install' if self.options.shared else 'install-static'

        #     with tools.environment_append(env_build.vars):
        #         with tools.chdir(self.name):
        #             cmd = 'make PREFIX=distr CFLAGS_FAST_EXTRA=-Wno-error CFLAGS_DEBUG_EXTRA=-Wno-error %s' % (target)
        #             self.output.warn(cmd)
        #             self.run(cmd)
        # else:
            cmake = CMake(self)
            cmake.configure(source_folder=self.source_subfolder)
            cmake.build()

    def package(self):
        self.copy("license*", dst="licenses", src=self.source_subfolder, ignore_case=True, keep_path=False)
        self.copy("*.h", dst="include", src=self.source_subfolder)
        # if self.options.shared:
        #     if self.settings.os == "Macos":
        #         self.copy(pattern="%s/distr/lib/*.dylib" % self.name, dst="lib", keep_path=False)
        #     else:
        #         self.copy(pattern="%s/distr/lib/*.so*" % self.name, dst="lib", keep_path=False)
        # else:
        #     self.copy(pattern="%s/distr/lib/*.a" % self.name, dst="lib", keep_path=False)
        if self.options.shared:
            self.copy("*http_parser.lib", dst="lib", keep_path=False) # Windows
            self.copy("*http_parser.dll", dst="bin", keep_path=False) # Windows
            self.copy("*http_parser.dll.a", dst="lib", keep_path=False) # Windows MinGW
            self.copy("*http_parser.so", dst="lib", keep_path=False) # Linux
            self.copy("*http_parser.dylib", dst="lib", keep_path=False) # Macos
        else:
            self.copy("*http_parser.lib", dst="lib", keep_path=False) # Windows
            self.copy("*http_parser.a", dst="lib", keep_path=False) # Linux & Windows MinGW
            self.copy("*http_parser.a", dst="lib", keep_path=False) # Macos

    def package_info(self):
        self.cpp_info.libs = ['http_parser']
