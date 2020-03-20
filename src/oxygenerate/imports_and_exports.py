import vtk
from vtk.util import numpy_support
import SimpleITK as sitk
import numpy as np

"""
.. module:: imports_and_exports
   :synopsis: Provides tools to read in images, and export model compatable files.
"""

def writeExDataFile(filename, coords, mean_radius_field=None):
    """
    Write out an ex data file with the given coords.
    :param filename: Filename to write to.
    :param coords: List of coordinate lists.
    :param mean_radius_field: Additonal mean radius field to write out (optional).
    :return: None
    """
    with open(filename, 'w') as f:
        f.write(' Group name : bif_centerline_points\n')
        f.write(' #Fields={0}\n'.format(1 if mean_radius_field is None else 2))
        f.write(' 1) coordinates, coordinate, rectangular cartesian, #Components=3\n')
        f.write('\tx.  Value index= 1, #Derivatives= 0\n')
        f.write('\ty.  Value index= 2, #Derivatives= 0\n')
        f.write('\tz.  Value index= 3, #Derivatives= 0\n')
        if mean_radius_field is not None:
            f.write(' 2) radius, field, rectangular cartesian, #Components=1\n')
            f.write('\tr.  Value index= 4, #Derivatives= 0\n')
        for i in range(len(coords)):
            f.write(' Node:     %.4d\n' % (i + 1))
            f.write('   %s  %s  %s\n' % (coords[i][0], coords[i][1], coords[i][2]))
            if mean_radius_field is not None:
                f.write('   %s\n' % mean_radius_field[i])


def writeExNodeFile(filename, coords):
    """
    Write out an ex Node file with the given coords.
    :param filename: Filename to write to.
    :param coords: List of coordinate lists.
    :return: None
    """
    with open(filename, 'w') as f:
        f.write(' Group name : MAC\n')
        f.write(' #Fields=1\n')
        f.write(' 1) coordinates, coordinate, rectangular cartesian, #Components=3\n')
        f.write('   x.  Value index= 1, #Derivatives= 0\n')
        f.write('   y.  Value index= 2, #Derivatives= 0\n')
        f.write('   z.  Value index= 3, #Derivatives= 0\n')
        for i in range(len(coords)):
            f.write(' Node:         %.4d\n' % (i + 1001))
            f.write('    %s\n' % (coords[i][0]))
            f.write('    %s\n' % (coords[i][1]))
            f.write('    %s\n' % (coords[i][2]))


def writeipNodeFile(filename, coords):
    """
    Write out an ipnode file with the given coords.
    :param filename: Filename to write to.
    :param coords: List of coordinate lists.
    :return: None
    """
    with open(filename, 'w') as f:
        f.write(' CMISS Version 2.1  ipnode File Version 2\n')
        f.write(' Heading: MAC\n\n')
        f.write(' The number of nodes is [    69]:     69\n')
        f.write(' Number of coordinates [3]: 3\n')
        f.write(' Do you want prompting for different versions of nj=1 [N]? N\n')
        f.write(' Do you want prompting for different versions of nj=2 [N]? N\n')
        f.write(' Do you want prompting for different versions of nj=3 [N]? N\n')
        f.write(' The number of derivatives for coordinate 1 is [0]: 0\n')
        f.write(' The number of derivatives for coordinate 2 is [0]: 0\n')
        f.write(' The number of derivatives for coordinate 3 is [0]: 0\n\n')
        for i in range(len(coords)):
            f.write(' Node number [  %d]:   %d\n' % ((i + 1001), (i + 1001)))
            f.write(' The Xj(1) coordinate is [ 0.00000E+00]:  %s\n' % (coords[i][0]))
            f.write(' The Xj(2) coordinate is [ 0.00000E+00]:  %s\n' % (coords[i][1]))
            f.write(' The Xj(3) coordinate is [ 0.00000E+00]:  %s\n\n' % (coords[i][2]))


def load_dicom_vtk(path):
    #Load all the images in the DICOM directory
    imagevtk = vtk.vtkDICOMImageReader()
    imagevtk.SetDirectoryName(path)
    imagevtk.Update()

    return imagevtk

