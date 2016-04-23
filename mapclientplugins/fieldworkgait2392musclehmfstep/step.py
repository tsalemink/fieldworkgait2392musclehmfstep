
'''
MAP Client Plugin Step
'''
import json

from PySide import QtGui

from mapclient.mountpoints.workflowstep import WorkflowStepMountPoint
from mapclientplugins.fieldworkgait2392musclehmfstep.configuredialog import ConfigureDialog
from mapclientplugins.fieldworkgait2392musclehmfstep.gait2392musclecusthmf import gait2392MuscleCustomiser


class FieldworkGait2392MuscleHMFStep(WorkflowStepMountPoint):
    '''
    Skeleton step which is intended to be a helpful starting point
    for new steps.
    '''

    def __init__(self, location):
        super(FieldworkGait2392MuscleHMFStep, self).__init__('Fieldwork Gait2392 Muscle HMF', location)
        self._configured = False # A step cannot be executed until it has been configured.
        self._category = 'OpenSim'
        # Add any other initialisation code here:
        self._icon =  QtGui.QImage(':/fieldworkgait2392musclehmfstep/images/morphometric.png')
        # Ports:
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#gias-lowerlimb'))
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#osimmodel'))
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#provides',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#osimmodel'))
        # Port data:
        self._portData0 = None # http://physiomeproject.org/workflow/1.0/rdf-schema#gias-lowerlimb
        self._portData1 = None # http://physiomeproject.org/workflow/1.0/rdf-schema#osimmodel
        self._portData2 = None # http://physiomeproject.org/workflow/1.0/rdf-schema#osimmodel
        # Config:
        self._config = {}
        self._config['identifier'] = ''
        self._config['osim_output_dir'] = './gait2392_simbody_custom.osim'
        self._config['in_unit'] = 'mm'
        self._config['out_unit'] = 'm'
        self._config['write_osim_file'] = True
        self._config['side'] = 'left'
        self._config['static_vas'] = True

        self._g2392_muscle_hmf = gait2392MuscleCustomiser(self._config)

    def execute(self):
        '''
        Add your code here that will kick off the execution of the step.
        Make sure you call the _doneExecution() method when finished.  This method
        may be connected up to a button in a widget for example.
        '''
        # Put your execute step code here before calling the '_doneExecution' method.
        self._g2392_muscle_hmf.config = self._config
        self._g2392_muscle_hmf.customise()
        self._doneExecution()

    def setPortData(self, index, dataIn):
        '''
        Add your code here that will set the appropriate objects for this step.
        The index is the index of the port in the port list.  If there is only one
        uses port for this step then the index can be ignored.
        '''
        if index == 0:
            self._g2392_muscle_hmf.ll = dataIn # http://physiomeproject.org/workflow/1.0/rdf-schema#gias-lowerlimb
        elif index == 1:
            self._g2392_muscle_hmf.set_osim_model(dataIn) # http://physiomeproject.org/workflow/1.0/rdf-schema#osimmodel

    def getPortData(self, index):
        '''
        Add your code here that will return the appropriate objects for this step.
        The index is the index of the port in the port list.  If there is only one
        provides port for this step then the index can be ignored.
        '''
        return self._g2392_muscle_hmf.gias_osimmodel._model # http://physiomeproject.org/workflow/1.0/rdf-schema#osimmodel

    def configure(self):
        '''
        This function will be called when the configure icon on the step is
        clicked.  It is appropriate to display a configuration dialog at this
        time.  If the conditions for the configuration of this step are complete
        then set:
            self._configured = True
        '''
        dlg = ConfigureDialog()
        dlg.identifierOccursCount = self._identifierOccursCount
        dlg.setConfig(self._config)
        dlg.validate()
        dlg.setModal(True)

        if dlg.exec_():
            self._config = dlg.getConfig()

        self._configured = dlg.validate()
        self._configuredObserver()

    def getIdentifier(self):
        '''
        The identifier is a string that must be unique within a workflow.
        '''
        return self._config['identifier']

    def setIdentifier(self, identifier):
        '''
        The framework will set the identifier for this step when it is loaded.
        '''
        self._config['identifier'] = identifier

    def serialize(self):
        '''
        Add code to serialize this step to string.  This method should
        implement the opposite of 'deserialize'.
        '''
        return json.dumps(self._config, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def deserialize(self, string):
        '''
        Add code to deserialize this step from string.  This method should
        implement the opposite of 'serialize'.
        '''
        self._config.update(json.loads(string))

        d = ConfigureDialog()
        d.identifierOccursCount = self._identifierOccursCount
        d.setConfig(self._config)
        self._configured = d.validate()


