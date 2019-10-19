class DivisionStateCars:
    def __init__(self):
        self.newer = []
        self.leave = []
        self.deleted = []
        self.len_newer = 0
        self.len_leave = 0
        self.len_deleted = 0
        self.len_exist_total = 0

    def of(self, separated_by_status):
        self.newer = separated_by_status['newer']
        self.leave = separated_by_status['leave']
        self.deleted = separated_by_status['deleted']
        self.len_newer = len(self.newer)
        self.len_leave = len(self.leave)
        self.len_deleted = len(self.deleted)
        self.len_exist_total = self.len_newer + self.len_leave

    def set_leave(self, leave_cars):
        self.leave = leave_cars
        self.len_leave = len(leave_cars)

    def get_newer(self):
        return self.newer

    def get_leave(self):
        return self.leave

    def get_deleted(self):
        return self.deleted

    def get_len_newer(self):
        return self.len_newer

    def get_len_leave(self):
        return self.len_leave

    def get_len_deleted(self):
        return self.len_deleted
    
    def get_len_exist_total(self):
        return self.len_exist_total
