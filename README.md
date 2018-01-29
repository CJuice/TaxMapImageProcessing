# Tax Map Image Processing
### Summary
Scripts automating the Tax Map Image Processing process for MD DoIT GIS group. Images are received from MDP.
###  Description
Multi-step process run through a GUI and command window interaction. Step 1 is the pre-processing step designed to 
examine image files, detect quality issues by report on key characteristics. Once quality is gauranteed, the
 the images are processed by Step 2.
###### General Stepwise Description of Functionality
Step 1:
* Inputs
    1. Directory path for the image files.
    2. Directory path for output .csv file.
* Checks
    1. File extensions present in image directory.
        1. Display list of extensions to user and ask for permission to proceed.
        2. No .zip files should be present.
    2. If each image (.tif) has an associated world file (.tfw).
    3. The bit depth of each image.
    4. The projection of each image.
    5. The units of the raster (feet/meters/other).
    6. The dimensions of the pixels.
* Actions
    1. Move all image files to a new consolidated location
* Outputs
    1. Report file in .csv format.
        1. User should inspect report before proceeding to step 2.

Step 2:
* Inputs
    1. Directory path for the consolidated image files.
    2. Directory path for the ESRI geodatabase workspace.
* Actions
    1. Define the projection of each image.
    2. Create Raster Catalog.
    3. Project each image file to workspace as WGS84 Web Mercator.
    4. Load workspace into raster catalog.
* Outputs
    1. New raster dataset for each image.
    2. New raster catalog containing all raster datasets.
### Instructions to Run
1. Download the program files.
2. Right-Click on TaxMapProcessGUI.py and create a shortcut. Open the properties of the shortcut and edit the 
    Shortcut>Target:> value to be [path to python executable] space [path to TaxMapProcessGUI.py file]. Click OK to 
    close the properties window.
3. Double click the shortcut to trigger the process.
4. When the GUI loads
    1. Enter the path for the image files.
    2. Enter the path where a new .csv file will be created.
    3. Click the button to 'Run Step 1'. Control moves to a python window.  
    3. Enter 'y' or 'n' in response to a request to continue with the file extensions discovered in the image
     file directory. Press Enter.
    4. Enter 'y' or 'n' in response to a request to continue with Step 2 or exit.
        1. If 'n' is entered, the process will terminate. To re-initiate, after quality issues have been resolved, double
        click the shortcut. Fill in the forms for Step 2 and click the buttton 'Run Step 2 ONLY'. Control moves to a python
        window.
        2. if 'y' is entered, follow the prompts to enter the path to the consolidated image files, and the path to the 
        geodatabase workspace.

*During each step, if the program is running successfully, you should see several print statements about the processes
    underway, and then a print statement that indicates the process is complete.  Nearly all print
    messages are also written to the process log file. Once complete, navigate to the 
    geodatabase workspace and view the raster catalog containing the processed tax map images.*