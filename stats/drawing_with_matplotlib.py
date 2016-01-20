#!/usr/bin/env python
import numpy as np
#import matplotlib.pyplot as plt
import pylab as plt
# Read the documentation to learn about all the options for styles, etc:
# http://matplotlib.org/api/pyplot_api.html
# http://matplotlib.org/users/pyplot_tutorial.html
from matplotlib.backends.backend_pdf import PdfPages
pdf = PdfPages('drawing_with_matplotlib.pdf') # save all plots in one pdf file
# Take a look at a module called DASHI:
# http://www.ifh.de/~middell/dashi/
# It tries to add more of the functionality we are used to in HEP. 

Nentries=1000

'''
 First, draw a histogram like a TGraph (scatter plot): with values of x and y
'''
x=np.arange(0,10)
y=[14,12,20,13,18,26,10,20,15,11]

# marker= squares (s), circle(o), triange (^)
# linestyle='steps' to look like a histogram
plt.plot(x, y, linewidth=2.0, linestyle='-', color='black', marker='o', markerfacecolor='r', markersize=5.2)

plt.title("Hello world")
plt.xlabel("x axis [years]")
plt.ylabel("y axis [units]")
#plt.ylim(0.)
plt.grid()
#plt.show()
#plt.savefig("matplotlib1.png")
pdf.savefig() # page 1
'''
 This can easily be plotted as TGraphError, too:
'''
plt.figure() # new figure
yerr=[0.10*i for i in y]
print yerr
plt.errorbar(x, y, yerr, marker='o', markerfacecolor='black', markersize=5.2)
#plt.savefig("matplotlib2.png")
pdf.savefig() # page 2

'''
 Or even be plotted as TGraphAsymmetricError. 
 Just make two arrays for yerr, the first one is the lower error, the second the upper error.
'''
plt.figure() # new figure
yerr_up=[0.05*i for i in y]
yerr_lo=[0.03*i for i in y]
print yerr_up, yerr_lo
plt.errorbar(x, y, [yerr_lo,yerr_up], linestyle='None', marker='o', markerfacecolor='blue', markersize=5.2)
#plt.savefig("matplotlib3.png")
pdf.savefig() # page 3
'''
 Finally a usual histogram, specifying how many bins:
'''
plt.figure() # create new figure
x = 200 + 50. * np.random.randn(Nentries)
# We could fill x inside a loop, just adding numbers to the array, 
# but we really only need an array of values.
n, bins, patches = plt.hist(x, 50, normed=1, range=[0,400], facecolor='g', alpha=0.75, histtype='stepfilled')
# alpha is the transparency of the data points (patch)
plt.axis([0, 400, 0, 0.01]) # sets the ranges for the x and y axis. This command overrides the range inside hist
#plt.savefig("matplotlib4.png")
pdf.savefig() # page 4
'''
 And now overlay
'''
plt.figure() # new figure
z=100 + 80. *  np.random.randn(Nentries)
#hist(x, bins, range, normed, weights, cumulative, bottom, histtype, align, orientation, rwidth, log, color, label, **kwargs)
n, bins, patches = plt.hist([x,z], 50, normed=1, label=['x','z'], color=['g','b'], histtype='step')
# Be careful, of you have two different plt.hist for x and z, then the bins will not be the same!
plt.yscale('log') # make it log scale!
plt.axis([0, 400, 0, 0.01])
# Add a legend:
plt.legend( ('x','z') , loc='upper right', frameon=False)
# If you want simple lines instead of boxes for the legend handles, you have to use plt.plot(a,x,'g-') and plt.plot(a,z,'b:') instead of plot.hist(). Where a are the bins and x and z are the patches from the above comands. 
#plt.savefig("matplotlib5.png")
pdf.savefig() # page 5

'''
 What about stacking and plotting data as points with error bars?
 Need version 1.3 of matplotlib for stacked=True to work in plt.hist!
'''
# Another way: http://stackoverflow.com/questions/18449602/matplotlib-creating-stacked-histogram-from-three-unequal-length-arrays
#http://matplotlib.org/examples/pylab_examples/stackplot_demo.html
plt.figure() # new figure
#n, bins, patches = plt.hist([x,z], 50, normed=1, color=['r','gray'], label='stacked', histtype='stepfilled')
nbins=10
ncont, bins, patches = plt.hist([x,z], nbins, range=[-100,400], label=['x','z'], color=['r','gray'], histtype='stepfilled', stacked=True)
print 'n counts', ncont
print 'bins ', bins
print 'Be careful if you use range=[] inside hist, that there are no overflow or underflow bins!'
plt.title("Note that z is on top of x")
plt.xlabel("axis name [units]")
plt.ylabel("# of events")
# Trick from: http://matplotlib.org/1.2.1/examples/api/histogram_demo.html
bincenters = 0.5*(bins[1:]+bins[:-1])
# Let's create some data that mimics the two histograms
data1 = 100 + 80. * np.random.randn(Nentries)
data2 = 200 + 50. * np.random.randn(Nentries)
# Read: http://stackoverflow.com/questions/9236926/concatenating-two-one-dimensional-numpy-arrays
data = np.concatenate([data1,data2])
#data_weights_zero=np.zeros(20000) # set weights to zero
# Create a histogram (doesn't plot it) for the data:
data_counts, data_bins = np.histogram(data, nbins)
# np.histogram returns the bin edges, so there will be 50 probability
# density values in n, 51 bin edges in bins and 50 patches.  To get
# everything lined up, we'll use the bin centers from the previous histogram.
# Remove last bin:
#data_bins= np.delete(data_bins,len(data_bins)-1)
# Add a count of zero in first bin:
#data_counts=np.insert(data_counts,0,0.0)

