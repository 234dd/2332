from config import Config


class Users:

    def __init__(self):
        self.config = Config(file='users.json', mode="json")

    def kick(self, user_id):
        self.config.remove(str(user_id))
        self.config.save()

    def add(self, user_id, name, group_grief, group_surv):
        self.config.set(str(user_id), {
            "warns": 0,
            "name": name,
            "all_reports": 0,
            "days_reports": 0,
            "week_reports": 0,
            "id": user_id,
            "role": "Intern",
            "role_id": 1,
            "medals": 0,
            "balance": 0,
            "group": {
                "surv": group_surv,
                "grief": group_grief
            }
        })
        self.config.save()

    def warn(self, user_id):
        all = self.config.getAll()
        all[str(user_id)]['warns'] += 1
        self.config.setAll(all)
        self.config.save()

    def unwarn(self, user_id):
        all = self.config.getAll()
        all[str(user_id)]['warns'] -= 1
        self.config.setAll(all)
        self.config.save()

    def in_config(self, user_id):
        if self.config.isset(str(user_id)):
            return True
        else:
            return False

    def getWarns(self, user_id):
        return self.config.get(str(user_id))['warns']

    def getAll(self):
        return self.config.getAll()

    def getUser(self, user_id):
        return self.config.get(str(user_id))

    def addReport(self, user_id):
        all = self.config.getAll()
        all[str(user_id)]['all_reports'] += 1
        all[str(user_id)]['days_reports'] += 1
        all[str(user_id)]['week_reports'] += 1
        self.config.setAll(all)
        self.config.save()

    def getAllReports(self, user_id):
        return self.config.get(str(user_id))['all_reports']

    def getDayReports(self, user_id):
        return self.config.get(str(user_id))['days_reports']

    def getWeekReports(self, user_id):
        return self.config.get(str(user_id))['week_reports']

    def getName(self, user_id):
        return self.config.get(str(user_id))['name']

    def clearDayReports(self, user_id):
        all = self.config.getAll()
        all[str(user_id)]['days_reports'] = 0
        self.config.setAll(all)
        self.config.save()

    def clearWeekReports(self, user_id):
        all = self.config.getAll()
        all[str(user_id)]['week_reports'] = 0
        self.config.setAll(all)
        self.config.save()

    def getRole(self, user_id):
        return self.config.get(str(user_id))['role']

    def getRoleById(self, user_id):
        return self.config.get(str(user_id))['role_id']

    def setRole(self, user_id, role_id):
        roles = {
            1: "Intern",
            2: "Helper",
            3: "St.Helper",
            4: "Moderator",
            5: "Administrator"
        }
        all = self.config.getAll()
        all[str(user_id)]['role_id'] = role_id
        all[str(user_id)]['role'] = roles.get(role_id)
        self.config.setAll(all)
        self.config.save()

    def getMedals(self, user_id):
        return self.config.get(str(user_id))['medals']

    def addMedals(self, user_id):
        all = self.config.getAll()
        all[str(user_id)]['medals'] += 1
        self.config.setAll(all)
        self.config.save()

    def addBalance(self, user_id, count):
        all = self.config.getAll()
        all[str(user_id)]['balance'] += count
        self.config.setAll(all)
        self.config.save()

    def getBalance(self, user_id):
        return self.config.get(str(user_id))['balance']

    def setBalance(self, user_id):
        all = self.config.getAll()
        all[str(user_id)]['balance'] = 0
        self.config.setAll(all)
        self.config.save()

    def minusBalance(self, user_id, count):
        all = self.config.getAll()
        all[str(user_id)]['balance'] -= count
        self.config.setAll(all)
        self.config.save()

    def getGroupGrief(self, user_id):
        return self.config.get(str(user_id))['group']['grief']

    def getGroupSurv(self, user_id):
        return self.config.get(str(user_id))['group']['surv']
