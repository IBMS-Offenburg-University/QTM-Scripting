import qtm
import numpy as np

def set_marker_reconstruct():
    # Set the marker that will be reconstructed. Marker must be present in static and should be
    # missing in the dynamic trial. Marker must be selected in the static trial in QTM.
    global MRLABEL
    selections = qtm.gui.selection.get_selections()
    help = selections[0]
    id = help['id']
    MRLABEL = qtm.data.object.trajectory.get_label(id)
    print("Missing Marker set to: " + MRLABEL)

def set_marker_1():
    # Set the first marker. Marker must be present in static and dynamic trial.
    # Marker must be selected in the static trial in QTM.
    global M1LABEL
    selections = qtm.gui.selection.get_selections()
    help = selections[0]
    id = help['id']
    M1LABEL = qtm.data.object.trajectory.get_label(id)
    print("Marker 1 set to: " + M1LABEL)
    
def set_marker_2():
    # Set the second marker. Marker must be present in static and dynamic trial.
    # Marker must be selected in the static trial in QTM.
    global M2LABEL
    selections = qtm.gui.selection.get_selections()
    help = selections[0]
    id = help['id']
    M2LABEL = qtm.data.object.trajectory.get_label(id)
    print("Marker 2 set to: " + M2LABEL)

def set_marker_3():
    # Set the third marker. Marker must be present in static and dynamic trial.
    # Marker must be selected in the static trial in QTM.
    global M3LABEL
    selections = qtm.gui.selection.get_selections()
    help = selections[0]
    id = help['id']
    M3LABEL = qtm.data.object.trajectory.get_label(id)
    print("Marker 3 set to: " + M3LABEL)

def add_command(name, execute_func, update_func=None):
    if name in qtm.gui.get_commands():
        return False  # E A R L Y   E X I T
    qtm.gui.add_command(name)
    qtm.gui.set_command_execute_function(name, execute_func)
    if update_func is not None:
        qtm.gui.set_command_update_function(name, update_func)
    return True

def add_menu_item(menu_id, button_text, command_name, index=None):
    # Get menu name
    list_of_all_menus_as_dicts = qtm.gui.get_menu_items()
    menu_name = ""
    for curr_menu in list_of_all_menus_as_dicts:
        if curr_menu["submenu"] == menu_id:
            menu_name = curr_menu["text"].replace("&", "")
    # Check for duplicate button-text in submenu
    list_of_all_menu_items_as_dicts = qtm.gui.get_menu_items(menu_id)
    for curr_item in list_of_all_menu_items_as_dicts:
        if curr_item["text"] == button_text:
            return False  # E A R L Y   E X I T
    qtm.gui.insert_menu_button(menu_id, button_text, command_name, index)
    return True

def calculate_frame(marker1, marker2, marker3):
# This function calculates the rotational matrix of the chosen segment 
# relative to the global coordinate system. marker1, marker2, and marker 3,
# are the position vectors (3 x 1 x n) of the chosen markers in the global
# coordinate system at Frame n.
# The origin (O_frame) of the segment is set at the center of the 3 chosen markers.
# The function return the origin (O_frame), the rotational matrix (R_frame) and the
# total number of frames in the static trial (y).
       
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
    O_frame = np.zeros((3,y))

    for i in range(y):
        O_frame[0:x, i] = (M1[0:x, i] + M2[0:x, i] + M3[0:x, i]) / 3

    Help1 = np.zeros((3, 1, y))
    X = np.zeros((3, 1, y))
    Y = np.zeros((3, 1, y))
    Z = np.zeros((3, 1, y))

    for i in range(y):
        X[0:x, 0, i] = M3[0:x, i] - M1[0:x, i]
        Help1[0:x, 0, i] = M2[0:x, i] - M1[0:x, i]
        Z[0:x, 0, i] = np.cross(X[0:x, 0, i], Help1[0:x, 0, i], axis = 0)
        Y[0:x, 0, i] = np.cross(Z[0:x, 0, i], X[0:x, 0, i], axis = 0)
        X[0:x, 0, i] = X[0:x, 0, i] / np.linalg.norm(X[0:x, 0, i])
        Y[0:x, 0, i] = Y[0:x, 0, i] / np.linalg.norm(Y[0:x, 0, i])
        Z[0:x, 0, i] = Z[0:x, 0, i] / np.linalg.norm(Z[0:x, 0, i])
    
    R_frame = np.concatenate((X, Y, Z), axis=1)
    return O_frame, R_frame, y

