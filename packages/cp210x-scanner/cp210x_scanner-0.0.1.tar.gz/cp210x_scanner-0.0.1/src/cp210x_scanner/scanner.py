from dataclasses import dataclass
from typing import List

from serial.tools.list_ports_common import ListPortInfo

from .CP210xManufacturing import PartNames
from dataclasses_json import dataclass_json

from .CP210xManufacturing import CP210xManufacturing, CP210x_SUCCESS

import serial.tools.list_ports


@dataclass_json
@dataclass
class Cp210xDeviceInfo:
    device_index: int = None
    part_number: str = None
    vid: int = None
    pid: int = None
    manufacturer: str = None
    product: str = None
    sn: str = None
    version: str = None
    port: str = None


def scan_cp210x_devices() -> List[Cp210xDeviceInfo]:
    devices: List[Cp210xDeviceInfo] = []
    serialports = serial.tools.list_ports.comports()

    cp210xlib = CP210xManufacturing()
    (status, NumDevices) = cp210xlib.CP210x_GetNumDevices()

    for i in range(0, NumDevices):
        device_info = get_device_info(cp210xlib, i)
        if device_info is not None:
            device_info.port = _get_comport(device_info, serialports)
            devices.append(device_info)
    return devices


def _get_comport(device_info: Cp210xDeviceInfo, serialports: List[ListPortInfo]):
    for sp in serialports:
        try:
            hwid = sp.hwid
            if hwid.find('USB VID:PID') == 0:
                hwid = hwid[12:]
                hwid = hwid.split(' ')
                [vid, pid] = hwid[0].split(':')
                sn = hwid[1].strip('SER=')
                if device_info.vid == int(vid, 16) and device_info.pid == int(pid, 16) and device_info.sn == sn:
                    return sp.device
        except Exception as e:
            pass


def get_device_info(device, dev_idx):
    device_info = Cp210xDeviceInfo()
    device_info.device_index = dev_idx

    if device.CP210x_Open(dev_idx) != CP210x_SUCCESS:
        return None
    (status, PartNum) = device.CP210x_GetPartNumber()
    if status == CP210x_SUCCESS:
        device_info.part_number = PartNames.get(PartNum, 'UNKNOWN')
    (status, devVID) = device.CP210x_GetDeviceVid()
    if status == CP210x_SUCCESS:
        device_info.vid = devVID
    (status, devPID) = device.CP210x_GetDevicePid()
    if status == CP210x_SUCCESS:
        device_info.pid = devPID

    (status, wVersion) = device.CP210x_GetDeviceVersion()
    if status == CP210x_SUCCESS:
        device_info.version = wVersion

    (status, manufacturer) = device.CP210x_GetDeviceManufacturerString()
    if status == CP210x_SUCCESS:
        device_info.manufacturer = manufacturer

    (status, product) = device.CP210x_GetDeviceProductString()
    if status == CP210x_SUCCESS:
        device_info.product = product

    (status, sn) = device.CP210x_GetDeviceSerialNumber()
    if status == CP210x_SUCCESS:
        device_info.sn = sn

    device.CP210x_Close()
    return device_info
