import psycopg2

# functions for creating and executing queries 
class Fdb():

    # general purpose function to execute queries passed through a string
    # initiates connection, executes a query and ends connection
    # for SELECT queries, returns result if they are found and False if they are not
    def dbDo(query):
        conn = psycopg2.connect("dbname = fdb")
        cc = conn.cursor()
        cc.execute(query)
        # for SELECT queries only:
        if (query.find("SELECT") > -1):
            result = cc.fetchall()
            if (isinstance(result, list) and (len(result) > 0)):
                return result
            else:
                return False
        conn.commit()
        conn.close()
        cc.close()

    # forms a query to alter values for an entity using a nested list of key:value pairs
    #   value_list: list of keys and values for entity instance being inserted
    #       in the form of [ [key, value], [key, value], [key, value], ...]
    #.      taken from dictionary format
    #   tablename: name of entity being altered
    def insert_values(value_list, tablename):

        # iterates through list of values and forms a string query from them
        # returns the 
        def insert_query(value_list, tablename):
            column_string = "("
            value_string = "("
            for value_pair in value_list:
                col = value_pair[0]
                val = str(value_pair[1])
                if val.find("'") > -1:
                    val = val.replace("'", "\"")
                current_index = value_list.index(value_pair)
                last_index = len(value_list) - 1
                if current_index == last_index:
                    column_string += col
                    value_string += "'" + str(val) + "'"
                else:
                    column_string += col + ", "
                    value_string += "'" + val + "', "
            query_string = ("INSERT INTO " + tablename + " " + column_string +
                ") VALUES " + value_string + ");")
            return(query_string)

        query = insert_query(value_list, tablename)
        result = Fdb.dbDo(query)
        return result

    # updates values for a specific attribute of an entity
    #   columnname:
    #   newvalue:
    #   condition_list:
    #.  tablename:
    def update_values(columnname, newvalue, condition_list, tablename):
        def update_value_list(columnname, newvalue, pairs, tablename):
            q1 = "UPDATE " + tablename
            q2 = " SET " + columnname + "='" + str(newvalue)+ "' WHERE "
            q3 = ""
            for pair in pairs:
                q3 += str(pair[0]) + "='" + str(pair[1]) + "'"
                if not pairs.index(pair) == len(pairs) - 1:
                    q3 += " AND "
                else:
                    q3 += ";"
            return(q1 + q2 + q3)

        query = update_value_list(columnname, newvalue, condition_list, tablename)
        result = Fdb.dbDo(query)
        return result

    def select_values(match_list, value_list, tablename):
        def colString(match_list):
            if match_list:
                col_string = ""
                for col in match_list:
                    col = str(col)
                    col_string += col
                    if ((match_list.index(col)) < (len(match_list) - 1)):
                        col_string += ", "
                return col_string
            else:
                return "id"

        def valueString(value_list):
            match_string = ""
            for pair in value_list:
                pair[1] = str(pair[1])
                if not (pair[1].find("'") == -1):
                    pair[1] = pair[1].replace("'", "\"")
                if (value_list.index(pair) == 0):
                    match_string += (pair[0] + "='" + pair[1] + "'")
                else:
                    match_string += " AND " + pair[0]
                    match_string += "='" + pair[1] + "'"
            return match_string

        query = ""
        col_string = colString(match_list)
        query += "SELECT " + col_string + " FROM " + tablename
        if value_list:
            match_string = valueString(value_list)
            query += " WHERE " + match_string
        query += ";"
        result = Fdb.dbDo(query)
        return result

    def match_values(value_list, tablename):
        result = Fdb.select_values(False, value_list, tablename)
        if result:
            return True
        else:
            return False


# contains functions to manipulate start and end dates
# 
class Temporal():

    # creates a dictionary format of a 
    def show_date_info(dd):
        ed = {}
        ed['date'] = dd['date']
        ed['month'] = dd['month']
        ed['year'] = dd['year']
        ed['hour'] = "23"
        ed['min'] = "59"
        ed['sec'] = "59"
        return ed

    # 
    def parse_date(date_string):
        date = {}
        date["default_end"] = date_string[:11] + "23:59:59.00Z"
        date["date"] = date_string[8:10]
        date["month"] = date_string[5:7]
        date["year"] = date_string[:4]
        date["hour"] = date_string[11:13]
        date["min"] = date_string[14:16]
        date["sec"] = "00"
        return date

