'''
Check the number of lines of logs in the CAN ascii log file.
filename: A string pointing to the file location of the log file
    Ex.: "CCAN.asc"
return: number of lines (integer)
    Ex.: 2994822
'''
def get_total_lines(filename):
    file = open(filename)
    hcount = 0
    numberLines = 0
    headerFinished = False
    for line in file:
        if hcount >= 3:
            if headerFinished:
                # Continue copying
                numberLines += 1
            else:
                # Copy header
                headerFinished = True
        else:
            hcount += 1
    
    file.close()
    
    return numberLines

'''
To trim the data (also in ASCII format) between a range of time.
Not CAN line specific.
filename: A string pointing to the file location of the log file
    Ex.: "CCAN.asc"
start: Line number to start copying at
end: Line number to end copying at
output: A file in current directory named "OUTPUT.asc"
    Format is same as input ASCII file (header info is preserved)
'''
def trim(filename, start, end):
    file = open(filename)
    copyTo = open("OUTPUT.asc", 'w')
    hcount = 0
    numberLines = 0
    headerFinished = False
    for line in file:
        if hcount >= 3:
            if headerFinished:
                # Continue copying
                numberLines += 1
                if numberLines < end and numberLines >= start:
                    copyTo.write(line)
                elif numberLines >= end:
                    break
            else:
                # Copy header
                headerFinished = True
        else:
            hcount += 1
            copyTo.write(line)
    
    file.close()
    copyTo.close()
    print("Copied " + str(end - start) + " lines.")

'''
To trim the data (also in ASCII format) between a range of time and only account for a given set of CAN IDs.
Not CAN line specific.
filename: A string pointing to the file location of the log file
    Ex.: "CCAN.asc"
start: Line number to start copying at
end: Line number to end copying at
canids: A list of CAN IDs to check against
    Ex.: ['450', '54A']
output: A file in current directory named "OUTPUT.asc"
    Format is same as input ASCII file (header info is preserved)
'''
def trim(filename, canids, start=0, end=0):
    if start == 0 and end == 0:
        start = 0
        end = get_total_lines(filename)
    file = open(filename)
    copyTo = open("OUTPUT.asc", 'w')
    hcount = 0
    numberLines = 0
    headerFinished = False
    for line in file:
        if hcount >= 3:
            if headerFinished:
                # Continue copying
                numberLines += 1
                if numberLines < end and numberLines >= start:
                    split = line.split()
                    if len(split) >= 3 and split[2] in canids:
                        copyTo.write(line)
                elif numberLines >= end:
                    break
            else:
                # Copy header
                headerFinished = True
        else:
            hcount += 1
            copyTo.write(line)
    
    file.close()
    copyTo.close()
    print("Copied " + str(end - start) + " lines.")

# TODO: Should dynamically get byte number (from user input)
def uniqueCanByte(filename, canids):
    result = {}
    linNums = {}
    file = open(filename)
    hcount = 0
    numberLines = 0
    headerFinished = False
    for line in file:
        if hcount >= 3:
            if headerFinished:
                # Continue copying
                numberLines += 1
                split = line.split()
                if len(split) >= 3 and split[2] in canids:
                    if len(split) >= 7 and split[6] not in result:
                        result[split[6]] = split[0]
                        linNums[split[6]] = numberLines
            else:
                # Copy header
                headerFinished = True
        else:
            hcount += 1
    
    file.close()
    sorted = []
    for (speed, time), (speed2, line) in zip(result.items(), linNums.items()):
        sorted.append((speed, time, line))
    
    sorted.sort(key=lambda tup: tup[0])
    
    for x in sorted:
        print(x[0], x[1], x[2])

'''
To make a quick query to see if a CAN ID exists on a CAN line.
CAN line 1 is hard coded.
filename: A string pointing to the file location of the log file
    Ex.: "CCAN.asc"
canids: A list of CAN IDs to check against
    Ex.: ['450', '54A']
return: The result as a dictionary
    Ex.: {'450': True, '52A': False}
'''
def findCanId(filename, canids):
    result = {}
    file = open(filename)
    hcount = 0
    headerFinished = False
    for line in file:
        if hcount >= 3:
            if headerFinished:
                # Continue copying
                split = line.split()
                if len(split) >= 3 and split[2] in canids:
                    result[split[2]] = True
            else:
                # Copy header
                headerFinished = True
        else:
            hcount += 1
    file.close()
    for id in canids:
        if id not in result:
            result[id] = False
    return result
    
    
# findCanId("CANOE.asc", ['450', '5D0', '4F1', '52A'])