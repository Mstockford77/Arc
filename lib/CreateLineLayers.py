import arcpy
import datetime


def make_layer(reviewer_db, production_db):
    # Set variables to run Locate Events along Route tool.
    # Start by making a copy of the LRSN Road Network that is filtered with the time stamp def query.
    arcpy.env.overwriteOutput = "true"
    target = reviewer_db.rindex('/')
    string1 = reviewer_db[target:-11]
    print string1
    arcpy.MakeFeatureLayer_management(
        production_db + "/INVDB.LRSN_RoadNetwork",
        'useMe',
        where_clause="(FromDate is null or FromDate<=CURRENT_TIMESTAMP) and (ToDate is null or ToDate>CURRENT_TIMESTAMP)")
    arcpy.CopyFeatures_management('useMe', reviewer_db + '/useMe')
    in_features = reviewer_db + "/REVDATASET/REVTABLELINE"
    in_routes = reviewer_db + '/useMe'
    print "features", in_features, "\nroutes", in_routes
    route_id_field = "ROUTEID"
    radius_or_tolerance = "1 Feet"
    point_radius = "20 Feet"
    out_table_line = reviewer_db + "/LineRT"
    props_line = "RID LINE FMEAS TMEAS"
    arcpy.LocateFeaturesAlongRoutes_lr(in_features, in_routes, route_id_field, radius_or_tolerance, out_table_line,
                                       props_line, "#", "#", "ZERO", "FIELDS")
    # Set variables for joining tables.
    # (This is what allows review records to be paired with the routes the tool just located.)
    now = datetime.datetime.now()
    in_features = reviewer_db + "/REVDATASET/REVTABLELINE"
    layer_name = "Line_Checks"
    in_field = "LINKGUID"
    in_field2 = "LineRT.LINKGUID"
    join_table = out_table_line
    join_table2 = reviewer_db + "/REVTABLEMAIN"
    join_field = "LINKGUID"
    join_field2 = "ID"
    join_type = "KEEP_COMMON"
    save_layer = reviewer_db + string1 + "_Line_Review_" + ("%s_%s" % (now.month, now.day))
    arcpy.Delete_management(save_layer)
    # Make a layer and join the tables with errors and the route events.
    # For line events:
    arcpy.MakeFeatureLayer_management(in_features, layer_name)
    arcpy.AddJoin_management(layer_name, in_field, join_table, join_field)
    arcpy.AddJoin_management(layer_name, in_field2, join_table2, join_field2, join_type)
    # Save the layer to the gdb.
    arcpy.CopyFeatures_management(layer_name, save_layer)

    # If geo checks create point layer
    if string1 == '/Geo':
        # Point events are edited in Arc and don't need a route id.
        # Variables for point joins and layer.
        in_features_point = reviewer_db + "/REVDATASET/REVTABLEPOINT"
        now = datetime.datetime.now()
        in_field2 = "PointRT.LINKGUID"
        out_table_point = reviewer_db + "/PointRT"
        # join_table = out_table_point
        layer_name = "Point"
        in_field = "LINKGUID"
        join_table = reviewer_db + "/REVTABLEMAIN"
        join_field = "ID"
        save_layer1 = reviewer_db + "/Geo_Point_Review" + ("%s_%s" % (now.month, now.day))

        # Run joins for point events layer:
        arcpy.MakeFeatureLayer_management(in_features_point, layer_name)
        arcpy.AddJoin_management(layer_name, in_field, join_table, join_field)
        arcpy.CopyFeatures_management(layer_name, save_layer1)

    return save_layer


"""
gdb = "Y:/Inventory/Road Inventory Processes/Checks/Databases/Geo_Checks.gdb"
production_db = "Database Connections/RDINV_LOCKROUTE.sde"
x = make_layer(gdb, production_db)
print x
"""






