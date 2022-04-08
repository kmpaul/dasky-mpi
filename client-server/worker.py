#!/usr/bin/env python

from pathlib import Path
from time import sleep

from mpi4py import MPI


cfg_file = Path('mpiport.cfg')
print('WORKER: Looking for port configuration file...', flush=True)
while not cfg_file.exists():
    sleep(1)
print('WORKER: Port configuration file found', flush=True)

print('WORKER: Reading port configuration file', flush=True)
with open(cfg_file) as cfg:
    port = cfg.read()
print(f'        Port configuration found: {port}', flush=True)

print('WORKER: Connecting to remote port...', flush=True)
comm = MPI.COMM_WORLD.Connect(port, root=0).Merge()
print('WORKER: Connected', flush=True)
print(f'WORKER: COMM rank/size: {comm.Get_rank()}/{comm.Get_size()}', flush=True)
print(f'WORKER: MPI rank: {comm.Get_rank()}', flush=True)

n = comm.recv(source=1)
print(f'WORKER: Received {n} from scheduler', flush=True)
