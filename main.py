import os
import argparse
import pandas as pd

# Argumentek beolvasása
parser = argparse.ArgumentParser(description="Paraméterek bekérése", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-t", "--target", help="Target directory when saved all file", default= "dist/")
parser.add_argument("-d", "--dirs", help="Create directory every files", default="true", choices=["true", "false"])
parser.add_argument("-a", "--addheaderkey", help="Add header key in content with join separator", default="true", choices=["true", "false"])
parser.add_argument("-j", "--join", help="The target file content line and header separator", default= "=")

parser.add_argument("source", help="Source location")
args = parser.parse_args()
arguments = vars(args)

source=arguments["source"]
targetDir=arguments["target"] if arguments["target"].endswith("/") else f'{arguments["target"]}/'
createDirs = True if arguments['dirs'] == "true" or arguments['dirs'] == "True" else False
addkey = True if arguments['addheaderkey'] == "true" or arguments['addheaderkey'] == "True"  else False
join =arguments['join']

if not os.path.isfile(source):
    exit("The source is not exist: "+source)

if not os.path.isdir(targetDir):
    os.mkdir(targetDir)

sheet_names = (pd.ExcelFile(source)).sheet_names
print("Table read is complete.")
fileCount=0

def writeFiles(dataRows, target):
    global fileCount
    for data in dataRows:
        if "name" not in data:
            print("Missing name attribute!")
            continue

        fileTarget = target
        if createDirs == True:
            fileTarget = f'{target}{data["name"]}/'

        if not os.path.isdir(fileTarget):
            os.mkdir(fileTarget)

        fileName=f'{fileTarget}{data["name"]}.{data["extension"]}'

        del data["name"]
        del data["extension"]

        content=[]
        for key, value in data.items():
            content.append(f'{key}{join}{value}' if addkey else str(value))

        f = open(fileName, "w", encoding='utf-8')
        f.write("\n".join(content))
        f.close()
        fileCount=fileCount+1


for sheet in sheet_names:
    sheetDir=f'{targetDir}{sheet}/'
    if not os.path.isdir(sheetDir):
        os.mkdir(sheetDir)

    data = pd.read_excel(source, sheet)
    json_data = data.to_dict(orient="records")
    writeFiles(json_data, sheetDir)

print(f'Finish. Created {len(sheet_names)} main liblaries ({", ".join(sheet_names)}) and {fileCount} files.')