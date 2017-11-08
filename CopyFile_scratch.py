# Move all files to master location
import os, UtilityClass
from sys import exit
classUtilClass = UtilityClass.UtilityClassFunctionality()

strInputFileDirectory = r"E:\TaxMapsProject\Testing\TestFileCopy"
strNewFolderPath = r"E:\TaxMapsProject\Testing\TestFileCopy\newfolder1"
os.mkdir(strNewFolderPath)
# if os.path.exists(strNewFolderPath):
#     print "exists"
# else:
#     print "doesn't exist"
# try:
#     for (dirname, dirs, files) in os.walk(strInputFileDirectory):
#         print files
#         for file in files:
#             tupFileNameParts = file.split(".")
#             classUtilClass.copyImageFileToLocation(file, strNewFolderPath)
#             # if ("tfw" in tupFileNameParts[1].lower()) or ("tif" in tupFileNameParts[1].lower()):
#             #     print "step 1"
#             #     classUtilClass.copyImageFileToLocation(file, strNewFolderPath)
#             # else:
#             #     continue
# except:
#     print "Error copying file: {}".format(file)
#     exit()
import shutil
# import os
source = os.listdir(strInputFileDirectory)
print "source: {}".format(source)
destination = strNewFolderPath
print "destination: {}".format(destination)

for files in source:
    files = files.lower()
    if files.endswith(".tfw") or files.endswith(".tif"):
        strFilePath = os.path.join(strInputFileDirectory,files)
        strFileDestination = os.path.join(destination, files)
        print "strFileDestination: {}".format(strFileDestination)
        shutil.move(strFilePath, strFileDestination)