# 
class Format():
    # 
    def string_to_list(list_string):
        list_string = list_string[1:-1]
        if list_string.find(",") > 0:
            newlist = list_string.split(", ")
            return list_string
        else:
            return [list_string]

class Status():
    def final_changes(inserts, updates):
        if changes:
            print("\n" + str(changes) + " SUCCESSFUL CHANGES MADE TO DATABASE")
        elif updates:
            print("\n" + str(changes) + " UPDATES MADE TO DATABASE")
        if (changes or updates):
            print("DATABASE UPDATE SUCCESS\n")
        else:
            print("\nNO CHANGES MADE TO DATABASE\n")

    def table_inserts(changes, table_name):
        if changes > 0:
            print(str(changes) + " INSERTS MADE TO TABLE: " + table_name)

    def table_updates(changes, table_name):
        if changes > 0:
            print(str(changes) + " UPDATES MADE TO TABLE: " + table_name)

class Given():

    show_dict_list = []

    class Venue():

        show_venues_data1={
            "id": 1,
            "name": "The Musical Hop",
            "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
            "address": "1015 Folsom street",
            "city": "San Francisco",
            "state": "CA",
            "phone": "123-123-1234",
            "website": "https://www.themusicalhop.com",
            "facebook_link": "https://www.facebook.com/TheMusicalHop",
            "seeking_talent": True,
            "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
            "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
            "past_shows": [{
                "artist_id": 1, #edited to fit serial primary_key modification from previous value of 4
                "artist_name": "Guns N Petals",
                "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
                "start_time": "2019-05-21T21:30:00.000Z"
            }],
            "upcoming_shows": [],
            "past_shows_count": 1,
            "upcoming_shows_count": 0,
        }

        show_venues_data2={
          "id": 2,
          "name": "The Dueling Pianos Bar",
          "genres": ["Classical", "R&B", "Hip-Hop"],
          "address": "335 Delancey street",
          "city": "New York",
          "state": "NY",
          "phone": "914-003-1132",
          "website": "https://www.theduelingpianos.com",
          "facebook_link": "https://www.facebook.com/theduelingpianos",
          "seeking_talent": False,
          "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
          "past_shows": [],
          "upcoming_shows": [],
          "past_shows_count": 0,
          "upcoming_shows_count": 0,
        }

        show_venues_data3={
            "id": 3,
            "name": "Park Square Live Music & Coffee",
            "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
            "address": "34 Whiskey Moore Ave",
            "city": "San Francisco",
            "state": "CA",
            "phone": "415-000-1234",
            "website": "https://www.parksquarelivemusicandcoffee.com",
            "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
            "seeking_talent": False,
            "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
            "past_shows": [{
                "artist_id": 2, #edited to fit serial primary_key modification from previous value of 5
                "artist_name": "Matt Quevedo",
                "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
                "start_time": "2019-06-15T23:00:00.000Z"
            }],
                "upcoming_shows": [{
                "artist_id": 3, #edited to fit serial primary_key modification from previous value of 6
                "artist_name": "The Wild Sax Band",
                "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
                "start_time": "2035-04-01T20:00:00.000Z"
            }, {
                "artist_id": 3, #edited to fit serial primary_key modification from previous value of 6
                "artist_name": "The Wild Sax Band",
                "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
                "start_time": "2035-04-08T20:00:00.000Z"
            }, {
                "artist_id": 3, #edited to fit serial primary_key modification from previous value of 6
                "artist_name": "The Wild Sax Band",
                "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
                "start_time": "2035-04-15T20:00:00.000Z"
            }],
                "past_shows_count": 1,
                "upcoming_shows_count": 1,
            }

        params = ["name", "city", "genres", "address", "city", "state", "phone", "image_link", "facebook_link", "seeking_talent", "num_shows", "shows"]

        dicts = [show_venues_data1, show_venues_data2, show_venues_data3]

    class Artist():

        show_artists_data1={
            "id": 1, #edited to fit serial primary_key modification from previous value of 4
            "name": "Guns N Petals",
            "genres": ["Rock n Roll"],
            "city": "San Francisco",
            "state": "CA",
            "phone": "326-123-5000",
            "website": "https://www.gunsnpetalsband.com",
            "facebook_link": "https://www.facebook.com/GunsNPetals",
            "seeking_venue": True,
            "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
            "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
            "past_shows": [{
            "venue_id": 1,
            "venue_name": "The Musical Hop",
            "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
            "start_time": "2019-05-21T21:30:00.000Z"
            }],
            "upcoming_shows": [],
            "past_shows_count": 1,
            "upcoming_shows_count": 0,
            }

        show_artists_data2={
            "id": 2, #edited to fit serial primary_key modification from previous value of 5
            "name": "Matt Quevedo",
            "genres": ["Jazz"],
            "city": "New York",
            "state": "NY",
            "phone": "300-400-5000",
            "facebook_link": "https://www.facebook.com/mattquevedo923251523",
            "seeking_venue": False,
            "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
            "past_shows": [{
            "venue_id": 3,
            "venue_name": "Park Square Live Music & Coffee",
            "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
            "start_time": "2019-06-15T23:00:00.000Z"
            }],
            "upcoming_shows": [],
            "past_shows_count": 1,
            "upcoming_shows_count": 0,
            }

        show_artists_data3={
            "id": 3, #edited to fit serial primary_key modification from previous value of 6
            "name": "The Wild Sax Band",
            "genres": ["Jazz", "Classical"],
            "city": "San Francisco",
            "state": "CA",
            "phone": "432-325-5432",
            "seeking_venue": False,
            "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
            "past_shows": [],
            "upcoming_shows": [{
                "venue_id": 3,
                "venue_name": "Park Square Live Music & Coffee",
                "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
                "start_time": "2035-04-01T20:00:00.000Z"
            }, {
                "venue_id": 3,
                "venue_name": "Park Square Live Music & Coffee",
                "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
                "start_time": "2035-04-08T20:00:00.000Z"
            }, {
                "venue_id": 3,
                "venue_name": "Park Square Live Music & Coffee",
                "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
                "start_time": "2035-04-15T20:00:00.000Z"
            }],
                "past_shows_count": 0,
                "upcoming_shows_count": 3,
            }

        params = ["name", "genres", "city", "state", "phone", "website", "facebook_link", "seenking_venue", "seeking_description", "image_link", "shows"]

        dicts = [show_artists_data1, show_artists_data2, show_artists_data3]

    genre_list = []

