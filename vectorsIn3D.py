#!/usr/bin/python3

#To do: add more colours in case we have more than 7 features.
#This only works with 3 morphemes in morpheme space.
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

class VectorsIn3D:

    def __init__(self, weights, dim1, dim2, dim3, title, features, weights2=None):
        self.weights = list(weights)
        if weights2 != None:
            self.weights2 = list(weights2)
        else:
            self.weights2 = None
        self.dim1 = dim1
        self.dim2 = dim2
        self.dim3 = dim3
        self.num_features = len(features)
        self.xlow = []
        self.ylow = []
        self.zlow = []
        for i in range(self.num_features):
            for l in [self.xlow, self.ylow, self.zlow]:
                l.append(0)
        self.title = title
        self.features = features
        self.colours = ['b', 'r', 'g', 'y', 'c', 'm', 'k']
        return


    def getAx(self):
        self.xhigh = []
        self.yhigh = []
        self.zhigh = []
        for w in self.weights:
            self.xhigh.append(w[0])
            self.yhigh.append(w[1])
            self.zhigh.append(w[2])
        if self.weights2 != None:
            self.xhigh2 = []
            self.yhigh2 = []
            self.zhigh2 = []
            for w2 in self.weights2:
                self.xhigh2.append(w2[0])
                self.yhigh2.append(w2[1])
                self.zhigh2.append(w2[2])
                              
        self.fig = plt.figure()
        self.ax  = self.fig.add_subplot(111, projection = '3d')
        self.ax.set_title(self.title+' with features '+self.dim1+' ' +self.dim2+' '+self.dim3, fontsize=12, y=1.1)
        self.ax.set_xlabel(self.dim1.upper())
        self.ax.set_ylabel(self.dim2.upper())
        self.ax.set_zlabel(self.dim3.upper())
        for i,ii,j,jj,k,kk,c in zip(self.xlow,self.xhigh,self.ylow,self.yhigh,self.zlow,self.zhigh, self.colours):
            self.ax.plot([i,ii],[j,jj],[k,kk],color = c) #Draw line from (i,j,kk) to (ii,jj,kk)
        if self.weights2 != None:
            for i,ii,j,jj,k,kk,c in zip(self.xlow,self.xhigh2,self.ylow,self.yhigh2,self.zlow,self.zhigh2, self.colours):
                self.ax.plot([i,ii],[j,jj],[k,kk],color = c, linestyle='dotted') #Draw line from (i,j,kk) to (ii,jj,kk)
            for i, f in enumerate(self.features):
                self.ax.plot([self.weights2[i][0]],[self.weights2[i][1]], [self.weights2[i][2]], self.colours[i]+'o', label=f)
        for i, f in enumerate(self.features):
            self.ax.plot([self.weights[i][0]],[self.weights[i][1]], [self.weights[i][2]], self.colours[i]+'^', label=f)
        plt.legend(numpoints=1, loc=1, fontsize='small', frameon=False)
        plt.show()
        plt.close(self.fig)
        return


