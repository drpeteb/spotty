import numpy as np
import matplotlib.pyplot as plt
import numpy.random as sprand




def spotty(message, figwidth, fontsize=90, scale=95, descent=0.29, border=0.2, dotratio=0.02, numdots=1000):
    """Draw a message with dots"""
    
    # Set figure height
    figheight = (1+2*border)*fontsize*(1+descent)/scale

    # Create the message figure
    fig = plt.figure(figsize=(figwidth,figheight))
    ax = fig.add_axes((0,0,1,1))

    # Write the message
    ax.text(0.01*figwidth, (border+descent)/(1+2*border+descent), "A message!", fontsize=fontsize)
    
    # Remove the axes
    ax.set_frame_on(False)
    ax.set_xticks([])
    ax.set_yticks([])
    plt.axis('off')

    # Renderer
    fig.canvas.draw()
    
    # Convert to a numpy array
    w,h = fig.canvas.get_width_height()
    immes = np.fromstring( fig.canvas.tostring_rgb(), dtype=np.uint8 )
    immes.shape = (h,w,3)
    plt.close(fig)
    
    # Convert to black and white
    immes = np.mean(immes, axis=2)    
    
    #print( immes.shape )
    #print( np.unique(immes) )
    #for row in immes:
    #    print(row)
    
    # Convert to a mask with 1 for text present
    textmask = immes!=191
    
    #print(np.sum(textmask)/textmask.size)
    
    # Dot size
    rad = dotratio*figheight
    
    # Final figure
    dotfig = plt.figure(figsize=(figwidth,figheight))
    dotax = dotfig.add_axes((0,0,1,1))
    dotax.set_xlim((0,figwidth))
    dotax.set_ylim((0,figheight))
    dotax.set_frame_on(False)
    dotax.set_xticks([])
    dotax.set_yticks([])
    plt.axis('off')

    # Dot loop
    for ii in range(numdots):      
        
        if (ii%100)==0:
            print(ii)
        
        # Generate a random dot colour and position
        col = sprand.uniform(size=3)
        pos = ( sprand.uniform(low=0.0, high=figwidth), sprand.uniform(low=0.0, high=figheight) )

        # Create figure
        fig = plt.figure(figsize=(figwidth,figheight))
        ax = fig.add_axes((0,0,1,1))
        ax.set_xlim((0,figwidth))
        ax.set_ylim((0,figheight))
        ax.set_frame_on(False)
        ax.set_xticks([])
        ax.set_yticks([])
        plt.axis('off')
        
        # Draw the circle
        circle_artist = plt.Circle(pos,rad,color=col,fill=True)
        ax.add_artist(circle_artist)

        # Renderer
        fig.canvas.draw()
        
        # Convert to a numpy array
        w,h = fig.canvas.get_width_height()
        imcirc = np.fromstring( fig.canvas.tostring_rgb(), dtype=np.uint8 )
        imcirc.shape = (h,w,3)

        # See if the dot intersects with the text
        imcirc = np.mean(imcirc, axis=2)
        #print(imcirc)        
        if np.all( np.logical_or(imcirc==191, textmask==False) ):
            
            #print(ii)
            
            # Draw the circle on the main axes
            dotax.add_artist(circle_artist)

        # Close the test figure
        plt.close(fig)

    # Renderer
    dotfig.canvas.draw()
        
    # Convert to a numpy array
    w,h = dotfig.canvas.get_width_height()
    imdot = np.fromstring( dotfig.canvas.tostring_rgb(), dtype=np.uint8 )
    imdot.shape = (h,w,3)
    
    plt.close(dotfig)
    
    return imdot







imdot = spotty('TeStInG!?', 10, numdots=5000)

# See what it looks like
#plt.figure(figsize=(figwidth,figheight))
fig = plt.figure()
plt.imshow(imdot)#, cmap='bone')
plt.axis('off')
fig.savefig('test.pdf')
#plt.axis("off");

#print(imdot)

