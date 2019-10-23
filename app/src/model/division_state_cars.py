import datetime
import pytz

class DivisionStateCars:
    def __init__(self):
        self.newer = []
        self.leave = []
        self.updated = []
        self.deleted = []
        self.len_newer = 0
        self.len_leave = 0
        self.len_updated = 0
        self.len_deleted = 0
        self.len_exist_total = 0

    def update_total(self):
        self.len_exist_total = self.len_newer + self.len_leave + self.len_updated
        
    def by_separated_status(self, separated_by_status):
        self.newer = separated_by_status.get('newer') if separated_by_status.get('newer') else []
        self.leave = separated_by_status.get('leave') if separated_by_status.get('leave') else []
        self.updated = separated_by_status.get('updated') if separated_by_status.get('updated') else []
        self.deleted = separated_by_status.get('deleted') if separated_by_status.get('deleted') else []
        self.len_newer = len(self.newer) if self.newer else 0
        self.len_leave = len(self.leave) if self.leave else 0
        self.len_updated = len(self.updated) if self.updated else 0
        self.len_deleted = len(self.deleted) if self.deleted else 0
        self.update_total()

    def set_newer(self, newer):
        self.newer = newer
        self.len_newer = len(newer)
        self.update_total()
        
    def set_leave(self, leave_cars):
        self.leave = leave_cars
        self.len_leave = len(leave_cars)
        self.update_total()

    def set_updated(self, updated_cars):
        self.updated = updated_cars
        self.len_updated = len(updated_cars)
        self.update_total()
        
    def get_newer(self):
        return self.newer

    def get_leave(self):
        return self.leave

    def get_updated(self):
        return self.updated
    
    def get_deleted(self):
        return self.deleted

    def get_len_newer(self):
        return self.len_newer

    def get_len_leave(self):
        return self.len_leave

    def get_len_updated(self):
        return self.len_updated

    def get_len_deleted(self):
        return self.len_deleted
    
    def get_len_exist_total(self):
        return self.len_exist_total

    def add_removed_date(self):
        for x in self.deleted:
            x['removed_date'] = datetime.datetime.now(tz=pytz.timezone('Asia/Seoul'))
            
    def add_updated_mark(self):
        if self.updated:
            for x in self.updated:
                x['state'] = "updated"
        