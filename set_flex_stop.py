#!/usr/bin/env python3

"""Set the mode of the Zappi to eco+"""

import run_zappi
import mec.zp
from mec.zp import DataException
from datetime import datetime, time

import logging as log

def set_eddi_mode(self, sno, on):
    on = 1 if on else 0
    log.debug('Setting eddi to %s', "Normal (not Stop)" if bool(on) else "Stop")
    try:
        data = self._load(suffix='cgi-eddi-mode-E{}-{}'.format(sno,on))
        log.debug(data)
        return data
    except DataException as e:
        log.debug('Error setting mode')
        log.debug(e)
        return 'Exception'
    
mec.zp.MyEnergiHost.set_eddi_mode = set_eddi_mode

def main():
    """Main"""

    config = run_zappi.load_config()

    server_conn = mec.zp.MyEnergiHost(config['username'], config['password'])
    server_conn.refresh()

    divert_on = True

    # Set ecop to False between 16:00 and 19:00
    if time(16, 0) <= datetime.now().time() < time(19, 0):
        divert_on = False

    for zappi in server_conn.state.zappi_list():
        if divert_on:
            print(server_conn.set_mode_ecop(zappi.sno))
        else:
            print(server_conn.set_mode_stop(zappi.sno))
        print('Zappi is currently in mode {}'.format(zappi.mode))

    for eddi in server_conn.state.eddi_list():
        server_conn.set_eddi_mode( eddi.sno, divert_on )
        print('Eddi is currently in mode {}'.format(eddi.status))
        
if __name__ == '__main__':
    main()
