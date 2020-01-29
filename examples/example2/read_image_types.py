import oxygenerate as oxy
import matplotlib.pyplot as plt          # needed for viewing the images
import SimpleITK as sitk
import numpy as np

def image_show(nda, figurenum=1,  title=None, margin=0.05, dpi=40):
    #spacing = nda.GetSpacing()
    figsize = (1 + margin) * nda.shape[0] / dpi, (1 + margin) * nda.shape[1] / dpi
    #extent = (0, nda.shape[1] * spacing[1], nda.shape[0] * spacing[0], 0)
    fig = plt.figure(num=figurenum,figsize=figsize, dpi=dpi)
    ax = fig.add_axes([margin, margin, 1 - 2 * margin, 1 - 2 * margin])

    plt.set_cmap("gray")
    ax.imshow(nda)#, extent=extent, interpolation=None)

    if title:
        plt.title(title)



path = '/Users/acla148/Downloads/MCDAnew/stack_601_1201_new.nii.gz'

sitk_t1 = oxy.read_nifti_sitk(path)

info = oxy.extract_dicom_metadata_sitk(sitk_t1)

t1 = oxy.sitk_to_numpy(sitk_t1)
'''
t1 = sitk.GetArrayFromImage(sitk_t1)
print(t1.shape)
t1_temp = np.zeros((t1.shape[2],t1.shape[1],t1.shape[0]))
print(t1_temp.shape)
for i in range(0,t1.shape[0]):
  for j in range(0,t1.shape[1]):
    for k in range(0,t1.shape[2]):
        t1_temp[k,j,i] = t1[i,j,k]
'''

#t1 = t1[5,:,:]
image_show(t1[:,:,100],figurenum=1)
#print(t1)

vtk_t2 = oxy.read_nifti_vitk(path)
t2 = oxy.vtk_to_numpy(vtk_t2)
print(t2.shape)
t2 = t2[:,:,100]
image_show(t2,figurenum=2)


print(np.max(t2),np.min(t2))

print(t2)

plt.show()