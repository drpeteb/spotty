#!/usr/bin/env python3

import sys
from optparse import OptionParser
import numpy as np
import matplotlib.pyplot as plt
import numpy.random as sprand

def spotty(message, fontSize=100, borderSize=0.5, dotRadius=3, numDots=10000):
    """Draw a message with dots"""
    
    # Create a figure in which to render the text to see how big it is
    fig = plt.figure(figsize=(1,1))
    ax = fig.add_axes((0,0,1,1))

    # Write the message
    text = ax.text(0, 0, message, fontsize=fontSize)
    
    # Remove the axes
    ax.set_frame_on(False)
    ax.set_xticks([])
    ax.set_yticks([])
    plt.axis('off')

    # Fire up a renderer
    fig.canvas.draw()
    
    # Get the bounding box coordinates
    textExtent = text.get_window_extent().get_points()
    
    # Work out where to put the text
    textHeight = textExtent[1,1]-textExtent[0,1]
    textDescent = textExtent[0,1]
    textWidth = textExtent[1,0]
    assert(textExtent[0,0]==0)
    
    # Figure size
    figHeight = textHeight/fig.dpi + 2*borderSize
    figWidth = textWidth/fig.dpi + 2*borderSize
    figDescent = textDescent/fig.dpi
    
    # Close the figure
    plt.close(fig)
    
    # Create the message figure
    fig = plt.figure(figsize=(figWidth,figHeight))
    ax = fig.add_axes((0,0,1,1))

    # Write the message
    text = ax.text(borderSize/figWidth, (borderSize-figDescent)/figHeight,
                   message, fontsize=fontSize)
    
    # Remove the axes
    ax.set_frame_on(False)
    ax.set_xticks([])
    ax.set_yticks([])
    plt.axis('off')

    # Fire up a renderer
    fig.canvas.draw()
    
    # Render the figure to a numpy array
    pixWidth,pixHeight = fig.canvas.get_width_height()
    messageImage = np.fromstring( fig.canvas.tostring_rgb(), dtype=np.uint8 )
    messageImage.shape = (pixHeight,pixWidth,3)
    plt.close(fig)
    
    # Convert to black and white
    messageImage = np.mean(messageImage, axis=2)    
    
    # Convert to a mask with 1 for text present
    textMask = messageImage!=191
    
    # Create image array
    dotImage = np.ones((pixHeight,pixWidth,3))
    iPix = np.arange(pixHeight)[:,np.newaxis]
    jPix = np.arange(pixWidth)[np.newaxis,:]
    
    # Dot loop
    for dd in range(numDots):
        
        if ((dd+1)%1000)==0:
            print("Drawn {} dots.".format(dd+1))
        
        # Generate a random dot colour and position
        dotColour = sprand.uniform(low=0.0, high=1.0, size=3)
        dotPosition = ( sprand.uniform(low=0.0, high=pixHeight),
                        sprand.uniform(low=0.0, high=pixWidth) )
        
        # Work out which pixels would be coloured
        tempImage = np.zeros((pixHeight,pixWidth))
        distToDot = np.hypot(iPix-dotPosition[0], jPix-dotPosition[1])
        tempImage[distToDot<dotRadius] = 1
        
        # See if the dot intersects with the text
        if np.all(np.logical_and(tempImage, textMask)==False):
            
            # Add the dot to the image
            dotImage[distToDot<dotRadius,:] = dotColour
    
    return dotImage


def main(argv=None):
    """Parse arguments and call spotty. If argv is None, sys.argv[1:] is
    used.
    
    """
    if argv is None:
        argv = sys.argv[1:]
    
    usage = "usage: %prog message [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("-f", "--file", dest="filename", default=None,
                      help="Output file name")
    parser.add_option("-s", "--fontsize", dest="fontSize", default=100,
                      help="Font size for message")
    parser.add_option("-b", "--bordersize", dest="borderSize", default=0.5,
                      help="Border thickness in inches")
    parser.add_option("-r", "--dotradius", dest="dotRadius", default=3,
                      help="Radius of spots in pixels")
    parser.add_option("-n", "--numdots", dest="numDots", default=10000,
                      help="Number of dots")
    
    (options, args) = parser.parse_args()
    
    if len(args)==0:
        parser.error("You must supply a message to make spotty.")
    
    message = args[0]
    
    image = spotty(message,
                   fontSize=int(options.fontSize),
                   borderSize=float(options.borderSize),
                   dotRadius=float(options.dotRadius),
                   numDots=int(options.numDots))
    
    fig = plt.figure()
    plt.imshow(image)
    plt.axis('off')
    plt.show()
    if options.filename:
        fig.savefig('{}'.format(options.filename))


if __name__ == "__main__":
    main(sys.argv[1:])
