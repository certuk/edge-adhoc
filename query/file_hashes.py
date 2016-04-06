from mongoengine.connection import get_db

def get_file_hashes_xsi(data):
    if not data:
        raise Exception("No file hashes supplied")
    matches_cursor = get_db().stix.aggregate([
        {
            '$match': {
                'data.summary.type': 'FileObjectType'
            }
        },
        {
            '$unwind': '$data.api.object.properties.hashes'
        },
        {
            '$match': {
                'data.api.object.properties.hashes.type': {
                    '$in': data}
            }
        },
        {
            '$group': {
                '_id':'$data.api.object.properties.hashes.type',
                'objects': {
                    '$push': '$_id'
                }
            }
        },
        {
            '$sort': {'_id':1}
        }
    ], cursor={})

    return matches_cursor


def get_file_hashes_no_xsi(data):
    if not data:
        raise Exception("No file hashes supplied")
    matches_cursor = get_db().stix.aggregate([
        {
            '$match': {
                'data.summary.type': 'FileObjectType'
            }
        },
        {
            '$unwind': '$data.api.object.properties.hashes'
        },
        {
            '$match': {
                'data.api.object.properties.hashes.type.value': {
                    '$in': data
            }
            }
        },
        {
            '$group': {
                '_id':'$data.api.object.properties.hashes.type.value',
                'objects': {
                    '$push': '$_id'
                }
            }
        },
        {
            '$sort': {'_id':1}
        }
    ], cursor={})

    return matches_cursor
