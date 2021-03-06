import arcpy
import datetime
import os
import sys
import DeleteSession
import Excel as xls
import Check_Valids as valid
import CreateLineLayers as cL
import time

# Set sleep timer so script can be started and waits to run until weekly tasks are finished.
# time.sleep(9000)


start = datetime.datetime.now()

# Set log file path and create or overwrite existing file to begin the log
with open( "Y:/Inventory/Road Inventory Processes/Checks/Logs/Shoulder_logs.txt", "w" ) as logfile:
    logfile.write( "DataReviewerBatch_Events.py" + '\n\n' + "Start Time:\t" + str( start )[:-7] + '\n\n' )
    # Write the opening start time to logfile and close


# Define results writing function to record result messages in processing window and in logfile
def writeMsg( message ):
    arcpy.AddMessage( message )  # Add message to Results Window
    with open( "Y:/Inventory/Road Inventory Processes/Checks/Logs/Shoulder_logs.txt", "a") as logfile:
        # Open file in append mode
     logfile.write( message + '\n' )  # Write message to log file and close


# Enable extension for data reviewer and overwriting output.
arcpy.CheckOutExtension("datareviewer")
arcpy.env.overwriteOutput = "true"

# Set variables for running batches.
reviewer_db = "Y:/Inventory/Road Inventory Processes/Checks/Databases/Shoulder_Checks.gdb"
rbj_path = "Y:/Inventory/Road Inventory Processes/Checks/RBJs/Event_Checks/"
# Events 4 will be added once shoulders are updated.
# "Events1.rbj", "Events2.rbj", "Events3.rbj",  "Events5.rbj", "Null_Not_Null.rbj"
rbj = [ "Events4.rbj" ]
production_db = "Database Connections/RDINV_LOCKROUTE.sde"
production_workspaceversion = "INVDB.LOCK_ROUTE"

# Delete previous session:
# This will delete previous records and clean up the db
DeleteSession.deleteSessions(reviewer_db, start)

# Create a new session:
session_name = ("%s_%s_%s" % (start.year, start.month, start.day))
print session_name
session = str(arcpy.CreateReviewerSession_Reviewer(reviewer_db, session_name))
print session
writeMsg("\nSession Id:  " + session )

# Set loop to run and log the batch events, or errors if present.
for check in rbj:
    try:
        use_rbj = rbj_path + check
        now = datetime.datetime.now()
        writeMsg("\nStarting Batch job:  " + check + " at \n" + str(now)[:-7])
        res = arcpy.ExecuteReviewerBatchJob_Reviewer(
            reviewer_db,
            session,
            use_rbj,
            production_db,
            "",
            "",
            production_workspaceversion)
        now = datetime.datetime.now()
        arcpy.Delete_management("in_memory")
        writeMsg("\nFinished at:  " + str(now)[:-7])
    except Exception as err:
        writeMsg("\n Batch job did not work.\n\n")
        writeMsg(str( err ))

# Create line layer for use. Layer returns layer name for use in valid checks.
now = datetime.datetime.now()
writeMsg("\nStarting Line Table at: " + str(now)[:-7])
saveLayer = cL.make_layer(reviewer_db, production_db)
now = datetime.datetime.now()
writeMsg("\nFinished Line Table at: " + str(now)[:-7])

# Write Excel file
now = datetime.datetime.now()
writeMsg("\nStarting Excel table  for 0 length records: " + str(now)[:-7])
xls.makeExcel(reviewer_db)

# Check valid list
now = datetime.datetime.now()
writeMsg("\nChecking records against valid records table: " + str(now)[:-7])
valids.check_valid(reviewer_db, saveLayer)

# Script finish
now = datetime.datetime.now()
writeMsg("*********************************************")
writeMsg("\nScript finished running at: " + str(now)[:-7])

# Release data reviewer extension.
arcpy.CheckInExtension("datareviewer")

# Delete connection
arcpy.ClearWorkspaceCache_management()

"""
# Set variables to run Locate Events along Route tool.
# Start by making a copy of the LRSN Road Network that is filtered with the time stamp def query.
arcpy.MakeFeatureLayer_management(
    production_db +
    "/INVDB.LRSN_RoadNetwork",
    'useMe',
    where_clause="(FromDate is null or FromDate<=CURRENT_TIMESTAMP) and (ToDate is null or ToDate>CURRENT_TIMESTAMP)")
arcpy.CopyFeatures_management('useMe', reviewer_db + '/useMe')
in_features = reviewer_db + "/REVDATASET/REVTABLELINE"
in_routes = reviewer_db + '/useMe'
route_id_field = "ROUTEID"
radius_or_tolerance = "1 Feet"
point_radius = "20 Feet"
out_table_line = reviewer_db + "/LineRT"
props_line = "RID LINE FMEAS TMEAS"

# Write log of and run Locate Events tool
now = datetime.datetime.now()
writeMsg("\nStarting Line Table at: " + str(now)[:-7])
arcpy.LocateFeaturesAlongRoutes_lr(
    in_features,
    in_routes,
    route_id_field,
    radius_or_tolerance,
    out_table_line,
    props_line,
    "#", "#",
    "ZERO",
    "FIELDS")
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
saveLayer = reviewer_db + "/Shoulder_Line_Review"+ ("%s_%s" % (now.month, now.day))

# Make a layer and join the tables with the errors and the route events.
# For line events:
now = datetime.datetime.now()
writeMsg("\nStarting Line Table Join at: " + str(now)[:-7])
arcpy.MakeFeatureLayer_management(in_features, layerName)
arcpy.AddJoin_management(layerName, in_field, join_table, join_field)
arcpy.AddJoin_management(layerName, in_field2, join_table2, join_field2, join_type)

# Save the layer to the gdb.
arcpy.CopyFeatures_management(layerName, saveLayer)
"""
