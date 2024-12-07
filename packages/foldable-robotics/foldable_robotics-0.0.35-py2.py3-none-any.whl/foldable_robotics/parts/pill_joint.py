# -*- coding: utf-8 -*-
"""
Written by Daniel M. Aukes and CONTRIBUTORS
Email: danaukes<at>asu.edu.
Please see LICENSE for full license.
"""

#import modules from shapely and matplotlib
import shapely.geometry as sg
import matplotlib.pyplot as plt

#import classes from my local modules
from foldable_robotics.laminate import Laminate
from foldable_robotics.layer import Layer

import foldable_robotics.manufacturing
import numpy

def generate(
        radius = .01,
        num_perforations = 5,
        ):

    num_segments = num_perforations*2+1
    num_points = num_segments+1
    a=numpy.r_[0:1:num_points*1j]
    lines = []
    for ii in range(int(len(a)/2)-1):
        p1 = sg.Point(a[2*ii+1]+radius,0)
        p2 = sg.Point(a[2*ii+2]-radius,0)
        lines.append(sg.LineString((p1,p2)))
    hinge = Layer(*lines)
    hinge<<=radius
    lam = Laminate(hinge)
    return lam



if __name__=='__main__':
    plt.ion()
    hinge = generate()
    plt.figure()
    hinge.plot()
    plt.show()
    # from foldable_robotics.dynamics_info import MaterialProperty
    # import idealab_tools.plot_tris as pt
    
    # m = MaterialProperty.make_n_blank(5,thickness = .1)
    
    # mesh_items = hinge.mesh_items(m)
    # pt.plot_mi(mesh_items)
