from arcpy import ExecuteError, GetMessages, management, env

# Specific to the Step 2 process
# Stored in Utility Class as static method
# def captureAndPrintGeoprocessingErrors(func):
#     from arcpy import ExecuteError, GetMessages
#
#     def f(*args, **kwargs):
#         try:
#             rv = func(*args, **kwargs)
#         except ExecuteError:
#             print "Error creating Raster Catalog.\n{}".format(GetMessages(2))
#             return exit()
#         except Exception as e:
#             print e
#             return exit()
#         return rv
#
#     return f
#
# Created in main processing script.
# @captureAndPrintGeoprocessingErrors
# def runESRIGPTool(*args, **kwargs):
#     rv = management.CreateRasterCatalog(*args, **kwargs)
#     return rv
#
# runESRIGPTool(out_path=env.workspace,
#               out_name=strRasterCatalogName,
#               raster_spatial_reference=objSpatialReferenceProjectedRaster,
#               spatial_reference=objSpatialReferenceProjectedRaster,
#               config_keyword=None,
#               spatial_grid_1=0,
#               spatial_grid_2=0,
#               spatial_grid_3=0,
#               raster_management_type="MANAGED",
#               template_raster_catalog=None)

# Testing Decorators
def outer(func):
    def f(*args, **kwargs):
        try:
            rv = func(*args, **kwargs)
        except Exception as e:
            print e
            return exit()
        return rv
    return f

@outer
def printArgs(*args, **kwargs):
    for arg in args:
        print "arg - {}".format(arg)
    for kwarg in kwargs:
        print "kwarg - {}".format(kwarg)


# printArgs([1,2,3,4,56], name="Saron", occupation="bot")
printArgs(name="Saron", occupation="bot")


# STORING CODE from Processing script that is the old style, sans Decorators. Keeping for comfort.
# try:
#     # Create Raster Catalog in workspace
#     management.CreateRasterCatalog(out_path=env.workspace,
#                                    out_name=strRasterCatalogName,
#                                    raster_spatial_reference=objSpatialReferenceProjectedRaster,
#                                    spatial_reference=objSpatialReferenceProjectedRaster,
#                                    config_keyword=None,
#                                    spatial_grid_1=0,
#                                    spatial_grid_2=0,
#                                    spatial_grid_3=0,
#                                    raster_management_type="MANAGED",
#                                    template_raster_catalog=None)
# except ExecuteError:
#     print "Error creating Raster Catalog.\n{}".format(GetMessages(2))
#     exit()
# except Exception as e:
#     print e
#     exit()

# try:
#     management.WorkspaceToRasterCatalog(env.workspace,
#                                         strRasterCatalogName,
#                                         include_subdirectories=None,
#                                         project=None)
# except ExecuteError:
#     print "Geoprocessing error loading workspace into {}.\n{}".format(strRasterCatalogName,GetMessages(2))
#     exit()
# except Exception as e:
#     print e
#     exit()

# try:
#     management.ProjectRaster(in_raster=objImage.getFilePath_Original(),
#                              out_raster=objImage.getFileName_lower(),
#                              out_coor_system=objSpatialReferenceProjectedRaster,
#                              resampling_type=None,
#                              cell_size=None,
#                              geographic_transform="NAD_1983_To_WGS_1984_1",
#                              Registration_Point=None,
#                              in_coor_system=None)
#     print "Re-Project successful.\n----------"
# except ExecuteError:
#     print "Geoprocessing error during Project Raster for {}. Skipping file.\n{}".format(objImage.getFileName_lower(),GetMessages(2))
#     lsUnsuccessfulImageReProjections.append(objImage.getFileName_lower())
# except Exception as e:
#     print e

# try:
#     management.DefineProjection(in_dataset=objImage.getFilePath_Original(),
#                                 coor_system=intDefineProjectionCode)
# except ExecuteError:
#     print "Geoprocessing error during Define Projection for image {}.\n{}".format(objImage.getFileName_lower(),GetMessages(2))
# except Exception as e:
#     print e