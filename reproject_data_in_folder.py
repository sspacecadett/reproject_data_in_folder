import arcpy
from arcpy import SpatialReference as sr
import os

target_folder = arcpy.GetParameterAsText(0)
target_proj = arcpy.GetParameterAsText(1)
target_sr = arcpy.Describe(target_proj).spatialReference

# Empty list to store datasets which have been reprojected
report = []

try:
    arcpy.env.workspace = target_folder
    shapefiles = arcpy.ListFeatureClasses("*.shp")

    for shp in shapefiles:
        in_sr = arcpy.Describe(shp).spatialReference
        out_name = os.path.splitext(shp)[0] + "_projected.shp"
        out_path = os.path.join(target_folder, out_name)

        if os.path.exists(out_path):
            arcpy.AddMessage("Shapefile skipped (already exists): {}".format(out_name))
            continue

        if in_sr.name != target_sr.name:
            arcpy.AddMessage("Currently reprojecting {}".format(shp))
            arcpy.Project_management(
                shp, 
                out_path,
                target_sr
                )
            report.append(out_name)
            
    if report:
        arcpy.AddMessage("Projected: " + ", ".join(report))
    else: 
        arcpy.AddMessage("No files needed projection.")

except Exception as e:
    arcpy.AddMessage("Failed to run: {}".format(e))