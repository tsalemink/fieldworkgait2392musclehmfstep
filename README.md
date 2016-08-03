Fieldwork Gait2392 Muscle HMF Step
==================================
MAP Client plugin for customising the OpenSim Gait2392 model's muscle path points using a GIAS2 lowerlimb model (see fieldworklowerlimb2sidegenerationstep).
Path point customisation is applied to the following bodies: pelvis, femurs, tibias.

For each body, the default Gait2392 path point coordinates associated with the body have been embedded in a host mesh along with the a dense cloud of point on the reference bone surface.
The host mesh is a single-element tri-cubic Lagrange mesh. 
When the step is executed, the embedded bone surface points are fitted to corresponding points on the input model's bone model by deforming the host mesh.
Global coordinates of the embedded path points are evaluated from the deformed host mesh and transformed into body locals coordinates as the new path point coordinates.
Finally, muscle optimal fibre length and tendon slack length are recalculated.

The method is best suited to static path points. There are limitations with more complex path points:

- Conditional path points : the coordinates of conditional path points are updated as described above but the activation joint angle is not customised and there is no guarantee that the point activates on the muscle path.
- Moving path points : The spline knots associated with moving path points are embedded in each body's host mesh and can be evaluated to customise the SimmSpline. However, since the host-mesh fit is to the new bone geometry, the deformed host-mesh has no general relation to the intended shape of the spline, which in Gait2392, is the trajectory of the patella through knee flexion.
- Wrapping surfaces are **not** supported.

Further development is required to resolve the issues above. For now, it is recommended that the user carefully check the output model and manually adjust conditional and moving path points as needed.

Requires
--------
- GIAS2: https://bitbucket.org/jangle/gias2
- MAP Client: https://github.com/MusculoskeletalAtlasProject/mapclient

Inputs
------
- **gias-lowerlimb** [GIAS2 LowerLimbAtlas instance]: GIAS2 lowerlimb model to be used to customise Gait2392.
- **osimmodel** [opensim.Model instance] : The Gait2392 opensim model to customise.

Outputs
-------
- **osimmodel** [opensim.Model instance] : The customised Gait2392 opensim model.

Usage
-----
This step is intended to customise the muscle geometry and properties in an input Gait2392 OpenSim lower limb model based on the geometry of an input lower limb model from the _Fieldwork Lowerlimb 2-side Generation Step_.

This step does not have a workflow-runtime GUI. It will simply attempt to perform the customisations automatically based on its configurations.

Configurations
--------------
- **identifier** : Unique name for the step.
- **Input Unit** : Unit of measurement in the input lowerlimb model.
- **Output Unit** : Unit of measurement of the customised OpenSim model. Default is in metres.
- **Write Osim File** : Whether to write out the customised OpenSim model.
- **Update Knee Splines** : Use host-mesh fitting to customise the splines of via points in the knee joint (not recommended for use).
- **Static Vastus** : Modify the splines of vastus muscle vias points so that tibia translation is static with respect to knee flexion (not recommended for use).
- **Output Folder** : Path of directory to output modified opensim model files.

Todo List
---------
- Customise ConditionalPathPoint parameters to ensure correct activation (e.g. on contact with bone, on muscle path)
- Evaluate knee MovingPathPoint trajectory from tibial-frame trajectory
