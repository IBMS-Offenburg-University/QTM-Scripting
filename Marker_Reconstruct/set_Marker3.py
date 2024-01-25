import qtm

# Set the third marker. Marker must be present in static and dynamic trial.
# Marker must be selected in the static trial in QTM.

selections = qtm.gui.selection.get_selections()
help = selections[0]
id = help['id']
M3label = qtm.data.object.trajectory.get_label(id)
print("Marker 3 set to: " + M3label)