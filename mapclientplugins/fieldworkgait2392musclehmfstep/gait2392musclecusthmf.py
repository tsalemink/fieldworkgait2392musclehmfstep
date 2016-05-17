"""
Module for customising opensim segmented muscle points by host mesh fitting
the bone surface
"""
import os
import numpy as np
import copy
from gias2.fieldwork.field import geometric_field
from gias2.fieldwork.field.tools import fitting_tools
from gias2.common import transform3D
from gias2.registration import alignment_fitting as af
from gias2.musculoskeletal.bonemodels import bonemodels
from gias2.musculoskeletal import osim

SELF_DIRECTORY = os.path.split(__file__)[0]
DATA_DIR = os.path.join(SELF_DIRECTORY, 'data/fieldwork_geometry')
VALID_SEGS = set(['pelvis',
                  'femur_l', 'femur_r',
                  'tibia_l', 'tibia_r',
                  ])
OSIM_FILENAME = 'gait2392_simbody.osim'
VALID_UNITS = ('nm', 'um', 'mm', 'cm', 'm', 'km')

def dim_unit_scaling(in_unit, out_unit):
    """
    Calculate the scaling factor to convert from the input unit (in_unit) to
    the output unit (out_unit). in_unit and out_unit must be a string and one
    of ['nm', 'um', 'mm', 'cm', 'm', 'km']. 

    inputs
    ======
    in_unit : str
        Input unit
    out_unit :str
        Output unit

    returns
    =======
    scaling_factor : float
    """

    unit_vals = {
        'nm': 1e-9,
        'um': 1e-6,
        'mm': 1e-3,
        'cm': 1e-2,
        'm':  1.0,
        'km': 1e3,
        }

    if in_unit not in unit_vals:
        raise ValueError(
            'Invalid input unit {}. Must be one of {}'.format(
                in_unit, list(unit_vals.keys())
                )
            )
    if out_unit not in unit_vals:
        raise ValueError(
            'Invalid input unit {}. Must be one of {}'.format(
                in_unit, list(unit_vals.keys())
                )
            )

    return unit_vals[in_unit]/unit_vals[out_unit]

def _update_femur_opensim_acs(femur_model):
    femur_model.acs.update(
        *bonemodels.model_alignment.createFemurACSOpenSim(
            femur_model.landmarks['femur-HC'],
            femur_model.landmarks['femur-MEC'],
            femur_model.landmarks['femur-LEC'],
            side=femur_model.side
            )
        )

def _update_tibiafibula_opensim_acs(tibiafibula_model):
    tibiafibula_model.acs.update(
        *bonemodels.model_alignment.createTibiaFibulaACSOpenSim(
            tibiafibula_model.landmarks['tibiafibula-MM'],
            tibiafibula_model.landmarks['tibiafibula-LM'],
            tibiafibula_model.landmarks['tibiafibula-MC'],
            tibiafibula_model.landmarks['tibiafibula-LC'],
            side=tibiafibula_model.side
            )
        )

def _osim_segment_data(name, out_unit):
    """
    Reads bone surface and muscle point data for a segment

    Inputs
    ------
    name : str
        Name of the model segment (pelvis, femur_{l|r}, tibia_{l|r})
    out_unit : str
        Measurement unit to output

    Returns
    -------
    osim_surf_pts : n x 3 array
        Surface point coordinates of the opensim bone model
    osim_muscle_pts : m x 3 array
        Coordinates of the opensim muscle points
    osim_surf_xi : list
        Host-mesh Xi coordinates of osim_surf_pts
    osim_muscle_xi : list
        Host-mesh Xi coordinates of osim_muscle_pts
    osim_muscle_labels : list of strings
        The names of each model point
    hm : geometric_field instance
        The host mesh
    """

    SURF_PTS_MULT = dim_unit_scaling('mm', out_unit)
    MUSCLE_PTS_MULT = dim_unit_scaling('m', out_unit) #1e3

    #==================================================#
    # Precalculated for each segment: host-meshes, surface xi, muscle point xi
    gait2392_segments = (
        'pelvis',
        'femur_l', 'femur_r',
        'tibia_l', 'tibia_r',
        )
    host_mesh_file_pat = '{}.hostmesh.{}'
    surf_ptcld_file_pat = '{}.nodes'
    surf_xi_file_pat = '{}.nodes.xi'
    muscle_ptcld_file_pat = '{}.muscles.txt'
    muscle_xi_file_pat = '{}.muscle.xi'
    #=================================================#

    # reference surface pointcloud & Xi
    osim_surf_pts = np.loadtxt(
        os.path.join(DATA_DIR, surf_ptcld_file_pat.format(name))
        )
    osim_surf_pts *= SURF_PTS_MULT
    
    _surf_xi = np.loadtxt(
        os.path.join(DATA_DIR, surf_xi_file_pat.format(name))
        )
    osim_surf_xi = [[l[0], np.array([l[1], l[2], l[3]])] for l in _surf_xi] 

    # reference muscle points, Xi & labels
    osim_muscle_labels = tuple(
        np.loadtxt(
            os.path.join(DATA_DIR, muscle_ptcld_file_pat.format(name)),
            usecols=(0,), dtype=str,
            )
        )
    osim_muscle_pts = np.loadtxt(
        os.path.join(DATA_DIR, muscle_ptcld_file_pat.format(name)),
        usecols=(1,2,3), dtype=float,
        )
    osim_muscle_pts *= MUSCLE_PTS_MULT
    _muscle_xi = np.loadtxt(
        os.path.join(DATA_DIR, muscle_xi_file_pat.format(name))
        )
    osim_muscle_xi = [[l[0], np.array([l[1], l[2], l[3]])] for l in _muscle_xi] 

    # host mesh
    hm = geometric_field.load_geometric_field(
        os.path.join(DATA_DIR, host_mesh_file_pat.format(name, 'geof')),
        os.path.join(DATA_DIR, host_mesh_file_pat.format(name, 'ens')),
        os.path.join(DATA_DIR, host_mesh_file_pat.format(name, 'mesh')),
        )

    return osim_surf_pts, osim_muscle_pts, osim_surf_xi, osim_muscle_xi,\
        osim_muscle_labels, hm

