import qtm
import numpy as np

# Script used to calculate the position of a reconstructed marker (predifined in a static)
# in a dynamic trial (the dynamic trial must be selected when running this script). 
# The local frame must be defined before running this script (get_LocalFrame_AllinOne).

def calculate_frame(marker1, marker2, marker3):
# This function calculates the rotational matrix of the chosen segment 
# relative to the global coordinate system. marker1, marker2, and marker 3,
# are the position vectors (3 x 1 x n) of the chosen markers in the global
# coordinate system at Frame n.
# The origin (O_frame2) of the segment is set at the center of the 3 chosen markers.
# The function returns the origin (O_frame2), the rotational matrix (R_frame2) and the
# total number of frames in the dynamic trial (y).
        
    M1 = []
    M2 = []
    M3 = []

    i=0
    while i < len(marker1):
        frame1 = marker1[i]
        frame2 = marker2[i]
        frame3 = marker3[i]
        frame_int1 = frame1['position']
        frame_int2 = frame2['position']
        frame_int3 = frame3['position']
        M1.append(frame_int1)
        M2.append(frame_int2)
        M3.append(frame_int3)
        i += 1

    M1 = np.asarray(M1)
    M2 = np.asarray(M2)
    M3 = np.asarray(M3)

    M1 = np.transpose(M1)
    M2 = np.transpose(M2)
    M3 = np.transpose(M3)

    x, y = M1.shape
    O_frame2 = np.zeros((3,y))

    for i in range(y):
        O_frame2[0:x, i] = (M1[0:x, i] + M2[0:x, i] + M3[0:x, i]) / 3

    Help1 = np.zeros((3, 1, y))
    X = np.zeros((3, 1, y))
    Y = np.zeros((3, 1, y))
    Z = np.zeros((3, 1, y))

    for i in range(y):
        X[0:x, 0, i] = M3[0:x, i] - M1[0:x, i]
        Help1[0:x, 0, i] = M2[0:x, i] - M1[0:x, i]
        Z[0:x, 0, i] = np.cross(X[0:x, 0, i], Help1[0:x, 0, i], axis=0)
        Y[0:x, 0, i] = np.cross(Z[0:x, 0, i], X[0:x, 0, i], axis=0)
        X[0:x, 0, i] = X[0:x, 0, i] / np.linalg.norm(X[0:x, 0, i])
        Y[0:x, 0, i] = Y[0:x, 0, i] / np.linalg.norm(Y[0:x, 0, i])
        Z[0:x, 0, i] = Z[0:x, 0, i] / np.linalg.norm(Z[0:x, 0, i])
    
    R_frame2 = np.concatenate((X, Y, Z), axis=1)
    return O_frame2, R_frame2, y


# Load trajectories of the 3 defined markers in the dynamic trial.

id1 = qtm.data.object.trajectory.find_trajectory(M1label)
id2 = qtm.data.object.trajectory.find_trajectory(M2label)
id3 = qtm.data.object.trajectory.find_trajectory(M3label)
marker1 = qtm.data.series._3d.get_samples(id1)
marker2 = qtm.data.series._3d.get_samples(id2)
marker3 = qtm.data.series._3d.get_samples(id3)
Oframe2, Rframe2, frames2 = calculate_frame(marker1,marker2,marker3)

# create the "new" reconstructed marker
trajectory_label = MRlabel + "_reconstructed"
trajectory_id = qtm.data.object.trajectory.add_trajectory(trajectory_label)
measured_range = qtm.gui.timeline.get_measured_range()
calculated_3d_data = []

# calculate location of the of the "new" reconstructed marker in the
# global coordinate system. The relative postion of the selected 
# marker in the local segment (MRlokalmean) is used to calculate the global
# postion.
i=0
MRglobal = np.zeros((3,frames2))
for i in range(frames2):
    MRglobal[0:3,i] = np.dot(Rframe2[0:3,0:3,i], MRlokalmean) + Oframe2[0:3,i]
    calculated_3d_data.append({"position": [MRglobal[0,i],MRglobal[1,i],MRglobal[2,i]], "residual": 0.0})

qtm.data.series._3d.set_samples(trajectory_id, measured_range, calculated_3d_data)


