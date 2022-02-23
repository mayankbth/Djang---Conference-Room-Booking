from django.shortcuts import render
from .models import MeetingRoom, Booking
import datetime
import re


# to the room or check the vacancy
def room(request):
    
    context = {'context': 'Meeting Rooms'}
    
    if request.method == 'GET':
        return render(request, 'room.html', context=context)
    else:
        data1 = request.POST['command']
        data2 = list(data1.split(' '))
        
        # If the first string of command is "BOOK"
        if data2[0] == 'BOOK':
            # this should not overlap with any bookings
            buffer_time = ['09:00', '13:15', '13:30', '18:45', '23:45']
            
            # checking if the starting time in buffer time or not
            if data2[1] in buffer_time:
                context.update({'NO_VACANT_ROOM': 'NO_VACANT_ROOM'})
                return render(request, 'room.html', context=context)
            else:
                # checking if the booking is starting and ending at XX:00, 15, 30, 45 min. or not
                if (re.findall(':00', data2[1]) or re.findall(':15', data2[1]) or re.findall(':30', data2[1])\
                    or re.findall(':45', data2[1])) and (re.findall(':00', data2[2]) or re.findall(':15', data2[2])\
                    or re.findall(':30', data2[2]) or re.findall(':45', data2[2])):
                    
                    # converting starting and ending time of booking slot into time object
                    start = datetime.datetime.strptime(data2[1], '%H:%M')
                    start_time = start.time()
                    end = datetime.datetime.strptime(data2[2], '%H:%M')
                    end_time = end.time()
                    
                    # converting the buffer time list in time objects for comparision 
                    buffer_time_1 = datetime.time(9,00,00)
                    buffer_time_2 = datetime.time(13,15,00)
                    buffer_time_3 = datetime.time(13,30,00)
                    buffer_time_4 = datetime.time(18,45,00)
                    buffer_time_5 = datetime.time(23,45,00)

                    # Checking if the booking slot is overlapping the buffer_time or not
                    if (start_time < buffer_time_1 and end_time <= buffer_time_1) or\
                        (start_time < buffer_time_2 and end_time <= buffer_time_2) or\
                        (start_time < buffer_time_3 and end_time <= buffer_time_3) or\
                        (start_time < buffer_time_4 and end_time <= buffer_time_4) or\
                        (start_time < buffer_time_5 and end_time <= buffer_time_5):
                        
                        # checking if the start_time (data2[1]) is less than end_time (data2[2]) or not    
                        if end_time > start_time:
                                                
                            # checking if the no. of person is in between 2 and 20
                            if int(data2[3]) >= 2 and int(data2[3]) <= 20:
                                
                                # checking if the number of person is suitable for c-connect or not
                                if int(data2[3]) >= 2 and int(data2[3]) <= 3:
                                    
                                    # creating a flog to represent if the slot is available or not, 0 = available, if not will change to 1
                                    slot_flag = 0
                                    
                                    # getting all the slots info
                                    try:
                                        occupied_slots = Booking.objects.filter(meeting_room=1)
                                        print(occupied_slots)
                                    except:
                                        pass
                                    
                                    # converting querryset into list of dictonary to run a for loop 
                                    # to check wether the slot ia available or not
                                    slot_list = list(occupied_slots.values())
                                    for slot in slot_list:
                                        slot_start_time = slot.get('start_time')
                                        slot_end_time = slot.get('end_time')
                                        
                                        # comparing if the slot is booked or not
                                        if (start_time >= slot_start_time and start_time < slot_end_time)or\
                                            (end_time > slot_start_time and end_time <= slot_end_time):
                                            slot_flag = 1
                                            pass
                                            
                                    # if slot flag is == 0, booking the slot
                                    if slot_flag == 0:
                                        # booking_start_time
                                        booking = Booking()
                                        # creating a foreign key instance to save it in foregn key field
                                        fk_instance = MeetingRoom.objects.get(id=1)
                                        booking.meeting_room = fk_instance
                                        booking.start_time = datetime.datetime.strptime(data2[1], '%H:%M').time()
                                        booking.end_time = datetime.datetime.strptime(data2[2], '%H:%M').time()
                                        booking.save()
                                        context.update({'room': 'C-Contact'})
                                        return render(request, 'room.html', context=context)

                                # checking if the number of person is suitable for s-sharing or Not
                                if int(data2[3]) >= 2 and int(data2[3]) <= 7:
                                    
                                    # creating a flog to represent if the slot is available or not, 0 = available, if not will change to 1
                                    slot_flag = 0
                                    
                                    # getting all the slots info
                                    try:
                                        occupied_slots = Booking.objects.filter(meeting_room=2)
                                    except:
                                        pass
                                    
                                    # converting querryset into list of dictonary to run a for loop 
                                    # to check wether the slot ia available or not
                                    slot_list = list(occupied_slots.values())
                                    for slot in slot_list:
                                        slot_start_time = slot.get('start_time')
                                        slot_end_time = slot.get('end_time')
                                        
                                        # comparing if the slot is booked or not
                                        if (start_time >= slot_start_time and start_time < slot_end_time)or\
                                            (end_time > slot_start_time and end_time <= slot_end_time):
                                            # print(start_time, slot_start_time)
                                            # print(end_time, slot_end_time)
                                            slot_flag = 1
                                            pass
                                        
                                    # if slot flag is == 0, booking the slot
                                    if slot_flag == 0:
                                        # booking_start_time
                                        booking = Booking()
                                        # creating a foreign key instance to save it in foregn key field
                                        fk_instance = MeetingRoom.objects.get(id=2)
                                        print(fk_instance)
                                        booking.meeting_room = fk_instance
                                        booking.start_time = datetime.datetime.strptime(data2[1], '%H:%M').time()
                                        booking.end_time = datetime.datetime.strptime(data2[2], '%H:%M').time()
                                        booking.save()
                                        context.update({'room': 'S-Sharing'})
                                        return render(request, 'room.html', context=context)

                                # checking if the number of person is suitable for t-team or Not
                                if int(data2[3]) >= 2 and int(data2[3]) <= 20:
                                    
                                    # creating a flog to represent if the slot is available or not, 0 = available, if not will change to 1
                                    slot_flag = 0
                                    
                                    # getting all the slots info
                                    try:
                                        occupied_slots = Booking.objects.filter(meeting_room=3)
                                    except:
                                        pass
                                    
                                    # converting querryset into list of dictonary to run a for loop 
                                    # to check wether the slot ia available or not
                                    slot_list = list(occupied_slots.values())
                                    for slot in slot_list:
                                        slot_start_time = slot.get('start_time')
                                        slot_end_time = slot.get('end_time')
                                        
                                        # comparing if the slot is booked or not
                                        if (start_time >= slot_start_time and start_time < slot_end_time)or\
                                            (end_time > slot_start_time and end_time <= slot_end_time):
                                            slot_flag = 1
                                            pass
                                    
                                    print()        
                                    # if slot flag is == 0, booking the slot
                                    if slot_flag == 0:
                                        # booking_start_time
                                        booking = Booking()
                                        # creating a foreign key instance to save it in foregn key field
                                        fk_instance = MeetingRoom.objects.get(id=3)
                                        booking.meeting_room = fk_instance
                                        booking.start_time = datetime.datetime.strptime(data2[1], '%H:%M').time()
                                        booking.end_time = datetime.datetime.strptime(data2[2], '%H:%M').time()
                                        booking.save()
                                        context.update({'room': 'T-Team'})
                                        return render(request, 'room.html', context=context)  
                                                                        
                                    # if no. of persion not suitable for any type of room
                                    else:
                                        context.update({"NO_VACANT_ROOM": "NO_VACANT_ROOM"})
                                        return render(request, 'room.html', context=context)
                                
                            # when the no. of person is not between 2 and 20    
                            else:
                                context.update({"NO_VACANT_ROOM": "NO_VACANT_ROOM"})
                                return render(request, 'room.html', context=context)
                        
                        # if the end_time (data2[2]) is less than start_time (data2[1])        
                        else:
                            context.update({"INCORRECT_INPUT": "INCORRECT_INPUT"})
                            return render(request, 'room.html', context=context)

                    # when the booking slot is overlapping the buffer_time
                    else:
                        context.update({"NO_VACANT_ROOM": "NO_VACANT_ROOM"})
                        return render(request, 'room.html', context=context)
                        
                # if booking is not starting and ending at XX:00, 15, 30, 45 min.
                else:
                    context.update({"INCORRECT_INPUT": "INCORRECT_INPUT"})
                    return render(request, 'room.html', context=context)
        
        # when the first string of command is "VACANCY"
        if data2[0] == 'VACANCY':
            
            start = datetime.datetime.strptime(data2[1], '%H:%M')
            start_time = start.time()
            end = datetime.datetime.strptime(data2[2], '%H:%M')
            end_time = end.time()
            
            # occupied_slots = Booking.objects.filter(start_time=start_time, end_time=end_time)
            occupied_slots = Booking.objects.all()
            occupied_slots_list = list(occupied_slots.values())
            
            room_list = []
            for slot in occupied_slots_list:
                slot_start_time = slot.get('start_time')
                slot_end_time = slot.get('end_time')
                if (start_time >= slot_start_time and start_time < slot_end_time)or\
                    (end_time > slot_start_time and end_time <= slot_end_time):
                        
                    slot_room = slot.get('meeting_room_id')
                    qs = MeetingRoom.objects.filter(id=slot_room)
                    qs_list = list(qs.values())
                    for q in qs_list:
                        occupied_room = q.get('name')
                        room_list.append(occupied_room)
            
            if len(room_list)==0:
                available_room_list = ['C-Contact', 'S-Sharing', 'T-Team']
                context.update({'available_room_list': available_room_list})
                return render(request, 'room.html', context=context)
                
            elif len(room_list)==1:
                all_room = ['C-Contact', 'S-Sharing', 'T-Team']
                available_room_list = set(all_room).difference(room_list)
                context.update({'available_room_list': available_room_list})
                return render(request, 'room.html', context=context)
                
            elif len(room_list)==2:
                all_room = ['C-Contact', 'S-Sharing', 'T-Team']
                available_room_list = set(all_room).difference(room_list)
                context.update({'available_room_list': available_room_list})
                return render(request, 'room.html', context=context)
                
            else:
                context.update({'NO_VACANT_ROOM': 'NO_VACANT_ROOM'})
                return render(request, 'room.html', context=context)
            
            return render(request, 'room.html', context=context)


def room_details(request):
    rooms = MeetingRoom.objects.all()
    context = {'context': 'Meeting Rooms Details', 'rooms': rooms}
    return render(request, 'room_details.html', context=context)


def instructions(request):
    context = {'context': 'Instructions To Book The Meeting Rooms'}
    return render(request, 'instructions.html', context=context)

