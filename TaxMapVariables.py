#Created on 20180122. Centralizing variables to reduce redundancy, code bloat, imports, and make revisions easier.
from datetime import date
from arcpy import SpatialReference

# COMMON TO BOTH
strDateTodayNoDashes = str(date.today()).replace("-", "")
strPSAProcessComplete = "Process complete."
lsImageObjects = []
strLogFileName = "LOG_TaxMapProcessing.log"

#_____________________________________________________________________________________________________________________
#PRE-PROCESSING VARIABLES
    # General
strNewImageFolderEnding = "_AllTaxMapImages"
strReportFileEnding = "_TaxMapReportFile.csv"
strFileExtensionsPresentInImageDatasets = "File extensions present in image datasets: {}"
strPSA_Processing = "Processing..."
strPSA_WritingReport = "Writing CSV report file...\n"
strPSA_ProcessingCompleteSeeReport = "Pre-Processing Complete. Please visit your report and review the contents.\n\tREPORT LOCATION > {}\n"
strPSA_ConsolidatedImageFilesLocation = "\tCONSOLIDATED IMAGE FILES PATH > {}\n"
strPSA_MoveToStepTwoProcess = "If the images files looks satisfactory, based on the report findings, type a 'y' to run Step 2 now. Type 'n' to stop.\n>"
strPSA_YESResponseToMoveToStepTwo = "y"
    # Report file headers
strFileNameHeader = "Filename_lowercase"
strHasTFWHeader = "HasTFW"
strBitDepthHeader = "BitDepth"
strProjectionHeader = "Projection"
strFeetVsMetersVsOtherHeader = "TFW_SuggestedUnit"
strXYPixelSizeHeader = "XY_PixelSize"
    # Input prompt messages
strPromptForImageDirectoryPath = "Paste the path for the directory of .tif files you want to process\n>"
strPromptForNewImageDirectoryPath = "Paste the path where a new folder will be created and will hold a copy of all images for processing\n>"
strPromptForProceedWithKnownPresentFileExtensions = "Proceed? (y/n)\n>"
    # Error messages
strErrorMsgImageFileDirectoryInvalid = "Image file directory appears to be invalid.\n{}"
strErrorMsgNewFolderCreationFail = "Error creating new folder.\n{}"
strErrorMsgNewImageDirectoryInvalidOrExists = "The new directory appears to be invalid or already exists.\n{}"
strErrorMsgWalkingDirectoryCheckingExtensionsFail = "Error walking directory and checking file extensions.\n{}"
strErrorMsgFileAlreadyExistsInLocation = "File [{}] already exists in new location."
strErrorMsgMovingFilesFail = "Error while moving files.\n{}"
strGPErrorMsgBitDepthCheckFail = "Geoprocessing error during image {} bit depth check: {}"
strGPErrorMsgSpatialReferenceCheckFail = "Geoprocessing error during image {} spatial reference check: {}"
strErrorMsgBuildingReportFail = "Error while building report data.\n{}"
strErrorMsgOpeningWritingCSVFileFail = "Error opening/writing to report file.\n{}"
    # Collections
lsAcceptableExtensionsForImageFilesOfInterest = ["tif","tfw","tif.xml"]
lsFileNamesTIF = []
lsFileNamesTFW = []
dictTFWCheck = {}
dictReportData = {}
setOfFileExtensions = None

#_____________________________________________________________________________________________________________________
# PROCESSING VARIABLES
    # General
strConsolidatedImageFileFolderPath = None
strGeodatabaseWorkspacePath = None
strRasterCatalogName = "RCmanaged_{}".format(strDateTodayNoDashes)
strPSADefiningProjection = "Defining projection... {}"
strPSAReProjecting = "Re-Projecting... {}"
strPSAWorkspaceToRasterCatalog = "Loading workspace into raster catalog..."
strPSAListOfFailedReProjections = "The following list of lowercase filenames did not Re-Project\n{}"
strGeographicTransformationNAD83_WGS84 = "NAD_1983_To_WGS_1984_1"
strRasterManagementType = "MANAGED"
intDefineProjectionCode = 26985 # WKID 2248 is feet, WKID 26985 is meters
intProjectRasterCode = 3857 # WKID 3857 is web mercator
objSpatialReferenceProjectedRaster = SpatialReference(intProjectRasterCode)
    # Input prompt messages
strPromptForConsolidatedImageFileFolderPath = "Paste the path to the folder containing the consolidated image files.\n>"
strPromptForGeodatabaseWorkspacePath = "Paste the path to the workspace (geodatabase).\n>"
    # Error messages
strErrorMsgPathInvalid = "Path does not appear to exist. \n{}\n"
strErrorMsgWalkingDirectoryAndObjectCreationFail = "Error walking directory and creating Image object.\n{}"
    # Collections
lsTifFilesInImagesFolder = []
lsUnsuccessfulImageReProjections = []