def get_localFrame_allInOne():
    global MRLOKALMEAN
    id1 = qtm.data.object.trajectory.find_trajectory(M1LABEL)
    id2 = qtm.data.object.trajectory.find_trajectory(M2LABEL)
    id3 = qtm.data.object.trajectory.find_trajectory(M3LABEL)
    marker1 = qtm.data.series._3d.get_samples(id1)
    marker2 = qtm.data.series._3d.get_samples(id2)
    marker3 = qtm.data.series._3d.get_samples(id3)
    Oframe, Rframe,frames = calculate_frame(marker1,marker2,marker3)

    # calculate the location of the marker that will be reconstructed
    # in the local segment (MRlokal).
    idMR = qtm.data.object.trajectory.find_trajectory(MRLABEL)
    marker = qtm.data.series._3d.get_samples(idMR)
    MR = []

    i=0
    while i < len(marker):
            frame = marker[i]
            frame_int = frame['position']
            MR.append(frame_int)
            i += 1

    MR = np.asarray(MR)
    MR = np.transpose(MR)

    i=0
    MRlokal = np.zeros((3,frames))
    for i in range(frames):
        MRlokal[0:3,i] = np.dot(np.transpose(Rframe[0:3,0:3,i]),(MR[0:3,i] - Oframe[0:3,i]))

    # calculate average postion troughout the static trial
    MRLOKALMEAN = np.mean(MRlokal, axis=1)
    print("Local frame defined and saved: ", MRLOKALMEAN)

def get_globalFrame_allInOne():
    # Load trajectories of the 3 defined markers in the dynamic trial.
    id1 = qtm.data.object.trajectory.find_trajectory(M1LABEL)
    id2 = qtm.data.object.trajectory.find_trajectory(M2LABEL)
    id3 = qtm.data.object.trajectory.find_trajectory(M3LABEL)
    marker1 = qtm.data.series._3d.get_samples(id1)
    marker2 = qtm.data.series._3d.get_samples(id2)
    marker3 = qtm.data.series._3d.get_samples(id3)
    Oframe2, Rframe2, frames2 = calculate_frame(marker1,marker2,marker3)

    # create the "new" reconstructed marker
    trajectory_label = MRLABEL + "_reconstructed"
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
        MRglobal[0:3,i] = np.dot(Rframe2[0:3,0:3,i], MRLOKALMEAN) + Oframe2[0:3,i]
        calculated_3d_data.append({"position": [MRglobal[0,i],MRglobal[1,i],MRglobal[2,i]], "residual": 0.0})

    qtm.data.series._3d.set_samples(trajectory_id, measured_range, calculated_3d_data)

def add_menu():
    add_command("set_marker_reconstruct", set_marker_reconstruct)
    add_command("set_marker_1", set_marker_1)
    add_command("set_marker_2", set_marker_2)
    add_command("set_marker_3", set_marker_3)
    add_command("get_localFrame_allInOne", get_localFrame_allInOne)
    add_command("get_globalFrame_allInOne", get_globalFrame_allInOne)

    menu_id = qtm.gui.insert_menu_submenu(None, "Reconstruct")
    qtm.gui.insert_menu_separator(menu_id)    
    add_menu_item(menu_id, "Set Marker Reconstruct", "set_marker_reconstruct")
    add_menu_item(menu_id, "Set Marker 1", "set_marker_1")
    add_menu_item(menu_id, "Set Marker 2", "set_marker_2")
    add_menu_item(menu_id, "Set Marker 3", "set_marker_3")
    add_menu_item(menu_id, "Get Local Frame All-in-One", "get_localFrame_allInOne")
    add_menu_item(menu_id, "Get Global Frame All-in-One", "get_globalFrame_allInOne")  

if __name__ == "__main__":
    add_menu()