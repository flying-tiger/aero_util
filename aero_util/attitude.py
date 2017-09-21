''' Tools for working with wind-relative atttitude parameterizations '''
from numpy import sqrt, sin, cos, arcsin, arctan2, radians, degrees

def ab_from_uvw(u, v, w):
    ''' Compute alpha/beta angles from wind-relative velocity vector

        INPUTS:
          u      X-component of the vehicle wind-relative velocity
          v      Y-component of the vehicle wind-relative velocity
          w      Z-component of the vehicle wind-relative velocity

        OUTPUTS:
          alpha  Pitch plane angle of attack, atan2(w,u)  [deg]
          beta   Yaw plane angle of attac, asin(v,V)      [deg]

        NOTE:
          Components of the wind-relative velocity vector are resolved
          in the body-fixed frame with X-axis forward, Y-axis to the
          right and Z-axis down.
    '''
    alpha = degrees(arctan2(w, u))
    beta = degrees(arcsin(v / sqrt(u*u + v*v + w*w)))
    return alpha, beta

def ap_from_uvw(u, v, w):
    ''' Compute total alpha/phi angles from wind-relative velocity vector

        INPUTS:
          u      X-component of the vehicle wind-relative velocity
          v      Y-component of the vehicle wind-relative velocity
          w      Z-component of the vehicle wind-relative velocity

        OUTPUTS:
          alphat  Total angle of attack, atan2(rss(v,w),u) [deg]
          phi     Aerodynamic roll angle, atan2(v,w)       [deg]

        NOTE:
          Components of the wind-relative velocity vector are resolved
          in the body-fixed frame with X-axis forward, Y-axis to the
          right and Z-axis down.
    '''
    alphat = degrees(arctan2(sqrt(v*v + w*w), u))
    phi = degrees(arctan2(v, w))
    return alphat, phi

def uvw_from_ab(alpha, beta):
    ''' Compute normalized wind-relative velocity from alpha/beta angles

        INPUTS:
          alpha   Pitch plane angle of attack, atan2(w,u)  [deg]
          beta    Yaw plane angle of attac, asin(v,V)      [deg]

        OUTPUTS:
          u      X-component of the vehicle wind-relative velocity
          v      Y-component of the vehicle wind-relative velocity
          w      Z-component of the vehicle wind-relative velocity

        NOTE:
          Components of the wind-relative velocity vector are resolved
          in the body-fixed frame with X-axis forward, Y-axis to the
          right and Z-axis down.
    '''
    alpha = radians(alpha)
    beta = radians(beta)
    u = cos(beta)*cos(alpha)
    v = sin(beta)
    w = cos(beta)*sin(alpha)
    return u, v, w

def uvw_from_ap(alphat, phi):
    ''' Compute normalized wind-relative velocity from total alpha/phi angles

        INPUTS:
          alphat  Total angle of attack, atan2(rss(v,w),u) [deg]
          phi     Aerodynamic roll angle, atan2(v,w)       [deg]

        OUTPUTS:
          u      X-component of the vehicle wind-relative velocity
          v      Y-component of the vehicle wind-relative velocity
          w      Z-component of the vehicle wind-relative velocity

        NOTE:
          Components of the wind-relative velocity vector are resolved
          in the body-fixed frame with X-axis forward, Y-axis to the
          right and Z-axis down.
    '''
    alphat = radians(alphat)
    phi = radians(phi)
    u = cos(alphat)
    v = sin(alphat)*sin(phi)
    w = sin(alphat)*cos(phi)
    return u, v, w

def ab_from_ap(alphat, phi):
    ''' Compute alpha/beta angles from total alpha/phi

        INPUTS:
          alphat  Total angle of attack, atan2(rss(v,w),u) [deg]
          phi     Aerodynamic roll angle, atan2(v,w)       [deg]

        OUTPUTS:
          alpha   Pitch plane angle of attack, atan2(w,u)  [deg]
          beta    Yaw plane angle of attac, asin(v,V)      [deg]
    '''
    return ab_from_uvw(*uvw_from_ap(alphat, phi))

def ap_from_ab(alpha, beta):
    ''' Compute alpha/beta angles from total alpha/phi

        INPUTS:
          alpha   Pitch plane angle of attack, atan2(w,u)  [deg]
          beta    Yaw plane angle of attac, asin(v,V)      [deg]

        OUTPUTS:
          alphat  Total angle of attack, atan2(rss(v,w),u) [deg]
          phi     Aerodynamic roll angle, atan2(v,w)       [deg]
    '''
    return ap_from_uvw(*uvw_from_ab(alpha, beta))

