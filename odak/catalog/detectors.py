from odak import np
import odak.catalog
from odak.wave import calculate_phase,calculate_amplitude,calculate_intensity
from odak.raytracing.primitives import define_plane,bring_plane_to_origin
from odak.raytracing.boundary import intersect_w_surface

class plane_detector():
    """
    A class to represent a plane detector. This is generally useful in raytracing and wave calculations.
    """
    def __init__(self,field=None,resolution=[1000,1000],shape=[10.,10.],center=[0.,0.,0.],angles=[0.,0.,0.]):
        """
        Class to represent a simple planar detector.

        Parameters
        ----------
        field       : ndarray
                      Initial field to be loaded.
        resolution  : list
                      Resolution of the detector.
        shape       : list
                      Shape of the detector.
        center      : list
                      Center of the detector.
        angles      : list
                      Rotation angles of the detector.
        """
        self.settings   = {
                           'resolution'    : resolution,
                           'center'        : center,
                           'angles'        : angles,
                           'rotation mode' : 'XYZ',
                           'shape'         : shape,
                          }
        self.plane      = define_plane(
                                       self.settings['center'],
                                       angles=self.settings['angles']
                                      )
        if type(field) == type(None):
            self.field = np.zeros(
                                  (
                                   self.settings['resolution'][0],
                                   self.settings['resolution'][1],
                                   1
                                  ),
                                  dtype=np.complex64
                                  )
    def get_field(self):
        """
        A definition to return the field measured on the detector.

        Returns
        ----------
        field       : ndarray
                      A copy of the field measured by the detector.
        """
        return np.copy(self.field)

    def get_intensity(self):
        """
        A definition to return the intensity of the field.

        Returns
        ---------
        intensity   : ndarray
                      Intensity of the field measured by the detector.
        """
        intensity = wave.calculate_intensity(self.field)
        return intensity

    def get_amplitude(self):
        """
        A definition to return the amplitude of the field.

        Returns
        ---------
        amplitude   : ndarray
                      Amplitude of the field measured by the detector.
        """
        amplitude = wave.calculate_amplitude(self.field)
        return amplitude

    def get_phase(self):
        """
        A definition to return the phase of the field.

        Returns
        ---------
        phase       : ndarray
                      Phase of the field measured by the detector.
        """
        phase = wave.calculate_phase(self.field)
        return phase

    def raytrace(self,ray,field=1,channel=0):
        """
        A definition to calculate the intersection between given ray(s) and the detector. If a ray contributes to the detector, field will be taken into account in calculating the field over the planar detector.
 
        Parameters
        ----------
        ray          : ndarray
                       Ray(s) to be intersected.
        field        : ndarray
                       Field(s) to be used for calculating contribution of rays to the detector.
        channel      : list
                       Which color channel to contribute to in the detector plane. Default is zero. One can use a list to select multiple channels separately.
 
        Returns
        ----------
        normal       : ndarray
                       Normal for each intersection point.
        distance     : ndarray
                       Distance for each ray.
        """
        normal,distance = intersect_w_surface(ray,self.plane)
        points          = bring_plane_to_origin(
                                                normal[:,0],
                                                self.plane,
                                                shape=self.settings["shape"],
                                                center=self.settings["center"],
                                                angles=self.settings["angles"],
                                                mode=self.settings["rotation mode"]
                                               )
        if points.shape[0] == 3:
            points = points.reshape((1,3))
        # This could improve with a bilinear filter. Basically removing int with a filter.
        detector_ids = np.array(
                                [
                                 (points[:,0]+self.settings["shape"][0]/2.)/self.settings["shape"][0]*self.settings["resolution"][0]+1,
                                 (points[:,1]+self.settings["shape"][1]/2.)/self.settings["shape"][1]*self.settings["resolution"][1]+1
                                ],
                                dtype=int
                               )
        detector_ids[0,:] = (detector_ids[0,:]>=1)*detector_ids[0,:]
        detector_ids[1,:] = (detector_ids[1,:]>=1)*detector_ids[1,:]
        detector_ids[0,:] = (detector_ids[0,:]<self.settings["resolution"][0]+1)*detector_ids[0,:]
        detector_ids[1,:] = (detector_ids[1,:]<self.settings["resolution"][1]+1)*detector_ids[1,:]
        cache             = np.zeros(
                                     (
                                      self.settings["resolution"][0]+1,
                                      self.settings["resolution"][1]+1,
                                      self.field.shape[2]
                                     ),
                                     dtype=np.complex64
                                    )
        cache[
              detector_ids[0],
              detector_ids[1],
              channel
             ]           += field
        self.field       += cache[1::,1::,:]
        return normal,distance
