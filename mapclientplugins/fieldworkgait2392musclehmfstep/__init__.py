'''
MAP Client Plugin
'''

__version__ = '0.1.1'
__author__ = 'Ju Zhang'
__stepname__ = 'Fieldwork Gait2392 Muscle HMF'
__location__ = 'https://github.com/mapclient-plugins/fieldworkgait2392musclehmfstep/archive/v0.1.0.zip'

# import class that derives itself from the step mountpoint.
from mapclientplugins.fieldworkgait2392musclehmfstep import step

# Import the resource file when the module is loaded,
# this enables the framework to use the step icon.
from . import resources_rc
