import arcpy
import datetime
import os
import sys
from lib import DeleteSession
from lib import Excel as xls


start = datetime.datetime.now()

# Set log file path and create or overwrite existing file to begin the log
with open( "Y:/Inventory/Road Inventory Processes/Checks/Logs/ZeroLength_Logs.txt", "w" ) as logfile:
    logfile.write( "DataReviewerBatch_Cross.py" + '\n\n' + "Start Time:\t" + str( start )[:-7] + '\n\n' )	# Write the opening start time to logfile and close
# [:-4]

# Define results writing function to record result messages in processing window and in logfile
def writeMsg( message ):
    arcpy.AddMessage( message )  # Add message to Results Window
    with open( "Y:/Inventory/Road Inventory Processes/Checks/Logs/ZeroLength_Logs.txt", "a") as logfile: # Open file in append mode
     logfile.write( message + '\n' )  # Write message to log file and close


# Enable extension for data reviewer and overwriting output.
arcpy.CheckOutExtension("datareviewer")
arcpy.env.overwriteOutput = "true"

# Set variables for running batches.
reviewer_db = "Y:/Inventory/Road Inventory Processes/Checks/Databases/ZeroLengths.gdb"
rbj_path = "Y:/Inventory/Road Inventory Processes/Checks/RBJs/ZeroLength/"
production_db = "Database Connections/RDINV_LOCKROUTE.sde"

# Batch for all records current and historical
# rbj = ["All_Records.rbj" ]

# Batch for current records only
rbj = ["ZeroLengthExtent.rbj"]


# Delete existing sessions
DeleteSession.deleteSessions(reviewer_db, start)

# Create a new session
session_name = ("%s_%s_%s" % (start.year, start.month, start.day))
print session_name
session = str(arcpy.CreateReviewerSession_Reviewer(reviewer_db, session_name))
writeMsg("\nSession Id:  " + session )
print session

# Set loop to run and log the batch events, or errors if present.
for check in rbj:
    try:
        use_rbj = rbj_path + check
        now = datetime.datetime.now()
        writeMsg("\nStarting Batch job:  " + check + " at " + str(now)[:-7])
        res = arcpy.ExecuteReviewerBatchJob_Reviewer(reviewer_db, session, use_rbj, production_db)
        now = datetime.datetime.now()
        arcpy.Delete_management("in_memory")
        writeMsg("\nFinished at:  " + str(now)[:-7])
    except Exception as err:
        writeMsg("\n Batch job did not work.\n\n")
        writeMsg(str( err ))
"""
# Set variables to run Locate Events along Route tool.
in_features = reviewer_db + "/REVDATASET/REVTABLELINE"
in_routes = production_db + "/INVDB.LRSN_RoadNetwork"
route_id_field = "ROUTEID"
radius_or_tolerance = "1 Feet"
point_radius = "25 Feet"
out_table_line = reviewer_db + "/LineRT"
props_line = "RID LINE FMEAS TMEAS"
# arcpy.env.overwriteOutput = "true"
# Write log of Locate Events tool
now = datetime.datetime.now()
writeMsg("\nStarting Line Table at: " + str(now)[:-7])
arcpy.LocateFeaturesAlongRoutes_lr(in_features, in_routes, route_id_field, radius_or_tolerance, out_table_line,
                                   props_line, "#", "#", "ZERO", "FIELDS")
now = datetime.datetime.now()
writeMsg("\nFinished Line Table at: " + str(now)[:-7])

# Set variables for joining tables.
# (This is what allows review records to be paired with the routes the tool just located.)
in_join_features = in_features
layerName = "Line_Checks"
in_field = "LINKGUID"
in_field2 = "LineRT.LINKGUID"
join_table = out_table_line
join_table2 = reviewer_db + "/REVTABLEMAIN"
join_field = "LINKGUID"
join_field2 = "ID"
join_type = "KEEP_COMMON"
saveLayer = reviewer_db + "/ZeroLength_Line_Review"
# Make a layer and join the tables with errors and the route events.
# For line events:
now = datetime.datetime.now()
writeMsg("\nStarting Line Table Join at: " + str(now)[:-7])
arcpy.MakeFeatureLayer_management(in_features, layerName)
arcpy.AddJoin_management(layerName, in_field, join_table, join_field)
arcpy.AddJoin_management(layerName, in_field2, join_table2, join_field2, join_type)

# Save the layer to the gdb.
arcpy.CopyFeatures_management(layerName, saveLayer)
"""
# Write Excel file
xls.makeExcel('ZeroLengths.gdb')


# Script finish
now = datetime.datetime.now()
writeMsg("*********************************************")
writeMsg("\nScript finished running at: " + str(now)[:-7])

# Release data reviewer extension.
arcpy.CheckInExtension("datareviewer")

# Delete connection
arcpy.ClearWorkspaceCache_management()