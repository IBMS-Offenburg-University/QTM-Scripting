import qtm

# Set the first marker. Marker must be present in static and dynamic trial.
# Marker must be selected in the static trial in QTM.

selections = qtm.gui.selection.get_selections()
help = selections[0]
id = help['id']
M1label = qtm.data.object.trajectory.get_label(id)
print("Marker 1 set to: " + M1label)