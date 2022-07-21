import sqlite3

connection = sqlite3.connect("LastFMArtistClouds.db")
database = connection.cursor()
def createCloudList(cloudList):
    database.execute("SELECT first_artist, second_artist from related_artist")
    rows = database.fetchall()
    for relationRow in rows:
        foundCloud = False
        for cloudSet in cloudList:
            if relationRow[0] in cloudSet:
                foundCloud = True
                cloudSet.add(relationRow[1])
        if foundCloud == False:
            cloudList.append(set([relationRow[0], relationRow[1]]))
            cloudList.append(set([relationRow[1], relationRow[0]]))
        # cloudList = removeSubClouds(cloudList)
    return cloudList
def removeSubClouds(cloudList):
    for firstIndex, cloudSet in enumerate(cloudList):
        for secondIndex, canidetCloud in enumerate(cloudList):
            if firstIndex != secondIndex:
                if canidetCloud.issubset(cloudSet):
                    # print('============')
                    # print(canidetCloud)
                    # print('+++++++++++++')
                    # print(cloudSet)
                    cloudList.remove(canidetCloud)
    return cloudList
                


cloudList = []
cloudList = createCloudList(cloudList)
cloudList = removeSubClouds(cloudList)
cloudList = removeSubClouds(cloudList)
for cloudSet in cloudList:
    print(cloudSet)