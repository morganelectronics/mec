#!/usr/bin/env python3

"""Set the mode of the Zappi to eco+"""

import run_zappi
import mec.zp
from datetime import datetime, time

def main():
    """Main"""

    config = run_zappi.load_config()

    server_conn = mec.zp.MyEnergiHost(config['username'], config['password'])
    server_conn.refresh()

    for zappi in server_conn.state.zappi_list():
        print('Zappi is currently in mode {}'.format(zappi.mode))

        ecop = True

        # Set ecop to False between 16:00 and 19:00
        if time(16, 0) <= time() < time(19, 0):
            ecop = False

        if ecop:
            print(server_conn.set_mode_ecop(zappi.sno))
        else:
            print(server_conn.set_mode_stop(zappi.sno))

if __name__ == '__main__':
    main()
