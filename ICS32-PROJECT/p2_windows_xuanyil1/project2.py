# Xuanyi Lin and Adan Garcia ics32a Project2
# xuanyil1 and adang6

from pathlib import Path

#The program will automatically search all the files through user's disk
#and skip some permission errors and OS errors. It may take several
#minutes to search though the whole disk. It will ask for the name of the file
#that user wants to search.


def allFileInList(path):
    '''This function puts all files that the program has access to in a list'''

    global fileList

    #For loop to run through the directories and subdirectories.
    for i in list(path.iterdir()):
        try:
            if i.is_dir():
                fileList.append(i.absolute())
                fileList += list(i.iterdir())
                allFileInList(i)
        except PermissionError as e:
            pass
        except OSError as e:
            pass
    return
    

def findPath():
    '''This function asks a name or a sector of a name that user wants to search.
    It then shows all the files that related to this name or sector.
    '''

    global absoluteFileList
    global fileList

    #The user will decided on a string to search for. 
    name = input('Interested name: ')
    found = 0
    if name == 'done-for-now':
        return

    #Run through the filelist from all_file_in_list to compare it with the user string.
    for i in fileList:
        if name in str(i) and str(i.absolute()) not in absoluteFileList:
            absoluteFileList.append(str(i.absolute()))
            print(i.absolute())
            print()
            found += 1
    if found == 0:
        print('NOT FOUND')
        findPath()
    return


def TextInTxt():
    '''This function asks the part that user want to see from the files listed above.
    if it is a filename open and read first three lines.
    '''
    
    global absoluteFileList

    #User inputs which path they're interested in exploring. 
    search = input('Interested part: ')
    listPrint = []
    formatTF = False

    #If user is interested in all files. 
    if search == 'all' or search == 'ALL':
        formatTF = True
        for i in absoluteFileList:
            listPrint.append(i)
    #Match the users input string for filename. 
    elif search in absoluteFileList:
        formatTF = True
        listPrint.append(search)
    elif search.split(',')[0] in absoluteFileList:
        formatTF = True
        listPrint = search.split(',')
    #Matcht directory to directory. 
    elif search.endswith('>') and search.startswith('<'):
        formatTF = True
        search = search.replace(' ', '')
        search = search.replace('>', '')
        search = search.replace('<', '')
        searchList = search.split('-')
        index1 = absoluteFileList.index(searchList[0])
        index2 = absoluteFileList.index(searchList[1])
        for i in range(index1, index2 + 1):
            listPrint.append(absoluteFileList[i])

    #Open the file.txt and read first three lines. 
    for i in listPrint:
        print(i)
        print()
        if str(i).endswith('.txt'):
            f = open(i)
            lf = f.readlines()
            if len(lf) >= 3:
                for j in range(3):
                    print(lf[j])
            else:
                for m in lf:
                    print(m)
            print()
        else:
            print('NOT TEXT')
            print()

    #If not a file above print ERROR and ask again. 
    if formatTF == False:
        print('ERROR')
        print()
        TextInTxt()
    return
                    

if __name__ == '__main__':
    '''Run the program'''
    
    p = Path(str(Path('.').absolute())[0:3])

    lpath = list(p.iterdir())
    fileList = []
    for x in lpath:
        try:
            if not x.is_dir():
                fileList.append(x)
        except PermissionError as e:
            pass

    absoluteFileList = []
    allFileInList(p)
    findPath()
    TextInTxt()
