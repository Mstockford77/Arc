import arcpy
import datetime


def merger(slivers, valids):
    print datetime.datetime.now()
    workspace = 'Database Connections/RDINV.sde'

    # Start an edit session. Must provide the workspace.
    edit = arcpy.da.Editor(workspace)

    # Edit session is started without an undo/redo stack for versioned data
    #  (for second argument, use False for unversioned data)
    edit.startEditing(False, True)

    # Start an edit operation
    edit.startOperation()
    routes = []
    routemergers = []
    fixed = []
    to_delete = []
    delete_table = "Y:/Inventory/Road Inventory Processes/Checks/Databases/Slivers_Checks.gdb/dTableSenate"
    # "Y:/Inventory/Road Inventory Processes/Checks/Databases/Slivers_Checks.gdb/dTableCongress"
    # fields = ["EVENTID", "route_id","from_measure","to_measure"]
    fields = ["EVENTID", "ROUTEID","FROMMEASURE","TOMEASURE"]
    cursor = [slv for slv in arcpy.da.SearchCursor(slivers, fields)]
    icursor = arcpy.da.InsertCursor(delete_table, fields)
    with arcpy.da.UpdateCursor(valids, fields, where_clause='(FROMDATE is null or FROMDATE<=CURRENT_TIMESTAMP) and (TODATE is null or TODATE>CURRENT_TIMESTAMP)') as cursor2:
        for row in cursor2:
            for slv in cursor:
                if slv[1] == row[1] and slv[0] not in fixed:
                    if row[2] == slv[3]:
                        rowList = list(slv)
                        to_delete.append(rowList)
                        routes.append(["Sliver to valid", " sliver: ", slv[0], " valid: ", row[0]])
                        routemergers.append(routes)
                        row[2] = slv[2]
                        cursor2.updateRow(row)
                        fixed.append(slv[0])
                        routes = []
                    # valid ends sliver starts
                    elif row[3] == slv[2]:
                        rowList = list(slv)
                        to_delete.append(rowList)
                        routes.append(["Valid to sliver", slv[0], row[0]])
                        routemergers.append(routes)
                        row[3] = slv[3]
                        cursor2.updateRow(row)
                        fixed.append(slv[0])
                        routes = []
                    else:
                        pass
                else:
                    pass
    del cursor, cursor2
    q = 1
    for row in to_delete:
        icursor.insertRow(row)
        q += 1
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
    del cursor1, cursor2
    print "\n", len(routemergers), "\nNumber of fixed event ids: ", len(fixed)
    print "Length set fixed: ", len(set(fixed))
    print "Number to delete: ", q
    print valids
    # Stop the edit operation.
    edit.stopOperation()

    # Stop the edit session and save the changes
    edit.stopEditing(True)
    print datetime.datetime.now()


# v = "Database Connections/RDINV.sde/INVDB.OKHouseDistrict"
# w = "Database Connections/RDINV.sde/INVDB.OKSenateDistrict"
# x = "Database Connections/RDINV.sde/INVDB.USCongressDistrict"
# copy = "Y:/Inventory/Road Inventory Processes/Checks/Databases/Slivers_Checks.gdb/HouseCopy_4"
valids = "Database Connections/RDINV.sde/INVDB.OKSenateDistrict"
slivers = "Y:/Inventory/Road Inventory Processes/Checks/Databases/Slivers_Checks.gdb/SenateValids"
merger(slivers, valids)
