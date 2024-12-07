import hashlib
import json
import logging
import pathlib
import shutil
import time
import typing
from urllib.request import urlopen

from fspacker.common import PackTarget
from fspacker.config import EMBED_FILE_NAME, EMBED_FILEPATH, PYTHON_VER, EMBED_URL_PREFIX
from fspacker.packer.base import BasePacker
from fspacker.utils.url import get_fastest_url


def _calc_checksum(filepath: pathlib.Path, block_size=4096) -> str:
    """Calculate checksum of filepath, using md5 algorithm.

    Args:
        filepath (pathlib.Path): input filepath.
        block_size (int, optional): read block size, default by 4096.
    """

    hasher = hashlib.md5()
    logging.info(f"Calculate checksum for: [{filepath.name}]")
    with open(filepath, "rb") as file:
        for chunk in iter(lambda: file.read(block_size), b""):
            hasher.update(chunk)
    logging.info(f"Checksum is: [{hasher.hexdigest()}]")
    return hasher.hexdigest()


def _get_json_value(filepath: pathlib.Path, key: str) -> typing.Any:
    with open(filepath) as f:
        data = json.load(f)
        return data.setdefault(key, None)


def _update_json_values(filepath: pathlib.Path, updates: typing.Dict[str, typing.Any]):
    """Update [key, value] in json file

    Args:
        filepath (pathlib.Path): Input file
        updates (typing.Dict[str, typing.Any]): update values
    """
    if filepath.exists():
        with open(filepath) as fr:
            data = json.load(fr)
    else:
        data = {}

    for key, value in updates.items():
        data[key] = value

    with open(filepath, "w") as fw:
        json.dump(data, fw, indent=4, ensure_ascii=False)


class RuntimePacker(BasePacker):
    def pack(self, target: PackTarget):
        dest = target.runtime_dir
        if (dest / "python.exe").exists():
            logging.info("Runtime folder exists, skip")
            return

        self.fetch_runtime()
        logging.info(f"Unpack runtime zip file: [{EMBED_FILEPATH.name}]->[{dest.relative_to(target.root_dir)}]")
        shutil.unpack_archive(EMBED_FILEPATH, dest, "zip")

    @staticmethod
    def fetch_runtime():
        """Fetch runtime zip file"""
        from fspacker.config import CONFIG_FILEPATH as CFG
        from fspacker.config import EMBED_FILEPATH as EMBED
        from fspacker.config import EMBED_REPO_DIR

        if not EMBED_REPO_DIR.exists():
            EMBED_REPO_DIR.mkdir(parents=True)

        if EMBED.exists():
            logging.info(f"Compare file [{EMBED.name}] with local config [{CFG.name}] checksum")
            src_checksum = _get_json_value(CFG, "embed_file_checksum")
            dst_checksum = _calc_checksum(EMBED)
            if src_checksum == dst_checksum:
                logging.info("Checksum matches!")
                return

        logging.info("Fetch fastest embed python url")
        fastest_url = get_fastest_url(EMBED_URL_PREFIX)
        archive_url = f"{fastest_url}{PYTHON_VER}/{EMBED_FILE_NAME}"
        with urlopen(archive_url) as url:
            runtime_files = url.read()

        logging.info(f"Download embed runtime from [{fastest_url}]")
        t0 = time.perf_counter()
        with open(EMBED, "wb") as f:
            f.write(runtime_files)
        logging.info(f"Download finished, total used: [{time.perf_counter() - t0:.2f}]s.")

        checksum = _calc_checksum(EMBED)
        logging.info(f"Write checksum [{checksum}] into config file [{CFG}]")
        _update_json_values(CFG, dict(embed_file_checksum=checksum))
