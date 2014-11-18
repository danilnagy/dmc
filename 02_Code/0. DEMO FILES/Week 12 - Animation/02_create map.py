import math
import sys
import shapefile
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from mpl_toolkits.basemap import Basemap

#set working directory
workingDirectory = "C:\\Users\\Danil\\Documents\\Teaching\\DMC\\Fall, 2014\\Week 12 - Python Viz\\class demo\\"

#setup plot
plt.close('all') 
fig = plt.figure(figsize=(11.7,8.3))
plt.subplots_adjust(left=0.05,right=0.95,top=0.90,bottom=0.05,wspace=0.15,hspace=0.05)
ax = plt.subplot(111)

#setup map bounds in lat/lon
x1 = 113.65
x2 = 114.65
y1 = 22.1
y2 = 22.85

#use basemap library to setup projection system, bounds, and draw boundaries and grid lines
m = Basemap(resolution='i',projection='merc', llcrnrlat=y1,urcrnrlat=y2,llcrnrlon=x1,urcrnrlon=x2,lat_ts=(y1+y2)/2)
#m.drawcountries(linewidth=0.5)
#m.drawcoastlines(linewidth=0.5)
m.drawparallels(np.arange(y1,y2,.2),labels=[1,0,0,0],color='black',dashes=[1,1],labelstyle='+/-',linewidth=0.1) # draw parallels
m.drawmeridians(np.arange(x1,x2,.2),labels=[0,0,0,1],color='black',dashes=[1,1],labelstyle='+/-',linewidth=0.1) # draw meridians

#use shapefile library to read in PRD water boundary shapefile
boundary = shapefile.Reader(workingDirectory + "data\\PRD_waterBoundary_water")

#extract shape and record data from shapefile
shapes = boundary.shapes()
records = boundary.records()

#iterate through shapes and records
for record, shape in zip(records,shapes):
    
    #extract lat/lon data and project to map units using basemap library
    lons,lats = zip(*shape.points)
    data = np.array(m(lons, lats)).T
 
    #test whether shape is multipart
    if len(shape.parts) == 1:
        segs = [data,]
    #if multipart, iterate through each part and add to segments array
    else:
        segs = []
        for i in range(1,len(shape.parts)):
            index = shape.parts[i-1]
            index2 = shape.parts[i]
            segs.append(data[index:index2])
        segs.append(data[index2:])
 
    #add segments to collection of lines
    lines = LineCollection(segs,antialiaseds=(1,))
    
    #set line properties
    lines.set_edgecolors('k')
    lines.set_linewidth(0.3)
    
    #add line collection to plot
    ax.add_collection(lines)


#import data set from previous script
import pickle
checkins = pickle.load( open( workingDirectory + "data\\checkins.p", "rb" ) )

#create variables for scatter and text label, and specify initial parameters (including color and transparency)
scat = ax.scatter(0,0, c='r', edgecolor ='r', lw=.01, alpha=.03, s = 50)  
txt = ax.text(1000, 1000, '')

#variable for total time steps
numTimes = len(checkins)

#create update function to be run at each ste of animation
def update(frame_number):
    
    #smoothing parameter specifies number of times to be integrated into each frame of the animation
    #(higher numbers give smoother animation but take longer to render)
    smoothing = 9
    
    #create long list of all checkins for chosen time steps
    a = []
    for i in range(smoothing):
        a += checkins[(frame_number+i)%numTimes].values()
    
    #update location and sizes of scatter plot points based on current data
    #(most parameters can be updated, including location, size, and color)
    scat.set_offsets( [ m(float(i[1]), float(i[0])) for i in a ] )
    scat._sizes = [ ((i[2] * 100.0) ** .75 ) for i in a ] 
    
    #update text label with hour and minute
    hour = int(math.floor(frame_number/60))
    minute = int(math.floor(frame_number%60)) 
    txt.set_text(str(hour) + ':' + str(minute))
    
    #save frame to file
    plt.savefig(workingDirectory + "animation\\" + str(frame_number) + '.png')
    
    #quit script after the last time step
    if frame_number > numTimes - 2:
        sys.exit()

#import animation library
from  matplotlib.animation import FuncAnimation

#run animation, specifying target plot, update function, and length of each frame
animation = FuncAnimation(fig, update, interval=50)

#show plot                                       
plt.show()
