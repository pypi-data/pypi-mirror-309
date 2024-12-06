### windows-only: [


# start delvewheel patch
def _delvewheel_patch_1_9_0():
    import os
    if os.path.isdir(libs_dir := os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'meshlib.libs'))):
        os.add_dll_directory(libs_dir)


_delvewheel_patch_1_9_0()
del _delvewheel_patch_1_9_0
# end delvewheel patch

# Fixes DLL loading paths.

def _init_patch():
    import os
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    os.add_dll_directory(libs_dir)

_init_patch()
del _init_patch

### ]


### wheel-only: [

def _override_resources_dir():
    """
    override resources directory to the package's dir
    """
    import pathlib
    from . import mrmeshpy as mr

    mr.SystemPath.overrideDirectory(mr.SystemPath.Directory.Resources, pathlib.Path(__file__).parent.resolve())
    mr.SystemPath.overrideDirectory(mr.SystemPath.Directory.Fonts, pathlib.Path(__file__).parent.resolve())

_override_resources_dir()
del _override_resources_dir

### ]
