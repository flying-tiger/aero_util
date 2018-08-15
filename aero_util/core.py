''' Core toolbox components for general-purpose calculations '''
import pint
import numpy as np


#-------------------------------------------------------------------------------
# Unit Conversion (Pint Wrappers)
#-------------------------------------------------------------------------------
_UREG = pint.UnitRegistry()

deg = np.degrees
rad = np.radians

def convert(value, uin, uout):
    ''' Convert value between units

        INPUTS:
            value   float     The value to be converted
            uin     str|unit  The units of measure for the input
            uout    str|unit  The units of measure for the output

        OUTPUTS:
            cvalue  float     The converted value
    '''
    return _UREG.convert(value, uin, uout)

def convert_from(value, uin):
    ''' Convert value from input units to SI

        INPUTS:
            value   float     The value to be converted
            uin     str|unit  The units of measure for the input

        OUTPUTS:
            cvalue  float     The converted value
    '''
    return _UREG.Quantity(value, uin).to_base_units().magnitude

def convert_to(value, uout):
    ''' Convert value from SI to output units

        INPUTS:
            value   float     The SI value to be converted
            uin     str|unit  The units of measure for the output

        OUTPUTS:
            cvalue  float     The converted value
    '''
    si_unit = _UREG(uout).to_base_units().units
    return _UREG.convert(value, si_unit, uout)


#-------------------------------------------------------------------------------
# Direction Cosine Matrices (DCMs)
#-------------------------------------------------------------------------------
# NOTE: Given two cartesian coordinate systems A and B, the vector V may be
#       equivilently expressed as:
#
#           V = a1*A1 + a2*A2 + a3*A3
#           V = b1*B1 + b2*B2 + b3*B3
#
#       The functions below return the change-of-basis (a.k.a passive or alias)
#       direction cosine matrix, TAB, which allows computing [b1,b2,b3] given
#       [a1,a2,a3].

def rotate_axis(axis, angle=None, angle_deg=None):
    ''' Return DCM for coordinate system rotation about an arbitrary axis

        INPUTS:
            axis       float(3)  Unit vector specifying axis of rotation
            angle      float     Angle of rotation [rad]
            angle_deg  float     Angle of rotation [deg]

        OUTPUTS:
            dcm        np.array  3x3 rotation matrix
    '''
    x,y,z = axis
    norm  = np.sqrt(x*x + y*y + z*z)
    x,y,z = x/norm, y/norm, z/norm

    a   = _set_angles(angle, angle_deg)
    c,s = np.cos(a), np.sin(a)
    C   = 1.0 - c

    return np.array([
        [x*x*C + c,   x*y*C + z*s, x*z*C - y*s],
        [y*x*C - z*s, y*y*C + c,   y*z*C + x*s],
        [z*x*C + y*s, z*y*C - x*s, z*z*C + c  ],
    ])

def rotate_seq(sequence, angles=None, angles_deg=None):
    ''' Return DCM for a sequence of x/y/z rotations

        INPUTS:
            sequence    string    List of rotations, e.g. 'zyx','xyx'
            angles      float(N)  Angles for each rotation [rad]
            angles_deg  float(N)  Angles for each rotation [deg]

        OUTPUTS:
            dcm        np.array  3x3 rotation matrix
    '''
    angles = _set_angles(angles, angles_deg)
    dcm = np.eye(3)
    for axis, angle in zip(sequence.lower(), angles):
        if axis == 'x':
            dcm = rotate_x(angle) @ dcm
        elif axis == 'y':
            dcm = rotate_y(angle) @ dcm
        elif axis == 'z':
            dcm = rotate_z(angle) @ dcm
        else:
            raise RuntimeError(f'Invalid rotation axis "{axis}"')
    return dcm

def rotate_x(angle=None, angle_deg=None):
    ''' Return DCM for coordinate system rotation about the X-axis

        INPUTS:
          angle      float     Rotation angle about +X axis [rad]
          angle_deg  float     Rotation angle about +X axis [deg]

        OUTPUTS:
          dcm        np.array  3x3 rotation matrix
    '''
    a = _set_angles(angle, angle_deg)
    return np.array([
        [1.0,  0.0,       0.0      ],
        [0.0,  np.cos(a), np.sin(a)],
        [0.0, -np.sin(a), np.cos(a)],
    ])

def rotate_y(angle=None, angle_deg=None):
    ''' Return DCM for coordinate system rotation about the Y-axis

        INPUTS:
          angle      float     Rotation angle about +Y axis [rad]
          angle_deg  float     Rotation angle about +Y axis [deg]

        OUTPUTS:
          dcm        np.array  3x3 rotation matrix
    '''
    a = _set_angles(angle, angle_deg)
    return np.array([
        [np.cos(a),  0.0, -np.sin(a)],
        [0.0,        1.0,  0.0      ],
        [np.sin(a),  0.0,  np.cos(a)],
    ])

def rotate_z(angle=None, angle_deg=None):
    ''' Return DCM for coordinate system rotation about the Z-axis

        INPUTS:
          angle      float     Rotation angle about +Z axis [rad]
          angle_deg  float     Rotation angle about +Z axis [deg]

        OUTPUTS:
          dcm        np.array  3x3 rotation matrix
    '''
    a = _set_angles(angle, angle_deg)
    return np.array([
        [ np.cos(a),  np.sin(a),  0.0],
        [-np.sin(a),  np.cos(a),  0.0],
        [ 0.0,        0.0,        1.0],
    ])


#-------------------------------------------------------------------------------
# Helper Functions
#-------------------------------------------------------------------------------
def _set_angles(angles=None, angles_deg=None):
    ''' Takes angles as either deg or radians, returning radians '''
    if angles == None and angles_deg == None:
        raise RuntimeError('Both angle and angle_deg are uninitialized')
    if angles != None and angles_deg != None:
        raise RuntimeError('Both angle and angle_deg are defined; please define one or the other')
    if angles_deg:
        angles = np.radians(angles_deg)
    return angles

