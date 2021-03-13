'''
usage: python visible_gpuusage.py gpu-order
'''

import os
import sys
import time
import datetime

# cmd = "nvidia-smi | grep MiB | awk '{print $9}' | sed -n '3p'"

cmd = "nvidia-smi --query-gpu=memory.used --format=csv"
totalcmd = "nvidia-smi --query-gpu=memory.total --format=csv"


def visible(gpuorder, total, log=None):
  while True:
    with os.popen(cmd) as f:
      lines = f.read().strip().split('\n')
      keyline = lines[gpuorder + 1]
      used = keyline.split()[0]
      percent = int(int(used) / total * 100)
      prgbar = '{:100}'.format('>' * percent)
      print(prgbar + f'{used:>5s}', end='\r')
      if log is not None:
        log.write(f'{datetime.datetime.today()} {prgbar}{used}\n')
        log.flush()
    time.sleep(1)


def main(args):
  gpuorder = int(args[0])
  total = int(
      os.popen(totalcmd).read().strip().split('\n')[gpuorder + 1].split()[0])
  logfile = args[1] if len(args) > 1 else None
  if logfile is not None:
    log = open(logfile, 'w')
  else:
    log = None
  visible(gpuorder, total, log)


if __name__ == '__main__':
  main(sys.argv[1:])