def _hmf_seg(targ_pts, osim_surf_pts, osim_muscle_pts,
    osim_surf_xi=None, osim_muscle_xi=None, host_mesh=None):
    """

    Inputs
    ------
    targ_pts : nx3 array
        Array of point coordinates of the target bone surface
    osim_surf_pts : nx3 array
        Array of point coordinates of the opensim bone surface
        Should be correspondent with targ_ptcld
    osim_muscle_pts : px3 array
        Array of unfitted muscle point coordinates

    Returns
    -------
    fitted_osim_muscle_points : px3 array
        Array of unfitted muscle point coordinates
    fit_rms : float
        RMS fitting error
    source_points_fitting_hmf : nx3 array
        Array of fitted source point coordinates
    """

    host_mesh_pad = 0.25 # host mesh padding around slave points
    host_elem_type = 'quad444' # quadrilateral cubic host elements
    host_elems = [1,1,1] # a single element host mesh [x,y,z]
    maxit = 50
    sobd = [4,4,4]
    sobw = 1e-6
    xtol = 1e-6

    source_points_fitting = osim_surf_pts
    source_points_passive = osim_muscle_pts
    target_points = targ_pts
    source_points_all = np.vstack([
        source_points_fitting,
        source_points_passive
        ])

    #=============================================================#
    # rigidly register source points to target points
    reg1_T, source_points_fitting_reg1, reg1_errors = af.fitRigid(
        source_points_fitting,
        target_points,
        xtol=1e-6,
        sample=1000,
        outputErrors=1
    )

    # add isotropic scaling to rigid registration
    reg2_T, source_points_fitting_reg2, reg2_errors = af.fitRigidScale(
        source_points_fitting,
        target_points,
        xtol=1e-6,
        sample=1000,
        t0=np.hstack([reg1_T, 1.0]),
        outputErrors=1
    )

    # apply same transforms to the passive slave points
    source_points_passive_reg2 = transform3D.transformRigidScale3DAboutP(
        source_points_passive,
        reg2_T,
        source_points_fitting.mean(0)
    )
    source_points_all = np.vstack([
        source_points_fitting_reg2,
        source_points_passive_reg2,
    ])

    # if host mesh provided, apply the same transforms
    if host_mesh is not None:
        host_mesh.transformRigidScaleRotateAboutP(reg2_T, source_points_fitting.mean(0))

    #=============================================================#

    def slave_func(x):
        return ((x - target_points)**2.0).sum(1)

    # make host mesh
    if host_mesh is None:
        host_mesh = GFF.makeHostMeshMulti(
            source_points_all.T,
            host_mesh_pad,
            host_elem_type,
            host_elems,
        )

    # calculate the emdedding (xi) coordinates of passive
    # source points.
    if osim_muscle_xi is not None:
        source_points_passive_xi = osim_muscle_xi
    else:
        source_points_passive_xi = host_mesh.find_closest_material_points(
            source_points_passive_reg2,
            initGD=[50,50,50],
            verbose=True,
        )[0]

    # make passive source point evaluator function
    eval_source_points_passive = geometric_field.makeGeometricFieldEvaluatorSparse(
        host_mesh, [1,1],
        matPoints=source_points_passive_xi,
    )

    # host mesh fit
    host_x_opt, source_points_fitting_hmf, \
    slave_xi, rmse_hmf = fitting_tools.hostMeshFitPoints(
        host_mesh,
        source_points_fitting_reg2,
        slave_func,
        slave_xi=osim_surf_xi,
        max_it=maxit,
        sob_d=sobd,
        sob_w=sobw,
        verbose=True,
        xtol=xtol
    )
    # evaluate the new positions of the passive source points
    source_points_passive_hmf = eval_source_points_passive(host_x_opt).T

    return source_points_passive_hmf, rmse_hmf, source_points_fitting_hmf

