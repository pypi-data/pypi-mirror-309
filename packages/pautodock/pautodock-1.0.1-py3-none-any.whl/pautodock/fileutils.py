#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fileutils.py

This file is part of PAutoDock.
Copyright (C) 2020 Giuseppe Marco Randazzo <gmrandazzo@gmail.com>
PAutoDock is distributed under GPLv3 license.
To know more in detail how the license work,
please read the file "LICENSE" or
go to "http://www.gnu.org/licenses/gpl-3.0.en.html"

Provides the basic operation for molecular files.

"""
import logging
import platform
import tarfile
from pathlib import Path

import requests


def get_bin_path(bin_name: str):
    """
    Get the path to the bin_name executable based on the operating system.
    """
    paths = {"Linux": ["/usr/bin/", "/usr/local/bin"], "Darwin": ["/opt/homebrew/bin/"]}
    system = platform.system()
    if system not in paths:
        raise ValueError("Platform not supported")

    for bin_path in paths.get(system):
        if bin_path and Path(f"{bin_path}/{bin_name}").exists():
            return bin_path
    raise ValueError(f"Unable to find {bin_name} installed.")


def download_file(url, destination):
    """
    Download a file from a URL to a local destination.
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(destination, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        logging.info(f"Downloaded: {destination}")
    except requests.RequestException as err:
        logging.error(f"Failed to download file: {err}")
        return False
    return True


def extract_tar_gz(file_path, extract_to):
    """
    Extract a .tar.gz file to a specified directory.
    """
    try:
        with tarfile.open(file_path, "r:gz") as tar:
            tar.extractall(path=extract_to)
        logging.info(f"Extracted: {file_path} to {extract_to}")
    except (tarfile.TarError, IOError) as err:
        logging.error(f"Failed to extract file: {err}")
        return False
    return True
