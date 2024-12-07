from pyanten.Utility import frequencyToWavelength

def minimumRange(frequency: float):
  r""" Minimum recommended distance for near-field antenna measurements in meters

  Parameters
  ----------
  frequency : float
      frequency of interest in Hertz [Hz]

  Notes
  -----
  Standard suggests to choose between 3 or 5 wavelength.
  In order to ensure copuling effect, 5 wavelength distance is choosen and implemented.

  .. [1] IEEE 1720-2012 Recommended Practice for Near-Field Antenna Measurements, Section 5.3.1.4, Page 27.

  Formula
  -------
  .. math::
      R_{nf} = 5\times\lambda = 5\times c_0/f
  """
  return 5*frequencyToWavelength(frequency)