def _map_local_coords(segment_name, target_model, global_pts):
    _target_model = copy.deepcopy(target_model)
    if 'femur' in segment_name:
        _update_femur_opensim_acs(_target_model)
    elif 'tibia' in segment_name:
        _update_tibiafibula_opensim_acs(_target_model)
    return _target_model.acs.map_local(global_pts)

def _update_osim_segment_muscle_points(omodel, labels, coords, in_unit, out_unit):
    """
    Modify muscle point coordinates in an opensim model
    """

    # convert back to meters
    coords = coords*dim_unit_scaling(in_unit, out_unit)
    
    for li, l in enumerate(labels):
        # skip points whose label contains the keyword
        if 'simmspline' not in l:
            muscle_name = l.split('-')[0]
            omodel.muscles[muscle_name].path_points[l].location = coords[li]

def _update_osim_tibia_vas_spline(side, omodel, labels, coords, in_unit, out_unit, static):
    """
    Modify tibia's vastus muscle splines. Spline point labels should have format:
    vas_{med|int|lat}_{l|r}-P[p]-simmspline-[n] where p is the path point number
    and n is an integer denoting the number of the spline point.
    """
    # convert back to meters
    coords = coords*dim_unit_scaling(in_unit, out_unit)

    def _get_coords_by_name(name):
        """
        Get spline points of the specified spline
        """
        inds = []
        named_labels = []
        for li, l  in enumerate(labels):
            if name in l:
                inds.append(li)
                named_labels.append(l)

        _new_order = np.argsort(named_labels)
        inds = [inds[i] for i in _new_order]
        return coords[inds,:]

    def _update_muscle(muscle_name, pathpoint):
        """
        Update the y values of the specified muscles pathpoint spline
        """
        
        if static:
            # get the static location of the path point
            pp = omodel.muscles[muscle_name].path_points['{}-P{}'.format(muscle_name, pathpoint)]
            # get current spline values and replace spline y values with the new
            # ones
            sx, sy, sz = pp.getSimmSplineParams()
            _x = np.array([pp.location[0],]*sx.shape[1])
            _y = np.array([pp.location[1],]*sy.shape[1])
            _z = np.array([pp.location[2],]*sz.shape[1])
            sx[1] = _x
            sy[1] = _y
            sz[1] = _z
        else:
            # get customised spline y values for each coordinate
            _x, _y, _z = _get_coords_by_name('{}-P{}-simmspline'.format(muscle_name, pathpoint)).T
            pp = omodel.muscles[muscle_name].path_points['{}-P{}'.format(muscle_name, pathpoint)]
            # get current spline values and replace spline y values with the new
            # ones
            sx, sy, sz = pp.getSimmSplineParams()
            sx[1] = _x
            sy[1] = _y
            sz[1] = _z[:2]

        pp.updateSimmSplineParams(x_params=sx, y_params=sy, z_params=sz)

    _update_muscle('vas_med_{}'.format(side), '5')
    _update_muscle('vas_int_{}'.format(side), '4')
    _update_muscle('vas_lat_{}'.format(side), '5')

