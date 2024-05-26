from __future__ import annotations

import logging

from GTC import type_a, ureal
from GTC.lib import UncertainReal
from msl.equipment import ConnectionRecord, EquipmentRecord

logging.basicConfig(level=logging.CRITICAL)

records = {
    'a': EquipmentRecord(
        manufacturer='HP',
        model='34401A',
        connection=ConnectionRecord(
            address='COM9',
            timeout=10,
        )
    ),
    'b': EquipmentRecord(
        manufacturer='HP',
        model='34401A',
        connection=ConnectionRecord(
            address='COM8',
            timeout=10,
        )
    ),
    'c': EquipmentRecord(
        manufacturer='HP',
        model='34401A',
        connection=ConnectionRecord(
            address='COM10',
            timeout=10,
        )
    ),
}


FUNCTIONS = {
    'ACV': 'VOLTAGE:AC',
    'ACI': 'CURRENT:AC',
    'DCV': 'VOLTAGE:DC',
    'DCI': 'CURRENT:DC',
}

class HP34401A:

    def __init__(self, name: str) -> None:
        """Hewlett Packard 34401A digital multimeter."""
        self._cxn = records[name].connect()

        reply = self._cxn.query('SYSTEM:REMOTE;*OPC?')
        assert reply.startswith('1')

    def configure(self,
                  function: str,
                  *,
                  range: float = 1,  # noqa: Shadows built-in name 'range'
                  nsamples: int = 1,
                  nplc: float = 10,
                  auto_zero: bool = True):
        """Configure the digital multimeter.

        Args:
            function: The measurement function (e.g., ACV, ACI, DCV, DCI).
            range: The range to use for the measurement.
            nsamples: The number of samples to acquire.
            nplc: The number of power-line cycles (only used for DC measurements).
        """
        if nsamples > 512:
            raise ValueError(f'Invalid number of samples, {nsamples}. Must be <= 512')

        fcn = FUNCTIONS[function.upper()]
        nplc_str = '' if fcn.endswith('AC') else f':SENSE:{fcn}:NPLC {nplc};'
        az = 'ON' if auto_zero else 'OFF'
        reply = self._cxn.query(
            f':CONFIGURE:{fcn} {range};'
            f'{nplc_str}'
            f':SENSE:ZERO:AUTO {az};'
            f':SAMPLE:COUNT {nsamples};'
            f':TRIGGER:SOURCE IMMEDIATE;COUNT 1;DELAY:AUTO ON;'
            f'*OPC?'
        )
        assert reply.startswith('1')

    def disconnect(self) -> None:
        """Set the digital multimeter to be in LOCAL mode and then close the connection."""
        self._cxn.query('SYSTEM:LOCAL;*OPC?')
        self._cxn.disconnect()

    def initiate(self) -> None:
        """Put the digital multimeter in the wait-for-trigger state (arm the trigger)."""
        self._cxn.write('INITIATE;*OPC?')

    def fetch(self) -> UncertainReal:
        """Fetch the samples."""
        assert self._cxn.read().startswith('1')  # wait for *OPC? that was sent in self.initiate() 
        data = tuple(map(float, self._cxn.query('FETCH?').split(',')))
        if len(data) > 1:
            return type_a.estimate(data)
        return ureal(data[0], 0)
