# μTouch: Accurate, Lightweight Self-Touch Sensing with Passive Magnets

## About
This directory contains code and PCB files for μTouch, as described in:

> [_μTouch: Enabling Accurate, Lightweight Self-Touch Sensing with Passive Magnets_]  
> Siyuan Wang, Ke Li, Jingyuan Huang, Jike Wang, Cheng Zhang, Alanson Sample, Dongyao Chen.  
> Proceedings of IEEE PerCom 2026 (to appear).

μTouch is a compact magnetic-sensing platform for recognizing self-touch micro‑gestures (e.g., nuanced face touches or subtle scratches). It combines low‑power magnetometers, magnetic silicon, and a lightweight semi‑supervised pipeline that needs only a few seconds of user data to adapt.

## Abstract
> Self-touch gestures (e.g., nuanced facial touches and subtle finger scratches) provide rich insights into human behaviors, from hygiene practices to health monitoring. However, existing approaches fall short in detecting such micro gestures due to their diverse movement patterns.  
> This paper presents μTouch, a novel magnetic sensing platform for self-touch gesture recognition. μTouch features (1) a compact hardware design with low-power magnetometers and magnetic silicon, (2) a lightweight semi-supervised framework requiring minimal user data, and (3) an ambient field detection module to mitigate environmental interference.  
> We evaluated μTouch in two representative applications in user studies with 11 and 12 participants. μTouch only requires three-second fine-tuning data for each gesture — new users need less than one minute before starting to use the system. μTouch can distinguish eight different face-touching behaviors with an average accuracy of **93.41%**, and reliably detect body-scratch behaviors with an average accuracy of **94.63%**. μTouch demonstrates accurate and robust sensing performance even after a month, showcasing its potential as a practical tool for hygiene monitoring and dermatological health applications.

## What’s in this repo
- **Firmware & data collection**: `Codes/Arduino` sketches and BLE data collection scripts in `Codes/read_raw_ble`.
- **Models & inference**: real-time classifiers, TS2Vec-based embeddings (submodule), and result analysis tools in `Codes/read_raw_ble`.
- **Optimization & calibration**: signal processing, calibration, and layout exploration code in `Codes/optimization`.
- **Hardware**: Magway PCB design package in `pcb/` (Altium project, BoM doc, PnP outputs).

## Quick start (edge pipeline)
1. **Hardware**: assemble the Magway PCB (see `pcb/README.md`) and flash `Codes/Arduino/bleReadMultiple/bleReadMultiple.ino` to the sensing array.
2. **Find device**: run `Codes/read_raw_ble/find_device.py` to locate your BLE address.
3. **Collect calibration**: run `Codes/read_raw_ble/read_sensor.py`, set the BLE address and output file name; perform figure‑8 motion away from magnetic interference.
4. **Run real-time classifier**: use `Codes/read_raw_ble/read_sensor_real.py` (data collection) or `read_sensor_real_classifier.py` (inference). Update offsets/scales to the latest calibration files and adjust model paths if needed.

## Development setup
- Python 3.10 (recommended)  
- Create env: `conda create -y -n muTouch python=3.10`  
- Install deps: `pip install -e .[dev]`  
- Install hooks: `pre-commit install`  
- Lint: `ruff check .`

## License
MIT License (see [LICENSE](LICENSE)).

## Credits
This codebase builds on the MagX project (MobiCom 2021). We retain the legacy MagX citation for attribution while extending the system to μTouch’s self-touch sensing pipeline.

## Citation (μTouch, PerCom 2026)
```bibtex
@inproceedings{mutouch_percom2026,
  author    = {Wang, Siyuan and Li, Ke and Huang, Jingyuan and Wang, Jike and Zhang, Cheng and Sample, Alanson and Chen, Dongyao},
  title     = {{\textmu}Touch: Enabling Accurate, Lightweight Self-Touch Sensing with Passive Magnets},
  booktitle = {Proceedings of the IEEE International Conference on Pervasive Computing and Communications (PerCom)},
  year      = {2026},
  address   = {Pisa, Italy},
  month     = mar,
  note      = {To appear}
}
```

### Legacy MagX citation
```bibtex
@inproceedings{MagX2021,
  author    = {Dongyao Chen and Mingke Wang and Chenxi He and Qing Luo and Yasha Iravantchi and Alanson Sample and Kang G. Shin and Xinbing Wang},
  title     = {MagX: Wearable, Untethered Hands Tracking with Passive Magnets},
  booktitle = {Proc. ACM MobiCom},
  year      = {2021}
}
```
