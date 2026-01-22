# Code Overview (μTouch)

## Arduino
- `batteryTest`: read battery voltage/level of the Adafruit Feather.
- `bleReadMultiple`: collect readings from the magnetometer array and send via BLE.
- `localReadMultiple`: stream readings over serial.
- `Library`: patched Adafruit_MLX90393 driver for better diagnostics.

## read_raw_ble
- BLE discovery (`find_device.py`), calibration capture (`read_sensor.py`), real-time capture (`read_sensor_real.py`), and online classifiers (`read_sensor_real_classifier.py`, silicon variants).
- TS2Vec embedding submodule (`ts2vec`) and trained models under `models/`.
- Utilities for result analysis, timing, and file parsing.

## optimization
- Calibration helpers, feature engineering, and layout/positioning algorithms; see per-module docs inside the folder.

## requirements.txt
- Python dependency pins used during development; install via `pip install -r Codes/requirements.txt` if you are not using `pip install -e .[dev]`.
