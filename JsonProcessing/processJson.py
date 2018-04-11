import os

def calcGradients(filename):
    line = ""
    file = open(filename,'r')
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
        dir = jsonDir+set
        setNameList = set.split("/")
        outputFileName = setNameList[0]+"_"+setNameList[1]+"_"+setNameList[2]+"_"+setNameList[3]+"_"+setNameList[4]
        files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
        print("\n"+ "Processing Set: "+dir)
        print("%d Files"%(len(files)))

        lines = []
        for jsonFile in files:
            print(jsonFile)
            lines.append(calcGradients(dir+"/"+jsonFile))

        outputFile = open(outputDir+outputFileName,"w+")

        for line in lines:
            if not (line == ""):
                outputFile.write(line+"/n")

        outputFile.close()


def checkDirectory(path):
    if not os.path.exists(path):
        os.makedirs(path)