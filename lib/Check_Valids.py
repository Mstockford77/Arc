import arcpy

"""
This script uses a list of data checks verified by reviewers and removes them from new runs of the data check.
The idea is that this will save time in the future as we will no longer need to re-verify checks that have 
already been verified as accurate but were flagged and will continue to be flagged in each new run of the 
data checks.

This module should take in the check geodatabase, the list of valids for that data base, and the line review
layer that we use to check data.

The script will go line by line over the valid table and look for a match of items in that row:
1st: item 15 is the type of data check
2nd: item 5 is the route id
3rd: item 6 is the beginning mile point of the record

Keeping in mind that mileages may change due to cartographic realignments I will probably add rounding to 3 or 4 digits.

Once satisfied that the script works as planned I will change it to accept the geodatabase, valid and line tables
as arguments from the running script and this will be done automatically during the batch run.

*** All of the print functions below are to verify the script is checking for the right things and do not effect the 
outcome of the script.

"""


def check_valid(in_gdb, new_list):
    # Enable extension for data reviewer and overwriting output.
    arcpy.CheckOutExtension("datareviewer")
    arcpy.env.overwriteOutput = "true"

    gdb = in_gdb

    valid_list = gdb + "/Valids"
    target = gdb.rindex('/')
    string1 = in_gdb[target:-11]
    print string1
    # new_list = gdb + string1 + 'Checked_Line_Review'+
    print new_list
    records = []
    record = []

    print(valid_list)
    i = 1
    # The try catch below allows the script to finish and exit if no valid list exist in the gdb.
    try:
        with arcpy.da.SearchCursor(valid_list, '*') as cursor:
            for r in cursor:
                # print row[5], row[6], row[7], row[15]
                # Next line prints check type and route id of valid list.
                # print r[5], round(r[6], 3), r[17]
                with arcpy.da.UpdateCursor(new_list, '*') as update_cursor:
                    for row in update_cursor:
                        if row[17] == r[17] and row[5] == r[5] and round(row[6], 3) == round(r[6], 3):
                            update_cursor.deleteRow()
                            print i
                            i += 1

        del cursor
    except Exception as er:
        print "Did not run.", er
    finally:
        arcpy.CheckInExtension("datareviewer")
        return





"""
# update_cursor.deleteRow() will go here when functional instead of the print below.
                            print 'Object: ', row[0], 'routed ID: ', row[5], 'is a match for record ', i, \
                                'rounded = ', round(r[6], 3)
                            i += 1

gdb = 'Y:/Inventory/Road Inventory Processes/Checks/Databases/Geo_Checks.gdb'
list = gdb  + '/Geo_Line_Review_1_8'
check_valid(gdb, list)
print 'done'
# reviewer_db = "Y:/Inventory/Road Inventory Processes/Checks/Databases/Cross_Checks.gdb"
# reviewer_db = "Y:/Inventory/Road Inventory Processes/Checks/Databases/Geo_Checks.gdb"

# Running from inside module to make sure everything still works.
# The function call will be run from inside the batch run script just like below.
# check_valid(reviewer_db)


string1 = 'cross_line_review'
string2 = 'cross_checks.gdb'
string3 = string1.strip('_')
string4 = string2[:-11]
print string4
I used this to build a list of valids to check before using an update cursor inside a search cursor.
        if len(record) == 0:
            record.append(row[15])
            record.append(row[5])
            record.append(row[6])
            record.append(row[7])
            records.append(record)
            record = []

"""