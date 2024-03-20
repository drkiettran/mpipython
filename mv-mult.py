from mpi4py import MPI

from mpi4py import MPI
import sys

m_val = 7
n_val = 5
raw_x = [3, 1, 4, 0, 3]
raw_A = [[2, 1, 3, 4, 0], 
         [5, -1, 2, -2, 4], 
         [0, 3, 4, 1, 2], 
         [2, 1, 3, 4, 0], 
         [5, -1, 2, -2, 4], 
         [0, 3, 4, 1, 2], 
         [2, 3, 1, -3, 0]
        ]

def get_input(rank):
    return raw_A, raw_x, m_val, n_val

def mv_mult(A, x, m, n):
    B = []
    for i in range(m):
        B.append(0)
    for row in range(m):
        for col in range(len(A[row])):
            B[row] += A[row][col] * x[col]
    return B

root = 0

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
count = 0; rem = 0; m = 0; n = 0; rem = 0
A = None; x = None

# print('rank:', rank)
# print('args: ', len(sys.argv))
      
if root == rank:
    A, x, m, n = get_input(rank)
    # print('A:\n', A)
    # print('x:\n', A)
    # print('m: ', m, 'n:', n)
    
    if size > 1:
        count = m // (size-1)
        rem = m % (size-1)
    else:
        count = m
        rem = m

# broadcast count and n.
count = comm.bcast(count, root=0)
m = comm.bcast(m, root=0)
rem = comm.bcast(rem, root=0)

if root == rank:
    for i in range(1,size):
        print('Sending to ', i, count, 'rows')
        comm.send(x, dest=i, tag=77)
        comm.send(A[(i-1)*count:i*count], dest=i, tag=77)
    B = mv_mult(A[(size-1)*count:], x, rem, n)
    y = []
    for i in range(1,size):
        x = comm.recv(source=i, tag=77)
        for e in x:
            y.append(e)
    for e in B:
        y.append(e)
    print('\n\nOutput:\n', y)
else:
    x = comm.recv(source=root, tag=77)
    A = comm.recv(source=root, tag=77)
    print(rank, 'receives vector', x)
    print(rank, 'receives matrix', A)
    B = mv_mult(A, x, count, n)
    comm.send(B, dest=root, tag=77)
    print(rank, ':', B)