def cust_segment_muscle_points(segment_name, target_model, omodel,
    in_unit='mm', out_unit='m', static_vas=True):
    """
    Customise Gait2392 muscle point coordinates based on customised bone
    geometries. The reference gait2392 muscle points are embedded in 
    reference host meshes. The reference bone surfaces are host mesh-fit
    to the customised bones and the transformation applied to the 
    muscle points.

    Inputs
    ------
    segment_name : string
        Name of the gait2392 segment to be customised. Should be one of
        "pelvis", "femur_l", "femur_r", "tibia_l", "tibia_r".
    target_model : BoneModel instance
        The customised bone model to be fitted to
    omodel : opensim.Model instance
        The model that will have its muscle points customised
    in_unit : str [optional]
        Input unit, see dim_unit_scaling.
    out_unit : str [optional]
        Output unit, see dim_unit_scaling.
    static_vas : bool [optional, default=True]
        If true, uses the same customised path point coordinate for
        all point along the spline of the patella insertion of the
        vastus muscles. Else, uses the HMF'd spline coordinates. 

    Returns
    -------
    None
    """

    if segment_name not in VALID_SEGS:
        raise ValueError(
            'Invalid segment name {}. Must be one of {}.'.format(
                segment_name, VALID_SEGS
                )
            )

    # load reference segment data
    targ_pts = target_model.gf.get_all_point_positions()
    (osim_surf_pts, osim_muscle_pts,
    osim_surf_xi, osim_muscle_xi,
    osim_muscle_labels,
    host_mesh) =  _osim_segment_data(segment_name, in_unit)

    # host mesh fit reference segment to target model
    cust_muscle_pts, rmse, cust_surf_pts = _hmf_seg(
        targ_pts, osim_surf_pts, osim_muscle_pts, osim_surf_xi,
        osim_muscle_xi, host_mesh
        )

    # map new muscle positions to segment local CS
    cust_muscle_pts_local = _map_local_coords(
        segment_name, target_model, cust_muscle_pts
        )

    # update osim file
    _update_osim_segment_muscle_points(
        omodel, osim_muscle_labels, cust_muscle_pts_local, in_unit, out_unit
        )

    # for tibia_l and tibia_r, need to define new vas P-5 spline
    if segment_name=='tibia_l':
        _update_osim_tibia_vas_spline(
            'l', omodel, osim_muscle_labels, cust_muscle_pts_local,
            in_unit, out_unit, static_vas
            )
    elif segment_name=='tibia_r':
        _update_osim_tibia_vas_spline(
            'r', omodel, osim_muscle_labels, cust_muscle_pts_local,
            in_unit, out_unit, static_vas
            )

    return (targ_pts, osim_surf_pts, osim_muscle_pts, cust_surf_pts,
            cust_muscle_pts, host_mesh
            )

class gait2392MuscleCustomiser(object):

    def __init__(self, config, ll=None, osimmodel=None):
        """
        Class for customising gait2392 muscle points using host-mesh fitting

        inputs
        ======
        config : dict
            Dictionary of option. (work in progress) Example:
            {
            'osim_output_dir': '/path/to/output/model.osim',
            'in_unit': 'mm',
            'out_unit': 'm',
            'write_osim_file': True,
            'side': 'left',
            }
        ll : LowerLimbAtlas instance
            Model of lower limb bone geometry and pose
        osimmodel : opensim.Model instance
            The opensim model instance to customise

        """
        self.config = config
        self.ll = ll
        self.gias_osimmodel = None
        if osimmodel is not None:
            self.set_osim_model(osimmodel)

    def set_osim_model(self, model):
        self.gias_osimmodel = osim.Model(model=model)

    def cust_pelvis(self):
        self.pelvis_res = cust_segment_muscle_points(
            'pelvis', self.ll.models['pelvis'], self.gias_osimmodel,
            in_unit=self.config['in_unit'],
            out_unit=self.config['out_unit'],
            )

    def cust_femur_l(self):
        self.femur_l_res = cust_segment_muscle_points(
            'femur_l', self.ll.models['femur-l'], self.gias_osimmodel,
            in_unit=self.config['in_unit'],
            out_unit=self.config['out_unit'],
            )

    def cust_femur_r(self):
        self.femur_r_res = cust_segment_muscle_points(
            'femur_r', self.ll.models['femur-r'], self.gias_osimmodel,
            in_unit=self.config['in_unit'],
            out_unit=self.config['out_unit'],
            )

    def cust_tibia_l(self):
        self.tibia_l_res = cust_segment_muscle_points(
            'tibia_l', self.ll.models['tibiafibula-l'], self.gias_osimmodel,
            in_unit=self.config['in_unit'],
            out_unit=self.config['out_unit'],
            static_vas=self.config['static_vas']
            )

    def cust_tibia_r(self):
        self.tibia_r_res = cust_segment_muscle_points(
            'tibia_r', self.ll.models['tibiafibula-r'], self.gias_osimmodel,
            in_unit=self.config['in_unit'],
            out_unit=self.config['out_unit'],
            static_vas=self.config['static_vas']
            )

    def write_cust_osim_model(self):
        self.gias_osimmodel.save(
            os.path.join(str(self.config['osim_output_dir']), OSIM_FILENAME)
            )

    def customise(self):
        self.cust_pelvis()
        self.cust_femur_l()
        self.cust_tibia_l()
        self.cust_femur_r()
        self.cust_tibia_r()
        if self.config['write_osim_file']:
            self.write_cust_osim_model()


