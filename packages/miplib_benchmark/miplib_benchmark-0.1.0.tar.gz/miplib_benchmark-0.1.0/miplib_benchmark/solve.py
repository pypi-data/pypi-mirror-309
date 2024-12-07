import highspy
import numpy as np
import pathlib
import gzip
from prisma.models import Result

from .db import with_db_retries, DB 
from .logger import logger
from .metadata import load_instances_metadata
from .dataset import get_mps_files_dir

def get_instance_path(instance_name: str) -> pathlib.Path:
    # use glob to find the instance path
    logger.info(f"Searching for instance {instance_name} in {get_mps_files_dir()}")
    mps_file_path = get_mps_files_dir() / f"{instance_name}.mps"
    # if the mps file exists, return it
    if mps_file_path.exists():
        logger.info(f"Found instance {instance_name} at {mps_file_path}")
        return mps_file_path
    
    # otherwise, search for .mps.gz
    mps_gz_file_path = get_mps_files_dir() / f"{instance_name}.mps.gz"
    if mps_gz_file_path.exists():
        logger.info(f"Found compressed instance {instance_name} at {mps_gz_file_path}")
        # unzip, write the unzipped file to instance_name.mps
        logger.info(f"Unzipping {mps_gz_file_path}")
        with gzip.open(mps_gz_file_path, "rb") as f:
            with open(mps_file_path, "wb") as f_out:
                f_out.write(f.read())
        return mps_file_path

    # if no instance is found, raise an error
    raise FileNotFoundError(f"Instance {instance_name} not found")

@with_db_retries()
def add_result(db: DB, data: dict) -> Result:
    result = db.result.create(data=data)
    logger.info(f"Saved result to database: {result}")
    return result

def solve_first_instance(): 
    metadata = load_instances_metadata()
    first_instance_name = metadata.iloc[0]["InstanceInst."]
    solve_instance(first_instance_name)

def solve_instance(instance_name: str) -> Result:
    instance_path = get_instance_path(instance_name)
    instance_path_str = str(instance_path)
    # solve the instance
    model = highspy.Highs()
    time_limit = 5
    model.setOptionValue("time_limit", time_limit)
    model.readModel(instance_path_str)
    model.run()
    runtime = model.getRunTime()
    
    info = model.getInfo()
    # Convert inf values to None for database compatibility
    gap = None if np.isinf(info.mip_gap) else info.mip_gap
    objective = None if np.isinf(info.objective_function_value) else info.objective_function_value
    print(info)
    data = {
        "instance_name": instance_name,
        "runtime": runtime,
        "time_limit": time_limit,
        "objective": objective,
        "gap": gap,
    }
    print(data)
    return add_result(data)
