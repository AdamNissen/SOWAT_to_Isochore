# -*- coding: utf-8 -*-
"""
Script for plotting isochores for my MSc. thesis. The only things that could 
break are external changes made to the dataset path (found line 17), and to the 
internal columns of the data.

This can be a good reference for remembering a couple things. First off, plotting
subplots with matplot lib, second using pandas.query(). I think everything is 
relatively concise.

Note, this spits out a plate with four colourmaps, one for each sample
"""

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


def intersection_divisor(line1, line2):
    # This is modified from stackoverflow code because I don't know linear algebra.
    # The code was sepparated into two functions so that det could be evaluated externally
    # to make everything work in pandas
    # https://stackoverflow.com/questions/20677795/how-do-i-compute-the-intersection-point-of-two-lines
    
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    return div



def line_intersection(line1, line2, div):
    #See comment on intersection_divisor    
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    d = (det(*line1), det(*line2))

    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

#Actual data
data = pd.read_excel(io ="Output/all_isochores.xlsx", sheet_name = 'isochores')
data['P (mPa)'] = data['P (bar)']/10 #convert bar to mpa to align with established figure practices
samples = list(data['Sample'].unique())

#Establishing the figure and axes (or subplots) of the figure
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2, figsize = (15, 12))
axs = [ax1, ax2, ax3, ax4]


#Building a list full of colourmap functions to be used later (~line 72)
cmaps = [plt.cm.Purples,
         plt.cm.Reds,
         plt.cm.Greens,
         plt.cm.Oranges]

