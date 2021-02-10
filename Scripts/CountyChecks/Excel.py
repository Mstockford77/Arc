import arcpy
import os
import sys
import datetime

def makeExcel(inGDB):
    # Enable extension for data reviewer and overwriting output.
    # arcpy.CheckOutExtension("datareviewer")
    arcpy.env.overwriteOutput = "true"
    print inGDB

    # Set local variables
    in_data = inGDB + "/REVTABLEMAIN"
    print in_data
    out_data = inGDB + "/NoGeometry"
    print out_data
    # in_data = "Y:/Inventory/Michael/" + inGDB + "/REVTABLEMAIN"
    # out_data = "Y:/Inventory/Michael/" + inGDB + "/NoGeometry"

    # Execute Copy
    arcpy.Copy_management(in_data, out_data)

    dcursor = arcpy.da.UpdateCursor(out_data, '*')

    with arcpy.da.UpdateCursor(out_data, "*") as cursor:
        for row in cursor:
            if row[4] == 'Feature Record':
                cursor.deleteRow()
    with arcpy.da.SearchCursor(out_data, "*") as cursor:
        for row in cursor:
            # if row[4] == 'Feature Record':
            print row
    now = datetime.datetime.now()
    run = str(now)[:-16]
    in_table = out_data
    # out_xls = "Y:/Inventory/Road Inventory Processes/Checks/Logs/"+ run + str(inGDB)[:-4] + "Review_Table.xls"
    out_xls = str(inGDB)[:-4] + "Review_Table.xls"

    arcpy.TableToExcel_conversion(in_table, out_xls)
    return





