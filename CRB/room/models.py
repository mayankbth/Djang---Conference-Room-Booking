from django.db import models


class MeetingRoom(models.Model):
    name = models.CharField(max_length=30)
    capacity = models.IntegerField()
    
    def __str__(self):
        return self.name
    

class Booking(models.Model):
    meeting_room = models.ForeignKey(MeetingRoom, on_delete=models.CASCADE, related_name='meeting_room')
    start_time = models.TimeField()
    end_time = models.TimeField()
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.meeting_room.name + " | " + str(self.start_time) + " | " + str(self.end_time)
    
    