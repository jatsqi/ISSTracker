import redis
from Backend.Core.dataStructs import parseTimeToTimestamp, ISSDBKey, Astronaut
from Backend.Requests import astrosOnISS

class redisDB:
    # establishing connection to redisDB
    __redisHost__ = "localhost"
    __redisDB__ = redis.StrictRedis(host=__redisHost__, port=6379, db=0, decode_responses=True)

    # push current ISS postition to DB
    def _setIsspos(self, data):
        # IssPos object (data):
        # {'latitude': -45.4742, 'longitude': 150.3883, 'timestamp': '2020-06-09 20-50-01'}
        with self.__redisDB__ as DB:
            # set Key and Value
            DB.set(name="ISSpos:" + data["timestamp"] + ":latitude", value=data["latitude"])
            DB.set(name="ISSpos:" + data["timestamp"] + ":longitude", value=data["longitude"])

            # key expires after 24h
            DB.expire(name="ISSpos:" + data["timestamp"], time=86400)


    def _getISS(self, requestData):

        # converting Timestamps from requests to actual Timestamps
        startTime = parseTimeToTimestamp(requestData["params"]["startTime"])
        endTime = parseTimeToTimestamp(requestData["params"]["endTime"])

        # define empty Key set (mathematische Menge)
        keyset = set()

        with self.__redisDB__ as DB:

            # Generating search pattern from request parameters
            searchPattern = "ISSpos" + ":" + requestData["params"]["startTime"].split(" ")[0] + "*"

            # Get all keys from DB which match previously defined keyset
            startTimeKeys = DB.keys(pattern=searchPattern)

            # add keys to keyset
            for key in startTimeKeys:
                splitted = str(key).split(':')

                # create new ISSDBKey object which holds all values (timestamp for this key is automaticly converted)
                currKeyObject = ISSDBKey(timeValue=splitted[1], key=splitted[2].strip("'"), value=None)

                # only add keys which are in the range of [startTime, endTime]
                if currKeyObject.timestamp >= startTime and currKeyObject.timestamp <= endTime:
                    # adding key to keyset
                    keyset.add(currKeyObject)

            # same code as for startTime -> see comments above for explanations
            searchPattern = "ISSpos" + ":" + requestData["params"]["endTime"].split(" ")[0] + "*"
            endTimeKeys = DB.keys(pattern=searchPattern)
            for key in endTimeKeys:
                splitted = str(key).split(':')  # [0] = requestName; [1] = timestamp; [2] = param
                currKeyObject = ISSDBKey(timeValue=splitted[1], key=splitted[2].strip("'"), value=None)
                if currKeyObject.timestamp >= startTime and currKeyObject.timestamp <= endTime:
                    keyset.add(currKeyObject)

            # convert keyset into a sorted list, sorted by timestamps
            keylist = sorted(keyset, key=lambda x: x.timestamp)

            # get values from DB
            for key in keylist:
                key.value = DB.get("ISSpos:" + key.timeValue + ":" + key.key)
            return keylist

    def _getGeoJsonSingel(self, countryname):
        with self.__redisDB__ as DB:
            # initialize return dict
            returnValue = {"countryname": countryname}

            # generate search pattern
            searchPattern = "GeoJson:" + countryname + ":*"

            # get keys
            keys = DB.keys(searchPattern)

            # build return dict from DB
            for i in range(len(keys) // 2):
                returnValue[str(i)] = {
                    "latitude": DB.get(name="GeoJson:" + countryname + ":" + str(i) + ":latitude"),
                    "longitude": DB.get(name="GeoJson:" + countryname + ":" + str(i) + ":longitude")
                }
            return returnValue

    def _getGeoJson(self, requestdata):
        with self.__redisDB__ as DB:

            if not requestdata["params"]["country"] == "all":
                return self._getGeoJsonSingel(countryname=requestdata["params"]["country"])
            else:
                # initialize return dict
                returnValue = []

                # get all countrys from DB
                keys = DB.keys("GeoJson:*")
                countryset = set()
                for i in range(len(keys)):
                    countryset.add(str(keys[i]).split(":")[1])

                # get GeoJson for every country
                for country in countryset:
                    returnValue.append(self._getGeoJsonSingel(countryname=country))
                return returnValue

    def _getAstros(self, requestData):
        astros = astrosOnISS.getAstrosOnISS()
        astrosWithItems = []
        with self.__redisDB__ as DB:
            for i in range(len(astros)):

                # get picture,flag and nation of current astro
                picture = DB.get("Astronaut:" + astros[i] + ":" + 'picture')
                flag = DB.get("Astronaut:" + astros[i] + ":" + 'flag')
                nation = DB.get("Astronaut:" + astros[i] + ":" + 'nation')
                # assign these items to current astronaut
                astrosWithItems.append(Astronaut(name=astros[i], pic=picture, flag=flag, nation=nation))
            return astrosWithItems


    def setData(self, data, requestname):
        # switch case for requestnames -> call correct function for every request
        topLevel = {
            "ISSpos": self._setIsspos,
            "RSS-Feed": "_setRSS"
        }
        topLevel.get(requestname)(data)

    def getData(self, requestData, requestName):
        # switch case for requestnames -> call correct function for every request
        functions = {
            "ISSDB": self._getISS,
            "GeoJson": self._getGeoJson,
            "AstrosOnISS": self._getAstros
        }
        return functions.get(requestName)(requestData)






# Comment out for Debugging purposes
# if __name__ == '__main__':
#     data = {
#         'latitude': -45.4742,
#         'longitude': 150.3883,
#         'timestamp': '2020-06-09 20-50-01'
#     }
#     DB = redisDB()
#     DB.setData(data=data, requestname="ISSpos")
#
#     datar = {
#         "params": {
#             "startTime": "2020-06-09 20-50-01",
#             "endTime": "2020-06-09 21-50-10",
#         }
#     }
#     print(DB.getData(requestData=datar, requestName="ISSDB"))

# if __name__ == '__main__':
#     DB = redisDB()
#     data = {
#         "params": {
#             "country": "all"
#         }
#     }
#     print(DB.getData(data, "GeoJson"))

# if __name__ == '__main__':
#     DB = redisDB()
#     data = {}
#     print(DB.getData(requestData=data, requestName="AstrosOnISS"))