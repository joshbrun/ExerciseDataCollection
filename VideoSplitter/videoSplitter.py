import os

#Split each video into the required frames

def splitVideos(videos):

    #For each video in videos
    for video in videos:
        for part in video['parts']:
            print(part)

            (videoName, outputPathName) = getPathName(video,part['name'])
            extractFrames(videoName, outputPathName, part['startTime'], part['endTime'])

def extractFrames(video, output, start, end):

    pass

def getPathName(video, part):
    print(video)
    print(part)
    exercise = video['exercise']
    sex = video['sex']
    view = video['view']
    label = video['label']
    pathName = "data/"+exercise+"/"+sex+"/"+view+"/"+part+"/"+label
    checkDirectory(pathName)

    outputPathName = "%s_%s_%s_%s.mp4" % (exercise, sex, view, label)
    return (video, outputPathName+"/")

def checkDirectory(path):
    if not os.path.exists(path):
        os.makedirs(path)