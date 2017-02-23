import csv

class seatingCSV(object):
    def __init__(self, fileName):
        self.fileName = fileName
        self.rows = None

    def getFileName(self):
        return self.fileName

    def getRows(self):
        if self.rows != None:
            return self.rows
        rows = []
        with open(self.fileName, 'r') as seating:
            reader = csv.DictReader(seating)
            for row in reader:
                rows.append(row)
        seating.close()
        self.rows = rows
        return self.rows

class student(object):
    def __init__(self, name, id_num):
        self.name = name
        self.id = id_num
        self.courses = None
        self.examSched = None

    def getName(self):
        return self.name

    def getID(self):
        return self.id

    def getCourses(self, rows):
        if self.courses != None:
            return self.courses

        self.courses = []

        while True:
            nameORcode = raw_input("\nPlease enter the course code or course name (or type 'DONE'): ")
            if nameORcode == 'DONE':
                break
            found = 0
            lastone = -1
            for row in rows:
                if row['COMP_CODE'] == lastone:
                    continue
                if row['DEPT_CODE'] + ' ' + row['COURSE_CODE'] == nameORcode or nameORcode in row['COURSE_NAME']:
                    flag2 = raw_input('Are you enrolled in ' + row['DEPT_CODE'] + ' ' + row['COURSE_CODE'] + ': ' + row['COURSE_NAME'] + '? (Y/N): ')
                    if flag2 == 'Y':
                        found = 1
                        self.courses.append(row['COMP_CODE'])
                        break
                lastone = row['COMP_CODE']

            if found == 0:
                print 'Could not find this course.'

        return self.courses

    def getSched(self, rows):
        if self.examSched != None:
            return self.examSched
        
        courses = self.getCourses(rows)
        sched = []
        for row in rows:
            if row['COMP_CODE'] in courses:
                if self.getID() >= row['ID_FROM'] and self.getID() <= row['ID_TO']:
                    sched.append(row)

        self.examSched = sched
        return sched

    def printSched(self, rows):
        examDays = range(3,17)
        time = [('FN','8AM to 11AM'), ('AN','3PM to 6PM')]
        exams = self.getSched(rows)
        print '\n\n\n' + self.getName() + ', ' + self.getID() + ':\n'
        for day in examDays:
            print 'MAY ' + str(day) + ':'
            for slot in time:
                print '    ' + slot[1] + ':',
                flag = 0
                for exam in exams:
                    if exam['MAY_DATE'] == str(day) and exam['SLOT'] == slot[0]:
                        flag = 1
                        print exam['COURSE_NAME'] + ' in Room #' + exam['ROOM_NO'] +'.'
                if flag == 0:
                    print 'No exam!!'

        print '\nHAPPY HOLIDAYS!!'

def main():
    name = raw_input('Enter your Name: ')
    ID = raw_input('Enter ID No.: ')
    print
    seating = seatingCSV('seatingCSV.csv')
    user = student(name, ID)
    user.printSched(seating.getRows())


main()
