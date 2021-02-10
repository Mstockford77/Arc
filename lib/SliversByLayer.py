import arcpy
import datetime
# from lib import DeleteSession
import DeleteSession
# from lib import Excel as xls
import Excel as xls
import Check_Valids as valid
import CreateLineLayers as cL
import time

# Set sleep timer so script can be started and waits to run until weekly tasks are finished.
# time.sleep(9000)
# Set variable for time stamp
now = datetime.datetime.now()

# Set log file path and create or overwrite existing file to begin the log
with open( "Y:/Inventory/Road Inventory Processes/Checks/Logs/SliversByLayer_logs.txt", "w" ) as logfile:
    logfile.write( "DataReviewerBatch_Geo.py" + '\n\n' + "Start Time:\t" + str( now )[:-7] + '\n\n' )
    # Write the opening start time to logfile and close
# [:-4]


# Define results writing function to record result messages in processing window and in logfile
def writeMsg( message ):
    arcpy.AddMessage( message )  # Add message to Results Window
    with open( "Y:/Inventory/Road Inventory Processes/Checks/Logs/SliversByLayer_logs.txt", "a") as logfile:
        # Open file in append mode
        logfile.write( message + '\n' )  # Write message to log file and close


# Enable data reviewer extension and allow over writes for output
arcpy.CheckOutExtension("datareviewer")
arcpy.env.overwriteOutput = "true"

# Set variables for running batch jobs
reviewer_db = 'Y:/Inventory/Road Inventory Processes/Checks/Databases/Slivers_Checks.gdb'
rbj_path = "Y:/Inventory/Road Inventory Processes/Checks/RBJs/Slivers/"
production_db = "Database Connections/RDINV_LOCKROUTE.sde"
production_workspaceversion = "INVDB.LOCK_ROUTE"

# Delete existing sessions
DeleteSession.deleteSessions(reviewer_db, now)

# Create a new session
start = datetime.datetime.now()
session_name = ("%s_%s_%s" % (start.year, start.month, start.day))
print session_name
session = str(arcpy.CreateReviewerSession_Reviewer(reviewer_db, session_name))
print session
writeMsg("\nSession Id:  " + session )

# Batch jobs to run.
# ********************************************************************************************************
# Use this line for Highways and Functionally classified roads
rbj = [ "LayerByLayer1.rbj", "LayerByLayer2.rbj", "LayerByLayer3.rbj", "LayerByLayer4.rbj" ]

# ********************************************************************************************************
# Use this for locals, ramps and frontage roads
# rbj = [ "LocalSlivers.rbj" ]
writeMsg("\nSession Id:  " + session )
# Run batch jobs.  This will loop through the batch jobs in rbj variable.
# Each iteration should log the check being run, begin, and end time.
for check in rbj:
    try:
        use_rbj = rbj_path + check
        now = datetime.datetime.now()
        writeMsg("\nStarting Batch job:  " + check + " at " + str(now)[:-7])
        res = arcpy.ExecuteReviewerBatchJob_Reviewer(
            reviewer_db,
            session,
            use_rbj,
            production_db,
            "",
            "",
            production_workspaceversion)
        arcpy.Delete_management("in_memory")
        now = datetime.datetime.now()
        writeMsg("\nFinished at:  \t\t" + str(now)[:-7])
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
valid.check_valid(reviewer_db, saveLayer)

# Script finish
now = datetime.datetime.now()
writeMsg("\nScript finished running at: " + str(now)[:-7])

# Release extension
arcpy.CheckInExtension("datareviewer")

# Delete connection
arcpy.ClearWorkspaceCache_management()

"""
# Set variables to run Locate Events along Route tool.
# Start by making a copy of the LRSN Road Network that is filtered with the time stamp def query.
arcpy.MakeFeatureLayer_management(
    production_db + "/INVDB.LRSN_RoadNetwork",
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
    "#",
    "#",
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
saveLayer = reviewer_db + "/Line_Review"+ ("%s_%s" % (now.month, now.day))

# Create a layer and join tables with errors to the route events.
# For line events:
now = datetime.datetime.now()
writeMsg("\nStarting Line Table Join at: " + str(now)[:-7])
arcpy.MakeFeatureLayer_management(in_features, layerName)
arcpy.AddJoin_management(layerName, in_field, join_table, join_field)
arcpy.AddJoin_management(layerName, in_field2, join_table2, join_field2, join_type)

# Save the layer to the gdb
arcpy.CopyFeatures_management(layerName, saveLayer)

"""

