import os
from wdpkp.utils import log


def send(file):
    log.info('EXPORTING VIDEO...')
    os.system('scp -q ' + file + ' ' + os.getenv("EXPORT_USER") + '@' + os.getenv("EXPORT_HOST") + ':' + os.getenv("EXPORT_DIR"))
