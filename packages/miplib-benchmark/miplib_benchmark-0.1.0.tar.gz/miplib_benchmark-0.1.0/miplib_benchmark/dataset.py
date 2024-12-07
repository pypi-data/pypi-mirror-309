# https://miplib.zib.de/downloads/benchmark.zip

import requests
import pathlib
from tqdm import tqdm
import zipfile
import os
from .logger import logger

def get_miplib_benchmark_dir():
    path_from_env = os.getenv("MIPLIB_BENCHMARK_DIR", None)
    if path_from_env is None:
        path = pathlib.Path.home() / ".miplib_benchmark"
    else:
        path = pathlib.Path(path_from_env)
    path.mkdir(parents=True, exist_ok=True)
    return path

def get_mps_files_dir():
    path = get_miplib_benchmark_dir() / "mps_files"
    path.mkdir(parents=True, exist_ok=True)
    return path

def get_zip_path():
    return get_miplib_benchmark_dir() / "benchmark.zip"

def download_if_not_exists():
    if not get_zip_path().exists():
        download_zip()
    else:
        logger.info(f"Zip file already exists at {get_zip_path()}")

def download_zip():
    url = "https://miplib.zib.de/downloads/benchmark.zip"
    logger.info(f"Downloading from {url} to {get_zip_path()}")
    
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(get_zip_path(), 'wb') as file, \
         tqdm(
            desc="Downloading",
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as progress_bar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            progress_bar.update(size)

    logger.info(f"Downloaded to {get_zip_path()}")


def unzip_if_empty():
    if len(list(get_mps_files_dir().iterdir())) == 0:
        unzip()
    else:
        logger.info(f"MPS files already unzipped at {get_mps_files_dir()}")

    # count the number of files in the directory
    num_files = len(list(get_mps_files_dir().iterdir()))
    logger.info(f"Found {num_files} MPS files in {get_mps_files_dir()}")

def unzip():
    logger.info(f"Unzipping {get_zip_path()} to {get_mps_files_dir()}")
    with zipfile.ZipFile(get_zip_path(), 'r') as zip_ref:
        zip_ref.extractall(get_mps_files_dir())
    logger.info(f"Unzipped to {get_mps_files_dir()}")

def get_all_mps_files_paths() -> list[pathlib.Path]:
    # Get both .mps and .mps.gz files
    mps_files = list(get_mps_files_dir().glob("*.mps"))
    mps_gz_files = list(get_mps_files_dir().glob("*.mps.gz"))
    return mps_files + mps_gz_files


def download_and_unzip():
    download_if_not_exists()
    unzip_if_empty()
