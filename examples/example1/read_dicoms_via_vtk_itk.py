import oxygenerate as oxy
import matplotlib.pyplot as plt          # needed for viewing the images
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

vtk_ct_images = oxy.load_dicom_vtk('../sample_inputs/CTPA')
vtk_ct_info = oxy.extract_dicom_metadata_vtk(vtk_ct_images)

sitk_ct_images = oxy.load_dicom_sitk('../sample_inputs/CTPA')
sitk_ct_info = oxy.extract_dicom_metadata_sitk(sitk_ct_images)

numpy_images_from_vtk = oxy.vtk_to_numpy(vtk_ct_images)
numpy_images_from_itk = oxy.sitk_to_numpy(sitk_ct_images,sitk_ct_info)

#print(np.size(numpy_images))
plt.figure()
for i in range(1,vtk_ct_info['pix_dim'][2]+1):
    image_show(np.transpose(numpy_images_from_vtk[:,:,i-1]),figurenum = i )
    image_show(np.transpose(numpy_images_from_itk[ :,:, i-1]), figurenum = i+3)

plt.show()