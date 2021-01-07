import numpy as np 
import math

def rotate(x, y, z, theta_x, theta_y, theta_z):

    theta_x = math.radians(theta_x)
    theta_y = math.radians(theta_y)
    theta_z = math.radians(theta_z)

    r_x = np.array([
        [
            1, 0, 0
        ],
        [
            0, math.cos(theta_x), -math.sin(theta_x)
        ],
        [
            0, math.sin(theta_x), math.cos(theta_x)
        ]
    ])

    r_y = np.array(
        [
            [
                math.cos(theta_y), 0, math.sin(theta_y)
            ],
            [
                0, 1, 0
            ],
            [
                -math.sin(theta_y), 0, math.cos(theta_y)
            ]
        ]
    )

    r_z = np.array(
        [
            [
                math.cos(theta_z), -math.sin(theta_z), 0
            ],
            [
                math.sin(theta_z), math.cos(theta_z), 0
            ],
            [
                0, 0, 1
            ]
        ]
    )

    r_xy = np.dot(r_x, r_z)
    r_xyz = np.dot(r_xy, r_z)
    return(r_xyz)

def rotateX3D (theta, x, y, z):
    sinTheta = math.sin(theta)
    cosTheta = math.cos(theta)
    ay = y * cosTheta - z * sinTheta
    az = z * cosTheta + y * sinTheta
    return [x, ay, az]

def rotateZ3D (theta, x, y, z): 
    sinTheta = math.sin(theta)
    cosTheta = math.cos(theta)

    ax = x * cosTheta - y * sinTheta
    ay = y * cosTheta + x * sinTheta
    return [ax, ay, z]


def rotateY3D(theta, x, y, z):
  sinTheta = math.sin(theta)
  cosTheta = math.cos(theta)
  ax = x * cosTheta + z * sinTheta
  az = z * cosTheta - x * sinTheta
  return [ax, y, az]


if __name__ == "__main__":
    

    print( rotateZ3D(20, 0, 20, 30) )



