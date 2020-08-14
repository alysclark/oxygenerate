import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider, Button, TextBox,LassoSelector

def image_show(nda, figurenum=1,  title=None, margin=0.05, dpi=40):
    #spacing = nda.GetSpacing()
    figsize = (1 + margin) * nda.shape[0] / dpi, (1 + margin) * nda.shape[1] / dpi
    #extent = (0, nda.shape[1] * spacing[1], nda.shape[0] * spacing[0], 0)
    fig = plt.figure(num=figurenum,figsize=figsize, dpi=dpi)
    ax = fig.add_axes([margin, margin, 1 - 2 * margin, 1 - 2 * margin])

    plt.set_cmap("gray")
    plt.axis('off')
    ax.imshow(nda,vmin=-1200.,vmax=200.)#, extent=extent, interpolation=None)

    if title:
        plt.title(title)


def plot_stack_as_array(img,img_info):

    plt.figure()
    if(img_info['pix_dim'][2]<=10):
        for i in range(1, img_info['pix_dim'][2] + 1):
            image_show(np.transpose(img[:, :, i - 1]), figurenum=i + 1)
    else:
        print('Warning - you have tried to open too many images - I am only showing middle 10')
        mid_point =int(np.ceil(img_info['pix_dim'][2]/2.))
        img_count = 1
        for i in range(mid_point-5, mid_point+5):
            image_show(np.transpose(img[:, :, i - 1]), figurenum=img_count)
            img_count = img_count+1

    plt.show()


def plt_show():
    try:
        plt.show()
    except UnicodeDecodeError:
        plt_show()



def plot_stack_slider(img,img_info,figurenum=1,  title=None, margin=0.05, dpi=40,cmap='gray',minI = 0,maxI=1):
    lasso_list = [None] * 1000 #empty list to be determined by lasso tool
    nda = img[:,:,0]
    plt.figure()
    figsize = (1 + 4*margin) * nda.shape[0] / dpi, (1 + 4* margin) * nda.shape[1] / dpi
    fig = plt.figure(num=figurenum,figsize=figsize, dpi=dpi)
    ax = fig.add_axes([margin, margin, 1 - 2 * margin, 1 - 2 * margin])
    axcolor = 'silver'
    plt.set_cmap(cmap)
    plt.axis('off')
    ax.imshow(np.transpose(nda),vmin=minI,vmax=maxI)#, extent=extent, interpolation=None)


    if title:
        plt.title(title)

    axslider = plt.axes([2*margin,margin/2, 1-4*margin,margin/4])
    sslider = Slider(axslider, 'Slice #', 1, img_info['pix_dim'][2], valinit=1,valstep=1,valfmt='%i')

    def update_slider(val):
        slice = sslider.val
        nda =  img[:,:,int(slice-1)]
        ax.clear()
        ax.axis('off')
        ax.imshow(np.transpose(nda))#, vmin=-1200., vmax=200.)  # , extent=extent, interpolation=None)
        plt.draw()

    sslider.on_changed(update_slider)

    axreset = plt.axes([1-2.5*margin,2*margin, 2*margin , margin])
    breset = Button(axreset, 'Reset', color=axcolor, hovercolor='0.975')
    def reset(event):
        sslider.reset()

    breset.on_clicked(reset)

    axgoto = plt.axes([1-1.8*margin,4*margin, 1.5*margin , margin])
    tgoto = TextBox(axgoto, 'Go To:', color='pink', hovercolor='0.975',initial='')
    def gotoslice(val):
        if val:
            slice = int(val)
            if slice > (img_info['pix_dim'][2]):
                slice = img_info['pix_dim'][2]
            sslider.set_val(int(slice))
            nda = img[:, :, int(slice-1)]
            ax.clear()
            ax.axis('off')
            ax.imshow(np.transpose(nda))#, vmin=-1200., vmax=200.)  # , extent=extent, interpolation=None)
            plt.draw()
        tgoto.set_val('')

    tgoto.on_submit(gotoslice)

    def arrow_key_move(event):
        if event.key == 'left':
            slice = int(sslider.val)
            slice = slice - 1
            if slice < 1:
                slice = 1
            nda = img[:, :, int(slice - 1)]
            ax.clear()
            ax.axis('off')
            ax.imshow(np.transpose(nda))#, vmin=-1200., vmax=200.)  # , extent=extent,
            # interpolation=None)
            sslider.set_val(int(slice))
            plt.draw()
        elif event.key == 'right':
            slice = int(sslider.val)
            slice = slice + 1
            if slice > img_info['pix_dim'][2]:
                slice = img_info['pix_dim'][2]
            nda = img[:, :, int(slice - 1)]
            ax.clear()
            ax.axis('off')
            ax.imshow(np.transpose(nda))#, vmin=-1200., vmax=200.)  # , extent=extent,
            # interpolation=None)
            sslider.set_val(int(slice))
            plt.draw()
        else:
            pass

    kmove = fig.canvas.mpl_connect('key_release_event', arrow_key_move)


    def onselect(verts,lasso_list):
        #print(len(verts),lasso_list)
        lasso_list[0:len(verts)]=verts
        lasso_list[len(verts):1000]=[None]*(1000-len(verts))
        #print(lasso_list[0:len(verts)])

        num_verts = len(verts)


    def enter_key_hit(event,lasso_list):
        res = []
        res = np.asarray([i for i in lasso_list if i])
        if event.key == 'enter':
            #print(res[:,0])
            ax.plot(res[:,0], res[:,1], 'o',markersize=2)
            #print(lasso_list)
        else:
            pass




    lasso = LassoSelector(ax, lambda event: onselect(event,lasso_list))
    cid = fig.canvas.mpl_connect('key_release_event',lambda event: enter_key_hit(event,lasso_list))



    plt_show()