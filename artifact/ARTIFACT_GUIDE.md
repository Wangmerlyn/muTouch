# μTouch Artifact Guide (Markdown Edition)

This Markdown guide is the detailed, always-updated companion to the short PDF checklist. Follow the steps below to reproduce the artifact, evaluate the system, and modify the code.

> Recommended view: [GitHub preview](https://github.com/Wangmerlyn/muTouch/blob/main/artifact/ARTIFACT_GUIDE.md)

## 1. Prerequisites
- OS: Ubuntu 20.04+ or macOS 12+ (tested on laptop CPU).
- Python 3.10.
- BLE 4.0+ adapter (USB dongle if desktop lacks BLE).
- Hardware: assembled μTouch PCB (files under `pcb/`, legacy filenames `Magway.*` kept for Altium compatibility), N52 magnets (6–8 mm, 1–2 pcs).

## 2. Setup
```bash
git clone --recurse-submodules git@github.com:Wangmerlyn/muTouch.git
# If SSH shows permission denied, use HTTPS:
# git clone --recurse-submodules https://github.com/Wangmerlyn/muTouch.git
cd muTouch
conda create -y -n muTouch python=3.10
conda activate muTouch   # prompt should show (muTouch)
pip install -r Codes/requirements.txt
cd Codes   # all runtime scripts assume this as the working directory
```
Why: isolating deps avoids version drift; success = no pip errors and `(muTouch)` prefix in your prompt.

## 3. Flash firmware
1. Open `Codes/Arduino/bleReadMultiple/bleReadMultiple.ino` in Arduino IDE.
2. Board: Adafruit Feather nRF52.
3. Upload to the sensing array.

## 4. Find BLE address
```bash
python read_raw_ble/find_device.py
```
Copy the device MAC/UUID.

## 5. Hardcode the address
Edit the `address = "..."` line near the bottom of:
- `read_raw_ble/read_sensor.py`
- `read_raw_ble/read_sensor_real.py`
- `read_raw_ble/read_sensor_real_classifier.py` (if you run the classifier)

## 6. Calibration capture
```bash
python read_raw_ble/read_sensor.py
```
- Perform a brief figure-8 motion away from metal.
- Raw CSVs are saved under `datasets/`.

## 7. Offsets & scales
- Latest calibration arrays are expected in `calibration_files/` as:
  - `offset-*.npy`
  - `scale-*.npy`
- The real-time scripts automatically load the newest timestamped files with those prefixes.

## 8. Real-time data collection
```bash
python read_raw_ble/read_sensor_real.py
```
Captures calibrated magnetometer streams; outputs timestamped CSVs under `datasets/` (one file per run).

## 9. Real-time classification
```bash
python read_raw_ble/read_sensor_real_classifier.py
```
Runs live classifier; expect gesture labels printed to console and logged under `datasets/`. Ensure offset/scale and model paths point to your latest files/checkpoints in `read_raw_ble/models/`.

## 10. Expected outcomes (baseline)
- Face-touching: ~93% accuracy (8 gestures) with 3 s/user fine-tuning.
- Scratch detection: ~95% accuracy (9 gestures) with 3 s/user fine-tuning.
- Real-time loop: >30 Hz on a laptop CPU.

## 11. TS2Vec submodule
The repo pulls the TS2Vec submodule used for embedding; no extra install steps beyond `requirements.txt` are needed. If you re-clone without `--recurse-submodules`, run:
```bash
git submodule update --init --recursive
```

## 12. Common issues
- **BLE not found**: rerun `find_device.py`; check power/pairing; try a USB BLE dongle.
- **Drift or noisy labels**: recalibrate; ensure distance from large metal; regenerate offset/scale.
- **Import errors**: verify working dir is `Codes/`; rerun submodule init.

## 13. Where to get more details
- Main repo overview and hardware credits: `README.md`.
- Short PDF checklist: `artifact/artifact_guide.pdf`.
- For modifications or reproduction, prefer this Markdown guide and `README.md`; the PDF is intentionally concise due to page limits.

## 14. Re-run the PDF (optional)
If you edit LaTeX and need the PDF:
```bash
cd artifact
/tmp/tectonic artifact_guide.tex
```

## 15. Attribution
This work builds on MagX (MobiCom’21) for magnetic sensing; see the BibTeX entry in the LaTeX guide (`\cite{mag_x}`).
