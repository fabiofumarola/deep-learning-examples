from urllib.request import urlretrieve
from os.path import isfile, isdir
from tqdm import tqdm
import zipfile

class DLProgress(tqdm):
    last_block = 0

    def hook(self, block_num=1, block_size=1, total_size=None):
        self.total = total_size
        self.update((block_num - self.last_block) * block_size)
        self.last_block = block_num


def download_zip_file(remote_path, remote_filename, dest_folder_path):
    dest_name = remote_filename.split(".")[0]

    if not isfile(remote_filename):
        with DLProgress(unit='B', unit_scale=True, miniters=1, desc = dest_name) as pbar:
            urlretrieve(
                "{}/{}".format(remote_path, remote_filename),
                filename=remote_filename,
                reporthook=pbar.hook)

    if not isdir(dest_folder_path):
        with zipfile.ZipFile(remote_filename) as zip_ref:
            zip_ref.extractall(dest_folder_path)

    return "{}/{}".format(dest_folder_path, dest_name)
