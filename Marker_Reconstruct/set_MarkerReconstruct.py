import qtm

# Set the marker that will be reconstructed. Marker must be present in static and should be
# missing in the dynamic trial. Marker must be selected in the static trial in QTM.

selections = qtm.gui.selection.get_selections()
help = selections[0]
id = help['id']
MRlabel = qtm.data.object.trajectory.get_label(id)
print("Missing Marker set to: " + MRlabel)