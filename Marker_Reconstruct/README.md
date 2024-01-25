# Marker_Reconstruct
Scripts to reconstuct a missing marker


Step 1: Define missing marker and adjacent markers

	Step 1.1:
	Open the static trial that was used in QTM
	Step 1.2:
	Select the marker that is missing in the dynamic trial and run the set_MarkerReconstruct script.
	Step 1.3:
	Unselect the missing marker and select the first of the adjacent markers. Run the set_Marker1 script.
	Steps 1.4 and 1.5
	Repeat for step 1.3 for the second and third adjacent markers (Run set_Marker2 and setMarker3).

Step 2: Calculate and store the local coordinate system	

	Step 2.1:
	Make sure the relevant static trial is still opened.
	Step 2.2:
	Run the set_LocalFrame_AllinOne script.

Step 3: Reconstruct the missing marker

	Step 3.1:
	Open the dynamic trial with the missing marker
	Step 3.2:
	Make sure all the markers are named in the same way as in the static trial.
	Step 3.3:
	Run the get_GlobalFrame_AllinOne script.
	
The missing marker will now be reconstructed and saved with the label from the staic trial 
and the additional suffix "_reconstructed".