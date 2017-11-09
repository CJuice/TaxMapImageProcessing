from arcpy import ExecuteError, GetMessages, management, env

# Was attempting to use a decorator on every geoprocessing tool run to capture geoprocessing exceptions and unnamed exceptions
# and to print them out without having the try: except: code be written multiple times. Tried to place this in the
# UtilityClass and access it but didn't find the way. Then moved the functions into the main script and it appeared
# to be somewhat correct but the tool failed to run. TypeError: 'NoneType' object is not callable. I switched the None to
# double quotes but it didn't work.

def captureAndPrintGeoprocessingErrors(func):

    def f(**kwargs):
        try:
            rv = func(**kwargs)
            return rv
        except ExecuteError:
            print "Error creating Raster Catalog.\n{}".format(GetMessages(2))
            return exit()
        except Exception as e:
            print e
            return exit()

@captureAndPrintGeoprocessingErrors
def runESRIGPTool(**kwargs):
    rv = management.CreateRasterCatalog(**kwargs)
    return rv

runESRIGPTool(out_path=env.workspace,
              out_name=strRasterCatalogName,
              raster_spatial_reference=objSpatialReferenceProjectedRaster,
              spatial_reference=objSpatialReferenceProjectedRaster,
              config_keyword=None,
              spatial_grid_1=0,
              spatial_grid_2=0,
              spatial_grid_3=0,
              raster_management_type="MANAGED",
              template_raster_catalog=None)