from mpi4py import MPI
import sys

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

print('rank:', rank)
print('args: ', len(sys.argv))
      
if rank == 0:
    data = {'a': 7, 'b': 3.14}
    
    for i in range(1,size):
        print('root sending data', data, 'to rank', i)
        comm.send(data, dest=i, tag=11)
else:
    data = comm.recv(source=0, tag=11)
    print('rank:', rank, 'received data', data)
