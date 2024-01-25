import qtm
import numpy as np

selections = qtm.gui.selection.get_selections()
help = selections[0]
id = help['id']
MRlabel = qtm.data.object.trajectory.get_label(id)