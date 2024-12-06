from src.cp210x_scanner.CP210xManufacturing import CP210xManufacturing
from src.cp210x_scanner.scanner import scan_cp210x_devices
devices = scan_cp210x_devices()
print(devices)