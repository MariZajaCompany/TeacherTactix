
class ScheduleCell:
    def __init__(self, teacher=None, room=None):
        self.teacher = teacher
        self.room = room

class Schedule:
    def __init__(self):
        self.scheduleTable = [[ScheduleCell() for _ in range(5)] for _ in range(5)]

    def print_schedule(self):
        for row in self.scheduleTable:
            for cell in row:
                if cell.teacher is not None:
                    print(f"teacher: {cell.teacher}, room: {cell.room}")
                else:
                    print("Empty cell")
            print()