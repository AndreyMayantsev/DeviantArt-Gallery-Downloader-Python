import os
import datetime


class log:

    LOG_FOLDER_NAME = "LOGS"
    LOG_FOLDER_SEPARATE_BY_DATE = True
    LOG_NAME = "log"

    dir = os.path.abspath(os.curdir)
    now = datetime.datetime.today().strftime('%Y-%m-%d')
    logDir = str(dir) + "/" + LOG_FOLDER_NAME + "/"
    fileName = "default.log"

    def __init__(self, name):
        self.LOG_NAME = name

        if self.folderExists(self.logDir):
            if self.LOG_FOLDER_SEPARATE_BY_DATE:
                self.folderExists(self.logDir + "/" + self.now)
                self.logDir = self.logDir + self.now
            else:
                pass

        self.fileName = "/" + self.LOG_NAME + "-" + self.now + ".log"

    def folderExists(self, folder):
        if os.path.exists(folder):
            return True
        else:
            try:
                os.mkdir(folder)
                return True
            except PermissionError:
                print(f"Log folder does not exists and can't be created! -> {folder} : Permission Denied!")
                return False
            except Exception as error:
                print(f"Log folder does not exists and can't be created! -> {folder} : {error}")
                return False

    def writeLog(self, logtext):
        time = datetime.datetime.today().strftime('%X')

        if self.LOG_FOLDER_SEPARATE_BY_DATE:
            self.actualizeLogDir()

        try:
            logFile = open(self.logDir + self.fileName, "a")
            logFile.write(time + " | " + logtext + "\n")
            logFile.close()
        except PermissionError:
            print(f"Error when writing log to a file -> {self.fileName} : Permission Denied!")
        except Exception as error:
            print(f"Error when writing log to a file -> {self.fileName} : {error}!")

    def actualizeLogDir(self):
        self.now = datetime.datetime.today().strftime('%Y-%m-%d')
        self.logDir = self.dir + "/" + self.LOG_FOLDER_NAME + "/" + self.now
        self.folderExists(self.logDir)


