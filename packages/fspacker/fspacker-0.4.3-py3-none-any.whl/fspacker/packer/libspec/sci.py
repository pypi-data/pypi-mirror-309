import logging

from fspacker.common import PackTarget
from fspacker.packer.libspec.base import ChildLibSpecPacker


class MatplotlibSpecPacker(ChildLibSpecPacker):
    PATTERNS = dict(
        matplotlib={
            "matplotlib/",
            "matplotlib.libs/",
            "mpl_toolkits/",
            "pylab.py",
        },
        contourpy=set(),
        cycler=set(),
        importlib_resources=set(),
        numpy=set(),
        packaging=set(),
        pillow=set(),
        pyparsing=set(),
        python_dateutil={
            "^dateutil",
        },
        zipp=set(),
    )

    def pack(self, lib: str, target: PackTarget):
        logging.info("Using [matplotlib] pack spec")
        super().pack(lib, target)


class PillowSpecPacker(ChildLibSpecPacker):
    PATTERNS = dict(
        pillow={"PIL"},
    )


class NumbaSpecPacker(ChildLibSpecPacker):
    PATTERNS = dict(
        numba=set(),
        cffi={"cffi", "_cffi_backend.cp38-win_amd64"},
        importlib_metadata=set(),
        llvmlite=set(),
        pycparser=set(),
    )


class TorchSpecPacker(ChildLibSpecPacker):
    PATTERNS = dict(
        torch={"torch"},
        fsspec=set(),
        filelock=set(),
        jinja2=set(),
        MarkupSafe=set(),
        matplotlib=set(),
        sympy=set(),
        typing_extensions=set(),
    )


class TorchVisionSpecPacker(ChildLibSpecPacker):
    PATTERNS = dict(
        torchvision={"torchvision"},
        torch=set(),
        numpy=set(),
        pillow=set(),
    )
