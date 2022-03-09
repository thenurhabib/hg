#!/usr/bin python3
# thenurhabib

# Import Modules
try:
    import os
    import sys
    import requests
    import validators
    from time import sleep
except ModuleNotFoundError:
    print("\n\nSome Modules are not installed.")
    print("\nInstalling Modules...\n")
    os.system("pip install -r requirements.txt")
    os.system("clear")
    


class colors:
    bold = '\033[1m'
    yellow ='\033[93m'
    cyan='\033[36m'
    blue='\033[34m'
    red='\033[31m'


def MainFunction():
    # Print Banner and author information
    print(f"""{colors.bold}{colors.cyan}

     _                    _             _       _           _             
    | |                  | |           (_)     (_)         | |            
    | |__   ___  __ _  __| | ___ _ __   _ _ __  _  ___  ___| |_ ___  _ __ 
    | '_ \ / _ \/ _` |/ _` |/ _ \ '__| | | '_ \| |/ _ \/ __| __/ _ \| '__|
    | | | |  __/ (_| | (_| |  __/ |    | | | | | |  __/ (__| || (_) | |   
    |_| |_|\___|\__,_|\__,_|\___|_|    |_|_| |_| |\___|\___|\__\___/|_|v1.0   
                                              _/ |                 
    Host Header injection  scanner.          |__/ 
    """
    )

    print(f"""{colors.yellow}
        -----------------------------------------------------------
                            Author  : Md. Nur habib
                            GitHub  : /thenurhabib
                            Twitter : /thenurhab1b
        -----------------------------------------------------------
        
        {colors.blue}""")

    usage = "Header Injector Usage : \n\nmain.py <options> <arguements>\n \nOptions : \n -u \t:\t URL of the Website \n -i \t:\t Input file of the URLS\n"
    keyword = "evil.com"
    resultList = list()
    ActionFileList = list()
    headerOne = {"Host": keyword}
    headerTwo = {"X-Forwarded-Host": keyword}
    headerThree = {"Origin": keyword}


    def isRedirect(status_code):
        if status_code == 301:
            return True
        elif status_code == 302:
            return True
        elif status_code == 303:
            return True
        elif status_code == 307:
            return True
        elif status_code == 308:
            return True
        else:
            return False


    def processRequestFile(fileURL):
        print(1)
        return


    def processFile(fileURL):
        f = open(fileURL, "r")
        for line in f:
            line = line.strip()
            customeRequest(line)
            actionCheck(line)
            print("\r" + "Scanning : " + line)
        f.close()
        if len(resultList) == 0:
            print("\nNo Vulnerable URL(s)")
        else:
            print("\nPotential Host Header Injection at :\n")
            for url in resultList:
                print(url)

        if len(ActionFileList) == 0:
            print("\nNo CORS Misconfig(s)")
        else:
            print("\nPossible CORS Misconfig at : ")
            print("\n")
            for url in ActionFileList:
                print(url)
        return


    def customeRequest(targetURL):
        targetURL = f"{targetURL}/"
        if validators.url(targetURL):
            try:
                responseOne = requests.get(
                    targetURL, headers=headerOne, allowRedirects=False
                )
                responseTwo = requests.get(
                    targetURL, headers=headerTwo, allowRedirects=False
                )
                responseOneLocation = ""
                responseTwoLocation = ""

                if isRedirect(responseOne.status_code):
                    if len(responseOne.headers["Location"]) != 0:
                        responseOneLocation = responseOne.headers["Location"]

                responseOneBody = responseOne.content

                if isRedirect(responseTwo.status_code):
                    if len(responseTwo.headers["Location"]) != 0:
                        responseTwoLocation = responseTwo.headers["Location"]

                responseTwoBody = responseTwo.content

                if (
                    responseOneBody.find(keyword) > -1
                    or responseOneLocation.find(keyword) > -1
                    or responseOne.status_code == 200
                    or responseTwoBody.find(keyword) > -1
                    or responseTwoLocation.find(keyword) > -1
                ):
                    resultList.append(targetURL)
            except:
                print(f"\n{colors.red}\t\tCan't connect with {targetURL} {colors.blue}")
        else:
            print(f"\rMalformed URL : {targetURL} \r")
            exit(1)
        return


    def actionCheck(targetURL):
        targetURL = f"{targetURL}/"
        try:
            responseThree = requests.get(targetURL, headers=headerThree, allowRedirects=False)
            responseThreeAction = ""

            if len(responseThree.headers["access-control-allow-origin"]) != 0:
                responseThreeAction = responseThree.headers["access-control-allow-origin"]
            if len(responseThree.headers["Access-Control-Allow-Origin"]) != 0:
                responseThreeAction = responseThree.headers["Access-Control-Allow-Origin"]

            if responseThreeAction.find(keyword) > -1:
                ActionFileList.append(targetURL)

        except:
            print(f"\n{colors.red}\t\tCan't connect with {targetURL}{colors.blue}")


    if len(sys.argv) > 1:
        if sys.argv[1] == "-u":
            targetURL = sys.argv[2]
            print(f"\n\t\tTarget : {targetURL}\n")
            customeRequest(targetURL)
            actionCheck(targetURL)
            if len(resultList) == 0:
                print("\n\t\tNo Reflection of Custom Host at all !")
            else:
                print("\nPotential Host Header Injection at :")
                for url in resultList:
                    print(url)

            if len(ActionFileList) == 0:
                print("\n\t\tNo CORS Misconfig I guess.")
            else:
                print("\nOverly Permissive CORS Policy :")
                for url in ActionFileList:
                    print(url)

        elif sys.argv[1] == "-i":
            print("\nReading from " + sys.argv[2])
            fileURL = sys.argv[2]
            if os.path.isfile(fileURL):
                processFile(fileURL)
            else:
                print("\nNot a Valid File")
        elif sys.argv[1] == "-r":
            print("\nParsing request from text file\n")
        else:
            print(sys.argv)
            print(usage)
    else:
        print(usage)


if __name__ == '__main__':
    MainFunction()