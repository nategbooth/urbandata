import csv
import sys
import re

from pymongo import MongoClient

connection_string = "mongodb+srv://uda_prueba_usuario:eficaciacomunicacionentusiasmo@cluster0.shwu1ii.mongodb.net/?retryWrites=true&w=majority"


def add_to_database(inmueble_objects):
    client = MongoClient(connection_string)
    db = client.inmueble
    inmuebles_collection = db.inmuebles
    print("Adding %d objects to db" % len(inmueble_objects))
    result = inmuebles_collection.insert_many(inmueble_objects)
    print("Successfully inserted %d objects" % len(result.inserted_ids))


# I didn't finish this because it seemed a bit silly but it would be more succinct considering many fields need to be filtered the same way.
def fix_field(field, contents):
    if field in {'build_status', 'date_diff', 'property_type', 'end_week', 'typology_type', 'id'}:
        return int(contents)
    else:
        return contents

def convert_row_to_inmueble_object(row):
    return {
        # I am assuming right now that id_uda is the unique MongoDB ID.
        '_id': row['id_uda'],
        'other_id': int(re.sub('[^A-Za-z0-9]+', '', row['id'])), # there are more efficient ways but this was easy
        'title': row['title'],
        'description': row['description'],
        'x_coord': float(row['coordinates'].split(',')[0]),
        'y_coord': float(row['coordinates'].split(',')[1]), # this is not efficient but I don't think it matters
        'is_active': row['is_active'].lower() == "true", # this will give False for nonsense data, but I think that's fine
        'build_status': int(row['build_status']),
        'start_month': int(row['start_month']),
        'construction_type': None if row['construction_type'].lower() in {'null', 'none'} else int(row['construction_type']),
        'date_diff': int(row['date_diff']),
        'date_in': row['date_in'],
        'property_type': int(row['property_type']),
        'end_week': int(row['end_week']),
        'typology_type': int(row['typology_type']),
        'boundary_id': int(row['boundary_id']),
        'listing_type': int(row['listing_type']),
        'date': row['date'],
    }


# Takes a command line argument for the CSV file, sanitizes only the types of error seen in the assets.csv file, and then adds them to my MongoDB database in Atlas.
if __name__ == "__main__":
    with open(sys.argv[1]) as assets_file:
        reader = csv.DictReader(assets_file)
        inmuebles_to_add_to_db = []
        for row in reader:
            if not row.get('id'):
                print("skipping row with no id")
                continue
            inmueble_object = convert_row_to_inmueble_object(row)
            print("inmueble object:", inmueble_object)
            inmuebles_to_add_to_db.append(inmueble_object)

    # Adding all inmuebles at once so you don't have duplicates if it crashes halfway through the CSV and you need to run it again
    add_to_database(inmuebles_to_add_to_db)
