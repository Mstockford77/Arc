import arcpy

def deleteSessions(reviewer_db, now):
    # arcpy.CheckOutExtension("datareviewer")
    # reviewer_db = "Y:/Inventory/Road Inventory Processes/Checks/Databases/Cross_Checks.gdb"
    date = now
    session_name = ("%s_%s_%s" % (date.year, date.month, date.day))
    print session_name
    # arcpy.CreateReviewerSession_Reviewer(reviewer_db, session_name)
    session_ID = ""
    path = reviewer_db + '/REVSESSIONTABLE'
    cursor = arcpy.da.SearchCursor(path, ['SESSIONID', 'SESSIONNAME'])
    for row in cursor:
        print row
        session = row[0]
        print session
        session_name = row[1]
        print session_name
        print "Session %d : %s" % (session, session_name)
        try:
            arcpy.DeleteReviewerSession_Reviewer(reviewer_db, "Session %d : %s" % (session, session_name))
        except:
            print "No delete required"

    print "Exited delete sessions."





