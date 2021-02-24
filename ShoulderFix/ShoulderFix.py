"""
This script was used to update inside shoulder type and width to match outside shoulder type and width for events
that have null values for inside shoulder width and type and outside shoulder type of "No Shoulder".  This was done
to update the system as previously inside shoulder type and width was left Null on roads with "No Shoulder" as the outside
shoulder type if the inside shoulder was of the same type.

Query used on layer was:
"(FromDate is null or FromDate<=CURRENT_TIMESTAMP) and (ToDate is null or ToDate>CURRENT_TIMESTAMP) AND
INSIDESHOULDERTYPE IS NULL AND OUTSIDESHOULDERTYPE = 0"

120356 records updated using this script.
"""

import arcpy
import datetime


# Defined as a function with the original intent of passing in multiple layers to check.
def merger(shoulders):
    print datetime.datetime.now()
    workspace = 'Database Connections/Test.sde'
    now = datetime.datetime.now()
    # Start an edit session. Must provide the workspace.
    edit = arcpy.da.Editor(workspace)
    now = time.strftime('%d/%m/%Y')
    # print now
    # Edit session is started without an undo/redo stack for versioned data
    #  (for second argument, use False for unversioned data)
    edit.startEditing(False, True)
    # Start an edit operation
    edit.startOperation()
    # Set variables
    # Set the fields to use.
    fields = ['ROUTEID', 'ESTABLISHEDDATE', 'INSIDESHOULDERTYPE', 'INSIDESHOULDERWIDTH', 'OUTSIDESHOULDERTYPE', 'OUTSIDESHOULDERWIDTH', 'LAST_EDITED_USER', 'LAST_EDITED_DATE']
    # Set counter for testing or tracking purposes.
    i = 1
    wc = "(FromDate is null or FromDate<=CURRENT_TIMESTAMP) and (ToDate is null or ToDate>CURRENT_TIMESTAMP) AND INSIDESHOULDERTYPE IS NULL AND OUTSIDESHOULDERTYPE = 0"
    # Create the cursor.
    with arcpy.da.UpdateCursor(shoulders, fields, where_clause=wc) as cursor:
        for row in cursor:
            # Set row variables to be updated to the value of the update.
            row[1] = str(now)
            row[2] = 0
            row[3] = 0
            row[6] = 'MSTOCKFORD'
            row[7] = str(now)
            cursor.updateRow(row)
            print i
            i += 1

    # Delete the cursor.
    del cursor
    # Stop the edit operation.
    edit.stopOperation()
    # Stop the edit session and save the changes
    edit.stopEditing(True)


# Set variables
x = "Database Connections/Test.sde/INVDBTEST.Shoulder"
# Call function
merger(x)