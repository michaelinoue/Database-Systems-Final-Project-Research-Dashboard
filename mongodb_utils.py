from pprint import pprint
from bson.son import SON

import pymongo

mongo_db = None


def init_mongodb():
    client_router = pymongo.MongoClient('localhost', port=27017, directConnection=True)
    global mongo_db
    mongo_db = client_router.academicworld
    create_Index()


def create_Index():
    global mongo_db
    mongo_db.publications.create_index(
        [('year', pymongo.ASCENDING), ('keywords.name', pymongo.ASCENDING)],
        name='year_keywords'
    )
    mongo_db.publications.create_index(
        [('year', pymongo.ASCENDING), ('keywords.name', pymongo.ASCENDING), ('id', pymongo.ASCENDING)],
        name='year_keywords_id'
    )
    mongo_db.publications.create_index(
        [('id', pymongo.ASCENDING)],
        name='id'
    )
    mongo_db.publications.create_index(
        [('year', pymongo.ASCENDING)],
        name='year'
    )
    mongo_db.faculty.create_index(
        [('name', pymongo.ASCENDING)]
    )
    mongo_db.faculty.create_index(
        [('publications', pymongo.ASCENDING)]
    )
    mongo_db.faculty.create_index(
        [('affiliation.name', pymongo.ASCENDING)],
        name='affiliation_name'
    )


def create_keyword_year_view(keyword_name, year1, year2):
    global mongo_db
    view_name = f"{keyword_name}_{year1}_{year2}_publications_view"
    try:
        # Create a view to match publications by keyword name, start/end year
        mongo_db.create_collection(view_name,
                                   viewOn="publications",
                                   pipeline=[{
                                       '$match': {
                                           'keywords.name': keyword_name,
                                           'year': {
                                               '$gte': year1,
                                               '$lte': year2
                                           }
                                       }
                                   }])
        return view_name
    except:
        # View already exists
        return view_name


def get_keyword_popularity_over_time(keyword_name, year1, year2):
    global mongo_db
    pipeline = [
        {'$match': {'keywords.name': keyword_name, 'year': {'$gte': year1, '$lte': year2}}},
        {'$project': {'_id': 0, 'year': 1, 'score': {'$sum': {
            '$map': {'input': {'$filter': {'input': '$keywords', 'cond': {'$eq': ['$$this.name', keyword_name]}}},
                     'as': 'k', 'in': '$$k.score'}}}}},
        {'$group': {'_id': '$year', 'keyword score': {'$sum': '$score'}}},
        {'$sort': {'_id': 1}},
        {'$project': {'_id': 0, 'year': '$_id', 'keyword score': 1}}
    ]
    cursor = mongo_db.publications.aggregate(pipeline)
    return list(cursor)


def get_school_topic_popularity_over_time(keyword_name, university_name, year1, year2):
    global mongo_db
    pipeline = [
        {
            '$match': {
                'keywords.name': keyword_name,
                'year': {
                    '$gte': year1,
                    '$lte': year2
                }
            }
        }, {
            '$lookup': {
                'from': 'faculty',
                'localField': 'id',
                'foreignField': 'publications',
                'as': 'faculty'
            }
        }, {
            '$unwind': '$faculty'
        }, {
            '$match': {
                'faculty.affiliation.name': university_name
            }
        }, {
            '$project': {
                '_id': 0,
                'year': 1,
                'score': {
                    '$sum': {
                        '$map': {
                            'input': {
                                '$filter': {
                                    'input': '$keywords',
                                    'cond': {
                                        '$eq': [
                                            '$$this.name', keyword_name
                                        ]
                                    }
                                }
                            },
                            'as': 'k',
                            'in': '$$k.score'
                        }
                    }
                }
            }
        }, {
            '$group': {
                '_id': '$year',
                'keyword score': {
                    '$sum': '$score'
                }
            }
        }, {
            '$project': {
                '_id': 0,
                'year': '$_id',
                'keyword score': 1
            }
        }, {
            '$sort': {
                'year': 1
            }
        }
    ]
    cursor = mongo_db.publications.aggregate(pipeline)
    return list(cursor)


def get_researcher_publication_count(researcher, keyword_name, year1, year2):
    global mongo_db
    view_name = create_keyword_year_view(keyword_name, year1, year2)
    pipeline = [
        {
            '$lookup': {
                'from': 'faculty',
                'localField': 'id',
                'foreignField': 'publications',
                'as': 'faculty'
            }
        }, {
            '$unwind': '$faculty'
        },
        {
            '$match': {
                'faculty.name': researcher,
            }
        }, {
            '$project': {
                '_id': 0,
                'year': 1,
                'pub_count': {
                    '$sum': 1
                }
            }
        }, {
            '$group': {
                '_id': '$year',
                'publication count': {
                    '$sum': '$pub_count'
                }
            }
        }, {
            '$project': {
                '_id': 0,
                'year': '$_id',
                'publication count': 1
            }
        }, {
            '$sort': {
                'year': 1
            }
        }
    ]
    cursor = mongo_db[view_name].aggregate(pipeline)
    return list(cursor)
