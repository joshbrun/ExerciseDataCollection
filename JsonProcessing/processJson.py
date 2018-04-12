import os
import json
import sys

PART_MAPPING = {
    0:"Nose",
    1:"Neck",
    2:"RShoulder",
    3:"RElbow",
    4:"RWrist",
    5:"LShoulder",
    6:"LElbow",
    7:"LWrist",
    8:"RHip",
    9:"RKnee",
    10:"RAnkle",
    11:"LHip",
    12:"LKnee",
    13:"LAnkle",
    14:"REye",
    15:"LEye",
    16:"REar",
    17:"LEar"
}
JOINTS_MAPPING = {
    1:[0,1],
    2:[0,14],
    3:[0,15],
    4:[1,2],
    5:[1,5],
    6:[1,8],
    7:[1,11],
    8:[2,3],
    9:[3,4],
    10:[5,6],
    11:[6,7],
    12:[8,9],
    13:[9,10],
    14:[11,12],
    15:[12,13],
    16:[14,16],
    17:[15,17]
}


def calcGradients(filename, label):
    correctness = 0
    if label == "true":
        correctness = 1

    line = ""
    file = open(filename,'r')
    lines = file.readline()
    jsonLines = json.loads(lines)
    people = jsonLines['people']

    #TODO this is assuming there is only one person in the frame
    keypoints = people[0]['pose_keypoints_2d']

    for key in JOINTS_MAPPING:
        partA = JOINTS_MAPPING[key][0]
        partB = JOINTS_MAPPING[key][1]

        indexA = partA*3
        x1 = keypoints[indexA]
        y1 = keypoints[indexA+1]
        c1 = keypoints[indexA+2]

        indexB = partB*3
        x2 = keypoints[indexB]
        y2 = keypoints[indexB + 1]
        c2 = keypoints[indexB + 2]

        if x2 == x1 and x2 == 0:
            #point doesnt exist
            line += ",%0.4d,%0.3d,%0.3d"%(0,0,0)
        elif y2 == y1 and y2 ==0:
            #point doesnt exist
            line += ",%.4f,%.3f,%.3f"%(0,0,0)

        elif x2 == x1 and y2 == y1:
            #points are the same
            line += ",%.4f,%.3f,%.3f"%(0,0,0)

        elif x2 == x1:
            #gradient is infinite
            g = sys.maxsize
            line += ",%.4f,%.3f,%.3f"%(g,0,0)
        elif y2 == y1:
            #gradient is 0
            line += ",%.4f,%.3f,%.3f"%(0,c1,c2)
        else:
            g = (float(y2)-float(y1))/(float(x2)-float(x1))
            line += ",%.4f,%.3f,%.3f"%(g,c1,c2)

    if not line == "":
        line = line[1:]+","+str(correctness)

    file.close()

    return line

def processJson():
    print("\nConverting the seperate Json files into a Trainable Vector Set")
    outputDir = os.getcwd()+"\\training"
    checkDirectory(outputDir)

    #Read the sets
    dir = os.getcwd()+"\\data\\"
    filename = "exerciseList"
    file = open(dir+filename,'r')
    sets = []

    for line in file.readlines():
        sets.append(line[:-2])
    file.close()

    print("Sets to process: %d"%(len(sets)))

    jsonDir = dir+"json\\"

    for set in sets:
        print("\n" + "Processing Set: " + dir)
        setNameList = set.split("/")
        print(setNameList)
        outputFileName = setNameList[1]+"_"+setNameList[2]+"_"+setNameList[3]+"_"+setNameList[4]
        outputFile = open(outputDir + "/" + outputFileName+".csv", "w+")

        for label in ["true","false"]:

            dir = jsonDir+label+"/"+set
            try:
                files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]


                lines = []
                for jsonFile in files:
                    print(jsonFile)
                    lines.append(calcGradients(dir+"/"+jsonFile, label))

                for line in lines:
                    if not (line == "[]"):
                        print(line)
                        outputFile.write(line+"\n")
            except FileNotFoundError as e:
                continue

        outputFile.close()


def checkDirectory(path):
    if not os.path.exists(path):
        os.makedirs(path)
