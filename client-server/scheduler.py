#!/usr/bin/env python

import asyncio
from pathlib import Path

from mpi4py import MPI


print('SCHEDULER: Opening new port...', flush=True)
port = MPI.Open_port()
print(f'           Port Opened: {port}', flush=True)

print('SCHEDULER: Saving port to config file', flush=True)
cfg_file = Path('mpiport.cfg')
with open(cfg_file, 'w') as cfg:
    cfg.write(port)


async def accept_new_workers(comms):
    while True:
        await asyncio.sleep(1)
        comm = MPI.COMM_WORLD.Accept(port, root=0).Merge()
        comms.append(comm)
        print(f'New worker connected ({len(comms)})', flush=True)

print('SCHEDULER: Accepting connections on new port...', flush=True)
worker_comms = []
asyncio.run(accept_new_workers(worker_comms))

print('SCHEDULER: Summary:', flush=True)
for i, comm in enumerate(worker_comms):
    print(f'           Worker {i} COMM rank/size: {comm.Get_rank()}/{comm.Get_size()}', flush=True)

numbers = list(i+10 for i in range(len(worker_comms)))
for n, comm in zip(numbers, worker_comms):
    print(f'SCHEDULER: Sending {n} to worker', flush=True)
    comm.send(n, dest=0)

print('SCHEDULER: Closing port', flush=True)
MPI.Close_port(port)

print('SCHEDULER: Deleting config file', flush=True)
cfg_file.unlink()
