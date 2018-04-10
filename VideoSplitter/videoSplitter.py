import os
#Split each video into the required frames

def splitVideos(videos):
    print("\n")
    #For each video in videos
    for video in videos:
        for part in video['parts']:
            startTime = getSeconds(part['startTime'])
            endTime = getSeconds(part['endTime'])
            duration = endTime - startTime

            input = "data/videos/"+video['identifier']+".mkv"
            # outputDir = "data/frames/"+part['label']+"/"+video['exercise']+"/"+video['sex']+"/"+part['view']+"/"+part['name']
            outputDir = "data/frames/"
            fileName = part['label'] + "_" + video['exercise'] + "_" + video['sex'] + "_" + part['view'] + "_" + part['name'] + "_" + video['identifier'] + "_" + "%05d.jpg"
            output = outputDir + fileName

            checkDirectory("data/frames")
            checkDirectory("data/framesOP")
            checkDirectory("data/json")
            print("Extracting Frames for: %s/%s"%(video["identifier"],part['name']))
            os.system("ffmpeg.exe -loglevel panic -ss "+part['startTime']+" -t 00:00:"+str(duration)+" -i "+input+ " "+output +" -hide_banner")

def checkDirectory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def getSeconds(time):
    h,m,s = time.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)