# #-*- coding:utf8 -*-
# from noise import pnoise2,pnoise3
# import numpy  as np
# from  numpy import sin,cos,arccos,arcsin,sqrt
# import pandas as pd
# import random
# import matplotlib.pyplot as plt

# def timer(func):
#     import datetime
#     from functools import wraps

#     @wraps(func)
#     def decorated(*args, **kwargs):
#         starttime = datetime.datetime.now()
#         res=func(*args, **kwargs)
#         endtime = datetime.datetime.now()
#         print('time used {} sec'.format((endtime - starttime).seconds))
#         return res
#     return decorated

# class Sphere:

#     def __init__(self,radius):
#         self.radius=radius

#     def coord_trans(self,longitude,latitude,radius=None):
#         '''
#         coordinate transformation
#         Cartesian coordinates
#         '''
#         lat,lon=latitude,longitude
#         if radius is None:
#             r=self.radius
#         else:
#             r=radius

#         x = r * cos(lat) * cos(lon)
#         y = r * cos(lat) * sin(lon)
#         z = r * sin(lat)
#         return x,y,z

#     def distance(self,lon,lat,angle='degrees',radius=None):
#         if angle=='degrees':
#             lon,lat=np.radians([lon,lat])

#         a1,a2=lat
#         b1,b2=lon
#         if radius is None:
#             r1=r2 =self.radius
#         elif isinstance(radius,(int,float)):
#             r1=r2 = radius
#         else:
#             r1,r2,*_=radius

#         'Cartesian distance'
#         tmp = cos(a1) * cos(a2) * cos(b1 - b2) + sin(a1) * sin(a2)
#         L = sqrt(r1 ** 2 + r2 ** 2 - 2 * r1 * r2 * tmp)

#         if r1==r2:
#             'spherical distance'
#             S = r1 * arccos(tmp)
#             return L,S
#         else:
#             return L,None

#     @timer
#     def create_sphere(self,unit=0.1,multiplier=1.0,stretch=1.0,
#                       seed=None,*args,**kwargs):
#         '''
#         Spherical coordinate system (lon,lat,r)
#         0 <= r < math.inf
#         0 <= lon <= PI * 2
#         -PI / 2 <= lat <= PI / 2
#         '''

#         lon=np.arange(-180,180,unit)
#         lat=np.arange(-90,90+unit,unit)

#         'coordinate transformation'
#         # coord = pd.MultiIndex.from_product([lon, lat], names=['lon', 'lat'])
#         # coord = pd.DataFrame(index=coord).reset_index()
#         lon1,lat1=np.meshgrid(lon,lat)
#         x, y, z = self.coord_trans(np.radians(lon1), np.radians(lat1), radius=stretch)

#         'default arguments'
#         if seed is None:
#             seed=random.randint(0,256)
#         else:
#             seed=int(seed)

#         'Define numpy ufunc(universal function)'
#         ufunc_pnoise3=lambda x,y,z:pnoise3(x, y, z,base=seed,*args,**kwargs)
#         self.ufunc_pnoise3=np.frompyfunc(ufunc_pnoise3, 3, 1)
#         h = self.ufunc_pnoise3(x,y,z)
#         # h=pd.pivot(coord.lat, coord.lon, h)

#         print('seed={}'.format(seed))
#         return lon,lat,h

#     def draw_sphere(self,lon,lat,h,map='ellipse'):
#         h1=h.copy()
#         h2=h.copy()
#         h1[h<0]=None
#         h2[h>0]=None

#         fig=plt.figure()
#         if map=='ellipse':
#             lon,lat=np.meshgrid(lon,lat)
#             lon=sqrt(1-(lat/90)**2)*lon
#             plt.contourf(lon, lat, h1, cmap='Greens_r')
#             plt.contourf(lon, lat, h2, cmap='Blues_r')
#         elif map=='cosine':
#             lon,lat=np.meshgrid(lon,lat)
#             lon=cos(np.radians(lat))*lon
#             plt.contourf(lon, lat, h1, cmap='Greens_r')
#             plt.contourf(lon, lat, h2, cmap='Blues_r')
#         else:
#             plt.contourf(lon, lat, h1, cmap='Greens_r')
#             plt.contourf(lon, lat, h2, cmap='Blues_r')
#         plt.show()

# earth=Sphere(radius=2)
# lon,lat,h=earth.create_sphere(octaves=10, persistence=0.5,multiplier=2,seed=57)
# earth.draw_sphere(lon,lat,h,map='ellipse')

import noise
import numpy as np
import matplotlib.pyplot as plt

# Set the seed for reproducibility
seed = 57

# Define the number of points you want in your 1D Perlin noise
num_points = 100

# Generate Perlin noise values
perlin_values = [noise.pnoise1(x/100.0, octaves=6, persistence=0.5, lacunarity=2.0, repeat=num_points, base=seed) for x in range(num_points)]

print(noise.pnoise1(255.1, octaves=6, persistence=0.5, lacunarity=2.0, repeat=num_points, base=seed))
print(perlin_values)
# Plot the Perlin noise
plt.plot(perlin_values)
plt.title("1D Perlin Noise")
plt.xlabel("X")
plt.ylabel("Value")
plt.show()
print(noise.pnoise1(1, octaves=6, persistence=0.5, lacunarity=2.0, repeat=num_points, base=49))
print(noise.pnoise1(5, octaves=2, persistence=0.8, lacunarity=5.0, repeat=100, base=57))



import noise
import numpy as np
import matplotlib.pyplot as plt

# Parameters for generating the mountain shape
num_points = 500  # Number of data points
scale = 100.0  # Adjust the scale to control the terrain roughness
octaves = 6    # Adjust the number of octaves for more detail
persistence = 0.5  # Adjust the persistence for more chaotic terrain
lacunarity = 2.0  # Adjust the lacunarity for more variation

# Generate Perlin noise values
x_values = np.linspace(0, 10, num_points)
print(x_values)
mountain_values = [noise.pnoise1(x / scale, octaves=octaves, persistence=persistence, lacunarity=lacunarity) for x in x_values]
print(mountain_values)
test = [x / scale for x in x_values]
print(test)
# Normalize the mountain values to the range [0, 1]
min_val = min(mountain_values)
max_val = max(mountain_values)
normalized_values = [(val - min_val) / (max_val - min_val) for val in mountain_values]

# Plot the mountain shape
plt.plot(x_values, normalized_values)
plt.title("1D Mountain Shape")
plt.xlabel("X")
plt.ylabel("Elevation")
plt.show()
