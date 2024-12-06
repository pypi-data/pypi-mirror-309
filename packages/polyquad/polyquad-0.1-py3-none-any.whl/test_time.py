import time

import numpy as np
from scipy.io import loadmat
import matplotlib.pyplot as plt

import polyquad


if __name__=='__main__':
    last_order = 25
    #ddry run to init all numba codes and vandermonde matrices
    geometry_file = '../demo/icosphere.mat'
    geo = loadmat(geometry_file)
    vertices = geo['verts']
    vertices[:,0] = vertices[:,0]*2
    vertices +=3
    faces = geo['faces']
    for order in range(1,last_order):
        print(f'doing order {order}')
        p, w, r = polyquad.get_quadrature(order, vertices, faces, get_residual = True)
        p, w, rsolve = polyquad.get_quadrature_solve(order, vertices, faces, get_residual = True)
        
    
    fig, axs = plt.subplots(2,2)
    fig.suptitle('evolution of the time spent for different polyhedra')
    geos = ['icosphere', 'tripod', 'spheres', 'bunny']
    tmp = [[0,0],[0,1],[1,0],[1,1]]
    jj = 0
    for geoName in geos:
        geometry_file = '../demo/'+geoName+'.mat'
        geo = loadmat(geometry_file)
        vertices = geo['verts']
        vertices[:,0] = vertices[:,0]*2
        vertices +=3
        faces = geo['faces']

        orders = np.arange(1,last_order)
        resList = np.zeros(len(orders))
        resListInv = np.zeros(len(orders))

        tsolve = np.zeros(len(orders))
        tlu = np.zeros(len(orders))

        for ii,order in enumerate(orders):
            print(f'doing order {order}')
            t1 = time.perf_counter()
            p, w, r = polyquad.get_quadrature(order, vertices, faces, get_residual = True)
            t2 = time.perf_counter()
            p, w, rsolve = polyquad.get_quadrature_solve(order, vertices, faces, get_residual = True)
            t3 = time.perf_counter()

            tlu[ii] = t2-t1
            tsolve[ii] = t3-t2
            resList[ii] = r
            resListInv[ii] = rsolve

        # axs[*tmp[jj]].semilogy(orders,resList,label = 'solve(a,b)')
        # axs[*tmp[jj]].semilogy(orders,resListInv,label = 'inv(a)*b')
        # axs[*tmp[jj]].legend()
        # axs[*tmp[jj]].grid()
        # axs[*tmp[jj]].set_title(geoName)
        # jj+=1

        axs[*tmp[jj]].semilogy(orders,tsolve,label = 'solve(a,b)')
        axs[*tmp[jj]].semilogy(orders,tlu,label = 'LU(a)*b')
        axs[*tmp[jj]].legend()
        axs[*tmp[jj]].grid()
        axs[*tmp[jj]].set_title(geoName)
        jj+=1

    print(f'timming with solve: {tsolve}s')
    print(f'timming with lu: {tlu}s')
    plt.show()
