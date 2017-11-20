# Tax Map Image Processing
### Summary
Scripts automating the Tax Map Image Processing process for MD DoIT GIS group. Images are received from the MDP.
###  Description
Two python scripts and associated class files. Step 1 is the pre-processing step designed to examine the image files
before they are processed by Step 2.
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
2. Open a command window in the same directory that this script is saved - hold shift and right-click anywhere
    in the directory, choose 'open command window here'. Type 'python TaxMapPRE_Processing.py' and Press Enter.
     1. This only works if you have already added the Python directory path to the system environment variable 
     path (Windows). If you have not done this, you need to do so or you need to use an IDE to run this script, 
     such as IDLE or PyCharm, etc. You may also try running it as an executable (double-click). (Borrowed from @jwhaney)
3. When prompted during Step 1
    1. Enter the path for the image files. Press Enter.
    2. Enter the path where a new .csv file will be created. Press Enter.    
    3. Enter 'y' or 'n' in response to a request to continue with the file extensions discovered in the image
     file directory. Press Enter.
    4. Enter 'y' or 'n' in response to a request to continue with Step 2 or exit.
4. When prompted during Step 2
    1. Enter the path for the consolidated image files. Press Enter.
    2. Enter the path for the geodatabase workspace. Press Enter.    

*During each step, if the program is running successfully, you should see several print statements about the processes
    underway, and then a print statement that indicates the process is complete. Once complete, navigate to the 
    geodatabase workspace and view the raster catalog containing the processed tax map images.*