# Plot data as points (no errorbars):
#plt.plot(bincenters, data_counts, linewidth=0.0, color='black', marker='o', markerfacecolor='black', markersize=5.2)

# Plot data as points and Poisson errorbars:
# http://www.pp.rhul.ac.uk/~cowan/atlas/ErrorBars.pdf Section 4
from scipy import stats
alpha=0.158655 # such that alpha=beta and 1-alpha-beta=0.6827
dataerr_up=[0.5*(stats.chi2(2*(n+1))).ppf(1-alpha)-n for n in data_counts]
dataerr_lo=[n-0.5*(stats.chi2(2*n)).ppf(alpha) for n in data_counts]
# This is the same as using in ROOT: TMath.ChisquareQuantile(1-alpha,2*(n+1))
# Plot data as points with binomial errorbars:
#dataerr_up=[0.5*(stats.f().ppf(1-alpha)-n for n in data_counts]
#dataerr_lo=
# Plot data as points with sqrt(n) errors (as ROOT does it):
dataerr_lo=dataerr_up=[np.sqrt(n) for n in data_counts if n>0]
#dataerr_lo=[np.sqrt(n) for n in data_counts if n>0]
plt.errorbar(bincenters, data_counts, [dataerr_lo,dataerr_up], linestyle='None', marker='o', markerfacecolor='black', markersize=5.2, ecolor='black', elinewidth=1.3, barsabove=True, label='Data')
# Now write a legend. plt.gca() = get current axes
handles, labels = plt.gca().get_legend_handles_labels()
# reverse the order of legend:
plt.legend(handles[::-1], labels[::-1],loc='upper left', frameon=False, numpoints=1)
#plt.xlim([-200,400]) ; # plt.ylim([0.,500.])
#plt.savefig("matplotlib6.png")
pdf.savefig() # page 6

'''
Now with inset for ratio
'''
# Read: http://matplotlib.org/examples/pylab_examples/subplots_demo.html
# http://matplotlib.org/users/gridspec.html
#f, (ax1,ax2) = plt.subplots(2, sharex=True)
import matplotlib.gridspec as gridspec
gs = gridspec.GridSpec(2, 1, height_ratios=[4,1]) # 1 column, 2 rows, 1st row is 4 times bigger
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1], sharex=ax1) # important that they share the same X axis!
# Now, ax1 is the first subplot
ax1.hist([x,z], nbins, range=[-100,400], label=['x','z'], color=['r','gray'], histtype='stepfilled', stacked=True)
ax1.errorbar(bincenters,data_counts,[dataerr_lo,dataerr_up], linestyle='None', marker='o', markerfacecolor='black', markersize=5.2, ecolor='black', elinewidth=1.3, barsabove=True, label='Data')
ax1.set_title('Sharing X axis')
# Now let's calculate the ratio for ax2:
MC_counts=ncont[1] # the last array in ncont is the sum of all bins (because stacked=True)
print 'MC counts', MC_counts
data_MC_ratio=[float(data_counts[i])/float(MC_counts[i]) for i in range(0,len(bincenters))]
data_MC_ratio_err=np.zeros(len(MC_counts))
ax2.errorbar(bincenters,data_MC_ratio,[data_MC_ratio_err,data_MC_ratio_err], linestyle='None', marker='o', markerfacecolor='black', markersize=5.2, ecolor='black', elinewidth=1.3, barsabove=True)
ax2.set_ylim(0.,2.)
ax2.grid()
# Draw horizontal line at 1: 
ax2.plot([-200, 400], [1.0, 1.0], 'k-', lw=2)
plt.setp(ax1.get_xticklabels(), visible=False)
plt.subplots_adjust(hspace=0.05)
#plt.savefig("matplotlib7.png")
pdf.savefig() # page 7
pdf.close()