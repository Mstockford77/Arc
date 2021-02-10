"""
This script was used to match slivers (records that measured 0.01 miles or less) to the next record on the route.
It was determined that the majority of these records were caused by spatial  appends that changed the value of the
record usually along a boundary or at an intersection at the beginning or ending of a route.  The script was designed to
match end points found with the query listed below directly from the layer to be changed.  The script then takes the the begin
or end point of the sliver, changes the value of the begin or end point of the next (valid) record to include the slivers
distance on the route, adds the sliver to a list of successfully found routes to merge, and finally deletes the sliver record.
This leaves only the valid record with the new length.  Any unsuccessful sliver to valid matches will remain in the layer
after the script has run. (The majority of these were routes whose entirety in smaller than the stated distance from the
query.

Query used on layer was:
(FromDate is null or FromDate<=CURRENT_TIMESTAMP) and (ToDate is null or ToDate>CURRENT_TIMESTAMP) AND
(ToMeasure - FromMeasure) < 0.01
"""



import arcpy
import datetime

# Defined as a function with the original intent of passing in multiple layers to check.
def merger(slivers, valid_attributes):
    print datetime.datetime.now()
    workspace = 'Database Connections/RDINV.sde'

    # Start an edit session. Must provide the workspace.
    edit = arcpy.da.Editor(workspace)

    # Edit session is started without an undo/redo stack for versioned data
    #  (for second argument, use False for unversioned data)
    edit.startEditing(False, True)

    # Start an edit operation
    edit.startOperation()
    
    # Set variables
    routes = []
    route_mergers = []
    fixed = []
    to_delete = []
    delete_table = "Y:/Inventory/Road Inventory Processes/Checks/Databases/Slivers_Checks.gdb/dTableCongress"
    # Set the fields to use.
    fields = ["EVENTID", "ROUTEID","FROMMEASURE","TOMEASURE"]
    # Create the cursors.  Works better if one of the cursors is used in memory as a list.
    cursor = [slv for slv in arcpy.da.SearchCursor(slivers, fields)]     # This line uses list comprehension to create the list using a cursor.
    icursor = arcpy.da.InsertCursor(delete_table, fields)  # This is the insert cursor that will create the delete table.
    with arcpy.da.UpdateCursor(valid_attributes, fields, where_clause='(FROMDATE is null or FROMDATE<=CURRENT_TIMESTAMP) and (TODATE is null or TODATE>CURRENT_TIMESTAMP)') as cursor2:
        for row in cursor2:
            for slv in cursor:
                if slv[1] == row[1] and slv[0] not in fixed:  # Checks RouteID to RouteID and if EventID already in Fixed list. 
                    if row[2] == slv[3]:  # sliver ends, valid starts
                        # Next line for readability only.  Changes slv to list from tuple
                        row_list = list(slv)
                        # Now it can be appended to the delete list.
                        to_delete.append(row_list)
                        # Append attributes to a route. (Done originally as a logic check.)
                        routes.append(["Sliver to valid", " sliver: ", slv[0], " valid: ", row[0]])
                        # Now append the route to a list of routes. (Allowed to check # of routes on list.)
                        route_mergers.append(routes)
                        # This is where the attribute is changed on the valid layer and updated.
                        row[2] = slv[2]
                        cursor2.updateRow(row)
                        # Append record to fixed list and set routs list back to an empty list.
                        fixed.append(slv[0])
                        routes = []
                    elif row[3] == slv[2]:  # valid ends, sliver starts
                        to_delete.append(list(slv))
                        routes.append(["Valid to sliver", slv[0], row[0]])
                        route_mergers.append(routes)
                        row[3] = slv[3]
                        cursor2.updateRow(row)
                        fixed.append(slv[0])
                        routes = []
                    else:
                        pass
                else:
                    pass
    # Delete the cursors.
    del cursor, cursor2

    # Set a counter and create the table of records to delete from the list.  Table will still be readable after program
    # runs while the list will not.
    q = 1
    for row in to_delete:
        icursor.insertRow(row)
        q += 1
    # Reset the counter and delete matching records from the actual layer.
    q = 1
    del icursor
    cursor1 = [slv for slv in arcpy.da.SearchCursor(delete_table, fields)]
    with arcpy.da.UpdateCursor(valids, fields) as cursor2:
        for row in cursor2:
            for slv in cursor1:
                if slv[1] == row[1] and slv[0] == row[0]:
                    cursor2.deleteRow()
                    print row, "\n", q
                    q += 1
                else:
                    pass
    # Delete the cursors.
    del cursor1, cursor2
    print "\nNumber of fixed event ids: ", len(fixed)
    # The next line is just to check that the list is only unique values.
    print "Length set fixed: ", len(set(fixed))
    print "Number to delete: ", q
    
    # Stop the edit operation.
    edit.stopOperation()

    # Stop the edit session and save the changes
    edit.stopEditing(True)
    print datetime.datetime.now()


# Set variables
valids = "Database Connections/RDINV.sde/INVDB.USCongressDistrict"
slivers = "Y:/Inventory/Road Inventory Processes/Checks/Databases/Slivers_Checks.gdb/CongressValids"
# Call function
merger(slivers, valids)