titles = ('a', 'b', 'c', 'd')
#Making four subplots
for i in range(4):
    
    ax = axs[i]
    
    #plotting background tielines
    ax.plot([237, 338, 670, 708, 746], [165, 147, 416, 465, 577], color = 'k', linestyle = '-', linewidth = 2) 
    ax.plot([263, 338], [30 ,147], color = 'k', linestyle = '-', linewidth = 2)
    ax.plot([676,670],[30, 416], color = 'k', linestyle = '-', linewidth = 2)
    ax.plot([822, 708],[30, 465], color = 'k', linestyle = '-', linewidth = 2)
    
    #Plotting labels
    ax.text(0.18, 0.45, 'Spodumene', transform = ax.transAxes)
    ax.text(0.05, 0.24, 'Eucryptite', transform = ax.transAxes)
    ax.text(0.4, 0.3, 'Petalite', transform = ax.transAxes)
    ax.text(0.72, 0.3, 'β-Spodumene', rotation = 285, transform = ax.transAxes)
    ax.text(0.85, 0.85, 'Virgilite', transform = ax.transAxes)

    
    #EKL peak metamorphism
    ax.fill_between([200, 1000], [400, 400], [350, 350], alpha = 0.3)
    plt.figtext(0.005, 0.71, 'EK/SMB peak metamorphism', size = 'small', transform = ax.transAxes)
    
    #BLP PT estimates from Kontak
    ax.fill_between([550,600], [400, 400], [350, 350], alpha = 0.6)
    
    #LCT pegmatite formation PT
    ax.fill_between([350, 550], [275, 275], [325, 325], alpha = 0.6)
    ax.text(355, 280, 'LCT pegmatite PT')
    
    #Thermal resetting minimum lines and text
    ax.axvline(x = 400, linestyle = "--", linewidth = 1.5)
    ax.axvline(x = 600, linestyle = "--", linewidth = 1.5)
    ax.text(405, 10, 'Onset of Ar resetting', rotation = 90, size = 'small')
    ax.text(605, 10, 'Onset of Sr re-equilibration', rotation = 90, size = 'small')


    #Plotting sample information
    sample = samples[i]

    #Finding the number of assemblages for colourmapping, the +3 is specific to the 
    #chosen colourmap because early segments of the colour spectrum don't show
    #up well, so we skip the first three segments
    n = len(data.query('Sample == @sample')# grouping by sample
              .Assemblage# calling the Assemblage column
              .unique()# returning only unique values
              )+3
    
    #Selecting a colourmap from the previously established list (~line 30) to 
    #establish the colours for each subfigure. A full colours function would look
    # like: colours = plt.cm.Purples(np.linspace(0,1,n))
    colours = cmaps[i](np.linspace(0, 1, n))
    
    #A counter to dictate the colour of each assemblage from the "colours" map
    counter = 3
    
    #So I've just discovered pandas.query, and I'm plotting the lines with it
    for assemblage in (data.query('Sample == @sample')# grouping by sample
              .Assemblage# calling the Assemblage column
              .unique()# returning only unique values
              ):# completing the chain and for line
    #Plotting the lines    
        # ax.plot(data.query('Sample == @sample and Assemblage == @assemblage and Th_type == "liquid"')['T (C)'], Attempting to remove lines for a less processed datasheet
        #         data.query('Sample == @sample and Assemblage == @assemblage and Th_type == "liquid"')['P (mPa)'],
        ax.plot(data.query('Sample == @sample and Assemblage == @assemblage')['T (C)'],
                data.query('Sample == @sample and Assemblage == @assemblage')['P (mPa)'],
      
                alpha = 0.7, color = colours[counter]) 
    
    #I am temporarily removing the difference between "outliers" and "non-outliers" because I think it is irrelivent
    #     ax.plot(data.query('Sample == @sample and Assemblage == @assemblage and Th_type == "liquid" and Outlier == False')['T (C)'],
    #             data.query('Sample == @sample and Assemblage == @assemblage and Th_type == "liquid" and Outlier == False')['P (mPa)'],
    #             alpha = 0.7, color = colours[counter])    
    # #plotting outliers with a dashed line     
    #     ax.plot(data.query('Sample == @sample and Assemblage == @assemblage and Th_type == "liquid" and Outlier == True')['T (C)'],
    #             data.query('Sample == @sample and Assemblage == @assemblage and Th_type == "liquid" and Outlier == True')['P (mPa)'],
    #             alpha = 0.7, linestyle = "--", color = colours[counter])
        
        #advancing the counter so each assemblage has unique colours
        counter+=1
    
    #Highlighting the spodumene intercept
    trapping_PT = pd.DataFrame()
    
    #Finding coordinates for the end and beginning of each isochore    
    for code in data.query('Sample == @sample').Inclusion_code.unique():
        newline = pd.DataFrame()
        newline['isochore'] = [code]
        #Pulling end coordinates of each isochore into a dictionary, these lines are messy, but they work
        newline['x0'] = list(data.query('Sample == @sample and Inclusion_code == @code').nsmallest(1, 'P (mPa)')['T (C)']) #Querying to limit the dataframe, nsmallest() gets the minimum. The list bits are just to extraxt single values
        newline['y0'] = list(data.query('Sample == @sample and Inclusion_code == @code').nsmallest(1, 'P (mPa)')['P (mPa)'])
        newline['x1'] = list(data.query('Sample == @sample and Inclusion_code == @code').nlargest(1, 'P (mPa)')['T (C)'])
        newline['y1'] = list(data.query('Sample == @sample and Inclusion_code == @code').nlargest(1, 'P (mPa)')['P (mPa)'])
        
        trapping_PT = pd.concat([trapping_PT, newline], ignore_index = True)
    
    
    #Calculating the intercept of lines in the form of
    #     ||A1 A2| A1-A2|
    #     ||B1 B2| B1-B2|
    # P = ---------------
    #     |A1-A2   B1-B2|
    #Yay linear algebra, maybe I should've taken more math courses...
    #I may need to do some work to make the segments of line segments work, but we will see

    trapping_PT['eu_div'] = intersection_divisor(((trapping_PT['x0'], trapping_PT['y0']), (trapping_PT['x1'], trapping_PT['y1'])), ((237, 165),(338, 147)))
    trapping_PT['pe_div'] = intersection_divisor(((trapping_PT['x0'], trapping_PT['y0']), (trapping_PT['x1'], trapping_PT['y1'])), ((338, 147),(670, 416)))
    
    trapping_PT['eu_x'], trapping_PT['eu_y'] = line_intersection(((trapping_PT['x0'], trapping_PT['y0']), (trapping_PT['x1'], trapping_PT['y1'])), ((237, 165),(338, 147)), trapping_PT['eu_div'])
    trapping_PT['pe_x'], trapping_PT['pe_y'] = line_intersection(((trapping_PT['x0'], trapping_PT['y0']), (trapping_PT['x1'], trapping_PT['y1'])), ((338, 147),(670, 416)), trapping_PT['pe_div'])
    
    eu_min = trapping_PT['eu_x'].min()
    eu_max = trapping_PT['eu_x'].max()
    pe_min = trapping_PT['pe_x'].min()
    pe_max = trapping_PT['pe_x'].max()
    
    #intersection @ (338, 147)
    
    # Setting a minimum x point for the highlighted spodumene boundary. I am not
    # considering isochore groups that don't cross the eucryptite-spodumene boundary
    # as that doesn't describe any of my data. I could some nested if else 
    # rules if I need to consider higher temp isochores only.
    min_point = (eu_min, list(trapping_PT.query('eu_x == @eu_min')['eu_y'])[0])

    
    if pe_max > 670:
        ax.plot([min_point[0], 338, 670, 708, 746], [min_point[1], 147, 416, 465, 577], color = 'deepskyblue', linestyle = '-', linewidth = 5) 

    elif 338 < pe_max < 670:
        max_point = (pe_max, list(trapping_PT.query('pe_x == @pe_max')['pe_y'])[0])
        ax.plot([min_point[0], 338, max_point[0]], [min_point[1], 147, max_point[1]], color = 'deepskyblue', linestyle = '-', linewidth = 5) 

    else:
        max_point = (eu_max, list(trapping_PT.query('eu_x == @eu_max')['eu_y'])[0])
        ax.plot([min_point[0], max_point[0]], [min_point[1], max_point[1]], color = 'deepskyblue', linestyle = '-', linewidth = 5) 
        
            
    # Defining subplot features
    ax.set_title(titles[i], loc = 'left', size = 'xx-large')
    ax.text(750, 10, "Sample "+sample, size = 'large')
    # ax.set_title(sample)
    ax.set_xlim(200, 900)
    #ax.set_xlim(0, 900)
    ax.set_ylim(0, 500)

#Setting superlabes for the x and y axis that apply to all subplots
fig.supxlabel('Temperature (°C)')
fig.supylabel('Pressure (mPa)')
    
#plotting and printing
plt.tight_layout()
plt.savefig("Output\individual_colours.jpg", dpi = 300)
plt.savefig("Output\individual_colours.svg", dpi = 300) #saving an svg for manual editing if necessary