def load_dicom_sitk(path):

    print("Reading Dicom directory:", path)
    reader = sitk.ImageSeriesReader()

    dicom_names = reader.GetGDCMSeriesFileNames(path)
    reader.LoadPrivateTagsOn();
    reader.MetaDataDictionaryArrayUpdateOn()
    reader.SetFileNames(dicom_names)

    imagesitk = reader.Execute()

    return imagesitk


def extract_dicom_metadata_sitk(imagesitk):
    pixel_dimension = imagesitk.GetSize()
    image_position = imagesitk.GetOrigin()
    pixel_spacing = imagesitk.GetSpacing()
    image_orientation = imagesitk.GetDirection()

    print('Pixel dimensions: ', pixel_dimension)
    print('Pixel spacing: ', pixel_spacing)
    print('Image position: ', image_position)
    print('Image orientation: ', image_orientation)

    return {'pix_dim':pixel_dimension, 'pix_space':pixel_spacing, 'im_pos': image_position, 'im_orient': image_orientation }





def extract_dicom_metadata_vtk(imagevtk):

    #extract extent of data
    extent = imagevtk.GetDataExtent()
    #calculate pixel dimensions
    pixel_dimension = [extent[1] - extent[0] + 1, extent[3] - extent[2] + 1, extent[5] - extent[4] + 1]
    #Load pixel spacing
    pixel_spacing = imagevtk.GetPixelSpacing()
    #Get imaged position
    image_position = imagevtk.GetImagePositionPatient()  # Get the (DICOM) x,y,z coordinates of the first pixel in the image (upper left hand corner) of the last image processed by the DICOMParse
    #Get imaged orientation
    image_orientation = imagevtk.GetImageOrientationPatient()  # It consist of the components of the first two vectors. The third vector ne
    print('Pixel dimensions: ',pixel_dimension)
    print('Pixel spacing: ', pixel_spacing)
    print('Image position: ', image_position)
    print('Image orientation: ', image_orientation)

    return {'pix_dim':pixel_dimension, 'pix_space':pixel_spacing, 'im_pos': image_position, 'im_orient': image_orientation }

def vtk_to_numpy(imagevtk):

   # Get the 'vtkImageData' object
    image_data = imagevtk.GetOutput()
    # Get the 'vtkPointData' object from the 'vtkImageData' object
    point_data = image_data.GetPointData()
    # Ensure that only one array exists within the 'vtkPointData' object
    assert (point_data.GetNumberOfArrays() == 1)
    # Get the `vtkArray` (or whatever derived type) which is needed for the `numpy_support.vtk_to_numpy` function
    array_data = point_data.GetArray(0)

    # Convert the `vtkArray` to a NumPy array
    dicom_array = numpy_support.vtk_to_numpy(array_data)
    # Reshape the NumPy array to 3D using 'ConstPixelDims' as a 'shape'
   # extract extent of data
    extent = imagevtk.GetDataExtent()
    # calculate pixel dimensions
    pixel_dimension = [extent[1] - extent[0] + 1, extent[3] - extent[2] + 1, extent[5] - extent[4] + 1]
    dicom_array = dicom_array.reshape(pixel_dimension, order='F')
    return dicom_array


def sitk_to_numpy(imagesitk):
    img_array = sitk.GetArrayFromImage(imagesitk)# this indexes [k,j,i] for 3d images so need to restack
    if(img_array.ndim > 2): #3D need to restack
        img_temp = np.zeros((img_array.shape[2], img_array.shape[1], img_array.shape[0]))
        for i in range(0, img_array.shape[0]):
            for j in range(0, img_array.shape[1]):
                for k in range(0, img_array.shape[2]):
                    img_temp[k, j, i] = img_array[i, j, k]
        img_array = img_temp
    return img_array

def read_nifti_sitk(path):
    img = sitk.ReadImage(path)
    return img

def read_nifti_vitk(path):
    # 1. Source -Reader

    reader = vtk.vtkNIFTIImageReader()
    reader.SetFileName(path)
    reader.Update()
    size = reader.GetOutput().GetDimensions()
    center = reader.GetOutput().GetCenter()
    spacing = reader.GetOutput().GetSpacing()
    reader.SetDataSpacing(spacing)

    reader.Update()

    return reader

