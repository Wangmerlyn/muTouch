"""
Calibrate the sensor and visualize the result
"""
import os
from src.preprocess import Calibrate_Data
from utils.read_files import find_latest_file_with_prefix_and_suffix

if __name__ == "__main__":
    calib_folder = "datasets/calib_3"
    cali_path = find_latest_file_with_prefix_and_suffix(
        calib_folder, "calib_3-", ".csv"
    )
    cali_path = os.path.join(calib_folder, cali_path)
    cali_data = Calibrate_Data(cali_path)
    cali_data.show_cali_result()
