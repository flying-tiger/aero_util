''' Tools for working with wind-relative attitude parameterizations '''
from numpy import sqrt, sin, cos, arcsin, arctan2

def ab_from_uvw(u, v, w):
    ''' Compute alpha/beta angles from wind-relative velocity vector

        INPUTS:
          u      X-component of the vehicle wind-relative velocity
          v      Y-component of the vehicle wind-relative velocity
          w      Z-component of the vehicle wind-relative velocity

        OUTPUTS:
          alpha  Pitch plane angle of attack, atan2(w,u)  [rad]
          beta   Yaw plane angle of attac, asin(v,V)      [rad]

        NOTE:
          Components of the wind-relative velocity vector are resolved
          in the body-fixed frame with X-axis forward, Y-axis to the
          right and Z-axis down.
    '''
    alpha = arctan2(w, u)
    beta = arcsin(v / sqrt(u*u + v*v + w*w))
    return alpha, beta

def ap_from_uvw(u, v, w):
    ''' Compute total alpha/phi angles from wind-relative velocity vector

        INPUTS:
          u      X-component of the vehicle wind-relative velocity
          v      Y-component of the vehicle wind-relative velocity
          w      Z-component of the vehicle wind-relative velocity

        OUTPUTS:
          alphat  Total angle of attack, atan2(rss(v,w),u) [rad]
          phi     Aerodynamic roll angle, atan2(v,w)       [rad]

        NOTE:
          Components of the wind-relative velocity vector are resolved
          in the body-fixed frame with X-axis forward, Y-axis to the
          right and Z-axis down.
    '''
    alphat = arctan2(sqrt(v*v + w*w), u)
    phi = arctan2(v, w)
    return alphat, phi

def uvw_from_ab(alpha, beta):
    ''' Compute normalized wind-relative velocity from alpha/beta angles

        INPUTS:
          alpha   Pitch plane angle of attack, atan2(w,u)  [rad]
          beta    Yaw plane angle of attac, asin(v,V)      [rad]

        OUTPUTS:
          u      X-component of the vehicle wind-relative velocity
          v      Y-component of the vehicle wind-relative velocity
          w      Z-component of the vehicle wind-relative velocity

        NOTE:
          Components of the wind-relative velocity vector are resolved
          in the body-fixed frame with X-axis forward, Y-axis to the
          right and Z-axis down.
    '''
    u = cos(beta)*cos(alpha)
    v = sin(beta)
    w = cos(beta)*sin(alpha)
    return u, v, w

def uvw_from_ap(alphat, phi):
    ''' Compute normalized wind-relative velocity from total alpha/phi angles

        INPUTS:
          alphat  Total angle of attack, atan2(rss(v,w),u) [rad]
          phi     Aerodynamic roll angle, atan2(v,w)       [rad]

        OUTPUTS:
          u      X-component of the vehicle wind-relative velocity
          v      Y-component of the vehicle wind-relative velocity
          w      Z-component of the vehicle wind-relative velocity

        NOTE:
          Components of the wind-relative velocity vector are resolved
          in the body-fixed frame with X-axis forward, Y-axis to the
          right and Z-axis down.
    '''
    u = cos(alphat)
    v = sin(alphat)*sin(phi)
    w = sin(alphat)*cos(phi)
    return u, v, w

def ab_from_ap(alphat, phi):
    ''' Compute alpha/beta angles from total alpha/phi

        INPUTS:
          alphat  Total angle of attack, atan2(rss(v,w),u) [rad]
          phi     Aerodynamic roll angle, atan2(v,w)       [rad]

        OUTPUTS:
          alpha   Pitch plane angle of attack, atan2(w,u)  [rad]
          beta    Yaw plane angle of attac, asin(v,V)      [rad]
    '''
    return ab_from_uvw(*uvw_from_ap(alphat, phi))

def ap_from_ab(alpha, beta):
    ''' Compute alpha/beta angles from total alpha/phi

        INPUTS:
          alpha   Pitch plane angle of attack, atan2(w,u)  [rad]
          beta    Yaw plane angle of attac, asin(v,V)      [rad]

        OUTPUTS:
          alphat  Total angle of attack, atan2(rss(v,w),u) [rad]
          phi     Aerodynamic roll angle, atan2(v,w)       [rad]
    '''
    return ap_from_uvw(*uvw_from_ab(alpha, beta))

