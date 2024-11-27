# QTM-Scripting

Python Scripts for QTM

## What is in this repository
This repository contains useful scripts for QTM.
1. Marker_Reconstruct contains the old version of Marker_Reconstruct.
2. Marker_Reconstruct_2_0 contains a tool that can reconstruct a missing marker basen on a static trial.
3. gap_fill contains a tool that relational gap fills all gaps in a selected marker (the tool is based on the gap_fill script from qualisys).

## How to use the different tools
2. Marker_Reconstruct_2_0:
  	Step 1: Define missing marker and adjacent markers

	    Step 1.1:
	    Open the static trial that was used in QTM
	    Step 1.2:
	    Select the marker that is missing in the dynamic trial and select the menu item "Set Marker Reconstruct" in the "Reconstruct" menu.
	    Step 1.3:
	    Unselect the missing marker and select the first of the adjacent markers. Select the menu item "Set Marker 1".
	    Steps 1.4 and 1.5
	    Repeat for step 1.3 for the second and third adjacent markers (Select the menu item "set Marker 2" and "Set Marker 3").

    Step 2: Calculate and store the local coordinate system	

	    Step 2.1:
	    Make sure the relevant static trial is still opened.
	    Step 2.2:
	    Select the menu item "Get LocalFrame All-in-One".

    Step 3: Reconstruct the missing marker

	    Step 3.1:
	    Open the dynamic trial with the missing marker
	    Step 3.2:
	    Make sure all the markers are named in the same way as in the static trial.
	    Step 3.3:
	    Select the menu item "Get GlobalFrame All-in-One".
	
  The missing marker will now be reconstructed and saved with the label from the staic trial and the additional suffix "_reconstructed".
  
3. gap_fill:
   Step 1: Select the marker that you want to fill
   Step 2: Select the menu item "Relational Gap Fill - Multi Pass" in the "GapFill" menu.
   Step 3: Check the filled gaps.

## Installing modules such as numpy
1. Open a command prompt window (as administrator):
    - Go to the QTM installation folder, usually "C:\Program Files\Qualisys\Qualisys Track Manager"
    - Invoke the pip installer with a command like this, "python -m pip install numpy"
    
## Documentation
https://qualisys.github.io/qtm-scripting/

## External Links
1. [qtm-scripting from Qualisys](https://github.com/qualisys/qtm-scripting.git)
2. [www.python.org](https://www.python.org/)
