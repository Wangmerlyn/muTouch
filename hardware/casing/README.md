# Sensor Casing / Enclosure

This folder contains the 3D printable casing/enclosure for the μTouch sensor array.

## Files

| File | Description |
|------|-------------|
| `mutouch_sensor_casing.stl` | 3D model file (STereoLithography format) for the sensor casing. Can be imported into any 3D printing slicer software. |
| `mutouch_sensor_casing.gcode` | Pre-generated G-code file ready for 3D printing. Generated for standard FDM printers; you may need to re-slice with your specific printer settings. |

## Printing Recommendations

- **Material**: PLA or PETG recommended for durability and ease of printing
- **Infill**: 20-30% for structural integrity
- **Layer Height**: 0.2mm for good detail/print time balance
- **Supports**: May be required depending on your printer and orientation

## Design Notes

The casing is designed to house the μTouch PCB sensor array and provide a comfortable form factor for wearable applications.

## Related

- PCB design files: [`../pcb/`](../pcb/)
- Firmware: [`../Codes/Arduino/`](../Codes/Arduino/)
