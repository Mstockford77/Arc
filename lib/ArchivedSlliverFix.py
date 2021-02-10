import arcpy
import datetime

def sets(extents, invdb):
    houseSetID = []
    seneateSetID = []
    congressSetID =[]
    cursor = [row for row in arcpy.da.SearchCursor(extents, "*")]
    for row in cursor:
        print row[2]
        congressSetID.append(row[2])
    del cursor
    print "Length of list is: ", len(congressSetID)
    congressSetID = set(congressSetID)
    print "New length of set is: ", len(congressSetID)
    print congressSetID
    cursor = [r for r in arcpy.da.UpdateCursor(y, "*")]
    i, k = 1, 1
    for r in cursor:
        if r[3] not in congressSetID:
            i += 1
        else:
            k += 1
    j = i + k
    print  "Total records:  ", j, " Total not on list: ", i, " Total on list: ", k
    del cursor
    dcursor = arcpy.da.UpdateCursor(y, "*")
    i = 1
    for row in dcursor:
        if row[3] not in congressSetID:
            dcursor.deleteRow()
            i += 1
    print "Deleted ", i, " rows."


def sliver_merge(in_layer, *layers):
    # Enable extension for data reviewer and overwriting output.
    arcpy.CheckOutExtension("datareviewer")
    arcpy.env.overwriteOutput = "true"
    gdb = in_layer
    print gdb
    layer = layers[0]
    sliver_list = in_layer
    i = 1
    # Set local variables
    objectid_list = []
    target = in_layer.rindex('/')
    out_path = in_layer[:target]
    print "out path is: ", out_path
    use_layer = out_path + "/HouseValidExtents"
    # use_layer = out_path + "/SenateValidExtents"
    # use_layer = out_path + "/CongressValidExtents"
    fields = ["EVENTID", "ROUTEID","FROMMEASURE","TOMEASURE"]
    # fields = "*"
    icursor = arcpy.da.InsertCursor(use_layer, fields)
    try:
        # Loop through the list of slivers.
        cursor = [r_sliver for r_sliver in arcpy.da.SearchCursor(layer, "*", where_clause='("to_measure" - "from_measure") <= 0.01 ')]
        with arcpy.da.SearchCursor(layer, fields) as cursor2:
            for row in cursor2:
                for r_sliver in cursor:
                    if row[1] == r_sliver[4] and r_sliver[5] == row[2] and r_sliver[6] == row[3]:
                        print r_sliver, "\n", row, i
                        if row[0] not in objectid_list:
                            objectid_list.append(row[0])
                            i += 1
                    else:
                        pass
        del cursor, cursor2
        for row in objectid_list:
            icursor.insertRow(row)
        # Stop the edit session and save the changes
        # edit.stopEditing(True)
    except Exception as er:
        print "Did not run.", er
    finally:
        print objectid_list, "\n", len(objectid_list)
        arcpy.CheckInExtension("datareviewer")
        return

# sliver_merge(data, v)

# data = "Y:/Inventory/Road Inventory Processes/Checks/Databases/Slivers_Checks.gdb/HouseSlivers"
# data = "Y:/Inventory/Road Inventory Processes/Checks/Databases/Slivers_Checks.gdb/SenateSlivers"
# data = "Y:/Inventory/Road Inventory Processes/Checks/Databases/Slivers_Checks.gdb/CongressSlivers"

"""
    with arcpy.da.UpdateCursor(valids, fields) as dcursor:
        for row in dcursor:
            if row[0] in fixed and row[1] in to_delete:
                if row
                print "row[0]: ", row[0], "row[1]: ", row[1], j
                j += 1
    k = 1
    for item in to_delete:
        print item, item[0], k
        k += 1
    print j
"""

