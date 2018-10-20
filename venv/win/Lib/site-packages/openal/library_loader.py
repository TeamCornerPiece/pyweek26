import ctypes
import os
import sys
import platform

_here = os.path.dirname(__file__)

class ExternalLibraryError(Exception):
    pass

_loaded_libraries = {}

class ExternalLibrary:
    architecture = platform.architecture()[0]
    
    windows_styles = ["{}", "{}.dll", "lib{}.dll", "lib{}_dynamic.dll", "{}_dynamic.dll"]

    other_styles = ["{}.lib", "lib{}.lib", "{}.a", "lib{}.a", "{}.so", "lib{}.so", "{}.la", "lib{}.la"]

    if architecture == "32bit":
        for arch_style in ["32bit", "32" "86", "win32", "x86", "_x86", "_32", "_win32", "_32bit"]:
            for style in ["{}.dll", "lib{}.dll"]:
                windows_styles.append(style.format("{}"+arch_style))
                
    elif architecture == "64bit":
        for arch_style in ["64bit", "64" "86_64", "amd64", "win_amd64", "x86_64", "_x86_64", "_64", "_amd64", "_64bit"]:
            for style in ["{}.dll", "lib{}.dll"]:
                windows_styles.append(style.format("{}"+arch_style))
    
    @staticmethod
    def load(name, paths = None):
        if name in _loaded_libraries:
            return _loaded_libraries[name]
        if sys.platform == "win32":
            lib = ExternalLibrary.load_windows(name, paths)
            _loaded_libraries[name] = lib
            return lib
        else:
            lib = ExternalLibrary.load_other(name, paths)
            _loaded_libraries[name] = lib
            return lib

    @staticmethod
    def load_other(name, paths = None):
        library = ctypes.util.find_library(name)
        if library:
            return ctypes.CDLL(library)

        if paths:
            for path in paths:
                for style in ExternalLibrary.other_styles:
                    candidate = os.path.join(path, style.format(name))
                    if os.path.exists(candidate) and os.path.isfile(candidate):
                        try:
                            return ctypes.CDLL(candidate)
                        except:
                            pass
        else:
            for path in [os.getcwd(), _here]:
                for style in ExternalLibrary.other_styles:
                    candidate = os.path.join(path, style.format(name))
                    if os.path.exists(candidate) and os.path.isfile(candidate):
                        try:
                            return ctypes.CDLL(candidate)
                        except:
                            pass

    @staticmethod
    def load_windows(name, paths = None):
        not_supported = [] # libraries that were found but aren't supported
        for style in ExternalLibrary.windows_styles:
            candidate = style.format(name)
            if not os.path.isfile(candidate):
                continue
            try:
                return ctypes.CDLL(candidate)
            except WindowsError:
                pass
            except OSError:
                not_supported.append(candidate)

        if paths:
            for path in paths:
                for style in ExternalLibrary.windows_styles:
                    candidate = os.path.join(path, style.format(name))
                    if os.path.exists(candidate) and os.path.isfile(candidate):
                        try:
                            return ctypes.CDLL(candidate)
                        except OSError:
                            not_supported.append(candidate)

        else:
            for path in [os.getcwd(), _here]:
                for style in ExternalLibrary.windows_styles:
                    candidate = os.path.join(path, style.format(name))
                    if os.path.exists(candidate) and os.path.isfile(candidate):
                        try:
                            return ctypes.CDLL(candidate)
                        except OSError:
                            not_supported.append(candidate)

        if not_supported:
            raise ExternalLibraryError("library '{}' couldn't be loaded, because the following candidates were not supported:".format(name)
                                 + ("\n{}" * len(not_supported)).format(*not_supported))

        raise ExternalLibraryError("library '{}' couldn't be loaded".format(name))

        

        