class Populate():


    class Prep():
        def show_data(tablename, id, name, image_link, show_dict_list):
            if tablename == "artist":
                id_key = "artist_id"
                name_key = "artist_name"
                image_key = "artist_image_link"
            elif tablename == "venue":
                id_key = "venue_id"
                name_key = "venue_name"
                image_key = "venue_image_link"
            for show_dict in show_dict_list:
                show_dict[id_key] = id
                show_dict[name_key] = name
                show_dict[image_key] = image_link
                Given.show_dict_list.append(show_dict)

    def literal_data(given_dict_list, params, tablename):
        inserts = 0
        for given_dict in given_dict_list:
            insert_list = []
            show_dict_list = []
            # add all given values to insert list
            for artist_key in given_dict:
                artist_value = given_dict[artist_key]
                if isinstance(artist_value, list):
                    if (artist_key == "genres"):
                    # format genre to make it insertable
                        Given.genre_list.append([artist_value, tablename, given_dict['id']])
                        insert_list.append([artist_key, artist_value])
                    elif len(artist_value) > 0:
                    # add show entry to show entry list
                        for item in artist_value:
                            show_dict_list.append(item)
                elif (artist_key in params):
                    insert_list.append([artist_key, artist_value])
            name_match = [['name', given_dict['name']]]
            if not (Fdb.match_values(name_match, tablename)):
                Fdb.insert_values(insert_list, tablename)
                inserts += 1
                id = Fdb.select_values(False, name_match, tablename)[0][0]
            else:
                id = Fdb.select_values(False, name_match, tablename)[0][0]
            Populate.Prep.show_data(tablename, id, given_dict['name'], given_dict['image_link'], show_dict_list)
        Status.table_inserts(inserts, tablename)
        return inserts

    def show_data():
        inserts = 0
        for listing in Given.show_dict_list:
            show_dict_list = []
            for item in listing:
                show_key = item
                show_value = str(listing[item])
                show_dict_list.append([show_key, show_value])
                if show_key == "start_time":
                    sd_dict = Temporal.parse_date(show_value)
                    ed_dict = Temporal.show_date_info(sd_dict)
                    for t in sd_dict:
                        if not (t == "default_end"):
                            show_dict_list.append([("start_" + t), sd_dict[t]])
                        else:
                            show_dict_list.append(["end_time", sd_dict[t]])
                    for t in ed_dict:
                        show_dict_list.append([("end_" + t), ed_dict[t]])
            if not (Fdb.match_values(show_dict_list, "show")):
                Fdb.insert_values(show_dict_list, "show")
                inserts += 1
        return inserts

    def area_list(listing, tablename):
        city = listing['city']
        state = listing['state']
        name = city + ", " + state
        insert_list = [['city', city],
            ['state', state],
            ['name', name]]
        if (tablename == 'venue'):
            venue_id = listing['id']
            return (insert_list, venue_id)
        elif (tablename == 'artist'):
            artist_id = listing['id']
            return (insert_list, artist_id)

    def venue_areas(listing_tuple, tablename):
        select_key = tablename + "s"
        inserts = 0
        updates = 0
        if Fdb.match_values(listing_tuple[0], 'area'):
            result = Fdb.select_values([select_key], listing_tuple[0],
                'area')[0][0]
            if result:
                result = Format.string_to_list(result)
                if not (str(listing_tuple[1]) in result):
                    result.append(listing_tuple[1])
                    result = str(result).replace("'", "")
                    Fdb.update_values(select_key, result, listing_tuple[0],
                        "area")
                    updates += 1
            else:
                Fdb.update_values(select_key, [listing_tuple[1]],
                    listing_tuple[0], "area")
        else:
            insert_list = listing_tuple[0]
            insert_list.append([select_key, [listing_tuple[1]]])
            Fdb.insert_values(insert_list, "area")
            inserts += 1
        area_id = Fdb.select_values(['id'], listing_tuple[0], 'area')[0][0]
        return (inserts, updates, area_id)

    def area():
        inserts = 0
        updates = 0
        artist_updates = 0
        venue_updates = 0
        for listing in Given.Venue.dicts:
            result = Populate.area_list(listing, "venue")
            id = result[1]
            result = Populate.venue_areas(result, "venue")
            inserts += result[0]
            updates += result[1]
            area_id = result[2]
            if not (Fdb.select_values(['area_id'], [['id', id]], "venue")[0][0]):
                Fdb.update_values('area_id', area_id, [['id', id]], "venue")
                venue_updates += 1
        for listing in Given.Artist.dicts:
            result = Populate.area_list(listing, "artist")
            id = result[1]
            result = Populate.venue_areas(result, "artist")
            inserts += result[0]
            updates += result[1]
            area_id = result[2]
            if not (Fdb.select_values(['area_id'], [['id', id]], "artist")[0][0]):
                Fdb.update_values('area_id', area_id, [['id', id]], "artist")
                artist_updates += 1
        Status.table_inserts(inserts, "area")
        Status.table_updates(updates, "area")
        Status.table_updates(venue_updates, "venue")
        Status.table_updates(artist_updates, "artist")
        return inserts + updates

    def genre():
        inserts = 0
        for item in Given.genre_list:
            for genre in item[0]:
                insert_list = [['name', genre], ['reference_type', item[1]],
                    ['reference_id', item[2]]]
                if not Fdb.match_values(insert_list, "genre"):
                    if not Fdb.match_values([['name', genre]], "gref"):
                        Fdb.insert_values([['name', genre]], "gref")
                    Fdb.insert_values(insert_list, "genre")
                    inserts += 1
        Status.table_inserts(inserts, "genre")
        return inserts

    def schedule():
        inserts = 0
        show_info = Fdb.select_values(['id', 'start_date', 'start_month',
            'start_year', 'venue_id', 'artist_id'], False, "show")
        for result_list in show_info:
            match_list = [['date', result_list[1]],
                ['month', result_list[2]],
                ['year', result_list[3]]]
            insert_list = [['show_ids', [result_list[0]]],
                ['venue_ids', [result_list[4]]],
                ['artist_ids', [result_list[5]]],
                ['reference_id', result_list[0]],
                ['reference_type', "given show"],
                ['multiday_event', False]] + match_list
            if not Fdb.match_values(match_list, "schedule"):
                Fdb.insert_values(insert_list, "schedule")
                inserts += 1
            else:
                result = Fdb.select_values(['id'], match_list, "schedule")
        Status.table_inserts(inserts, "schedule")
        return inserts

changes = 0
inserts = 0
changes += Populate.literal_data(Given.Artist.dicts, Given.Artist.params, "artist")
changes += Populate.literal_data(Given.Venue.dicts, Given.Venue.params, "venue")
changes += Populate.show_data()
changes += Populate.area()
changes += Populate.genre()
changes += Populate.schedule()

Status.final_changes(changes, inserts)