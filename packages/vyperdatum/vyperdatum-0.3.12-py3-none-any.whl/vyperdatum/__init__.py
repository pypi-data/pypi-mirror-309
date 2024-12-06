from importlib.metadata import version
import os
import pathlib
import json
import time
import logging.config
from osgeo import gdal

__version__ = version("vyperdatum")
log_configuration_dict = json.load(
    open(
        pathlib.Path(
            pathlib.Path(__file__).parent, "logging_conf.json"
        )
    )
)
logging.config.dictConfig(log_configuration_dict)
logging.Formatter.converter = time.gmtime

os.environ.update(PROJ_NETWORK="ON")
gdal.UseExceptions()

# db = DB(db_dir=r"path\to\datum_file")
