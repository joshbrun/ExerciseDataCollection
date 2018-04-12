from os import listdir, getcwd, rename, makedirs, remove
from os.path import isfile, join, exists

def sortJsonFiles():
    #Take a file in the form:
    # true_squat_male_left_up_t2b8fDsAlFs_00035_keypoints
    # into
    # /true/squat/male/left/up/t2b8fDsAlFs_00035_keypoints
    jsonFiles = []
    dir =  getcwd()+"\\data\\json\\"

    files = [f for f in listdir(dir) if isfile(join(dir, f))]
    fileCount = len(files)
    excludedCount = 0
    includedCount = len(files)
    print("\nSorting %d files"%(fileCount))
    for file in files:
        fileArray = file.split("_")
        newDir = fileArray[0]+"/"+fileArray[1]+"/"+fileArray[2]+"/"+fileArray[3]+"/"+fileArray[4]+"/"
        newFile = fileArray[5]+"_"+fileArray[6]+"_"+fileArray[7]
        checkDirectory(dir+newDir)
        try:
            rename(dir+file, dir+newDir+newFile)
            if not (newDir in jsonFiles):
                jsonFiles.append("/"+fileArray[1]+"/"+fileArray[2]+"/"+fileArray[3]+"/"+fileArray[4]+"/")
        except FileExistsError as e:
            excludedCount = excludedCount + 1
            includedCount = includedCount - 1
            remove(dir+file)


    f = open("data/exerciseList",'a+')
    for file in jsonFiles :
        print(file)
        f.write(file+"\n")

    print("Json created for %d/%d files, %d already existed "%(includedCount, fileCount, excludedCount))
    f.close()

def checkDirectory(path):
    if not exists(path):
        makedirs(path)