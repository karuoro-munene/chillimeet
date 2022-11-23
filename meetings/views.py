import re

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from num2words import num2words

from meetings.models import Staff, Meeting, MeetingItem, MeetingItemStatus


# Create your views here.
def home(request):
    return render(request, 'index.html', locals())


def meetings(request):
    meeting_types = ["MANCO",
                     "Finance",
                     "Project Team Leaders"]
    all_meetings = Meeting.objects.all().order_by("-created_on")
    if request.method == 'POST' and 'type' in request.POST:
        meeting_type = request.POST.get("type")
        meeting_date = request.POST.get("date")
        meeting_time = request.POST.get("time")
        print("meeting type: ", meeting_type)
        if meeting_type == "MANCO":
            prefix = "M"
            try:
                last_manco_meeting = Meeting.objects.filter(meeting_type=meeting_type).latest("created_on")
                print("last meeting", last_manco_meeting)
                new_manco_meeting = Meeting.objects.create(meeting_type=meeting_type,
                                                           meeting_number=f"M{int(last_manco_meeting.meeting_number.replace('M', '')) + 1}",
                                                           meeting_date=meeting_date,
                                                           meeting_time=meeting_time)
                new_manco_meeting.save()
                print("new meeting", new_manco_meeting)
            except ObjectDoesNotExist:
                new_manco_meeting = Meeting.objects.create(meeting_type=meeting_type, meeting_number="M1",
                                                           meeting_date=meeting_date,
                                                           meeting_time=meeting_time)
                new_manco_meeting.save()
                print("new meeting", new_manco_meeting)
            return redirect(create_meeting, meeting_number=new_manco_meeting.meeting_number)
        elif meeting_type == "Finance":
            prefix = "F"
            try:
                last_finance_meeting = Meeting.objects.filter(meeting_type=meeting_type).latest("created_on")
                print("last meeting", last_finance_meeting)
                new_finance_meeting = Meeting.objects.create(meeting_type=meeting_type,
                                                             meeting_number=f"F{int(last_finance_meeting.meeting_number.replace('F', '')) + 1}",
                                                             meeting_date=meeting_date,
                                                             meeting_time=meeting_time
                                                             )
                new_finance_meeting.save()
                print("new meeting", new_finance_meeting)
            except ObjectDoesNotExist:
                new_finance_meeting = Meeting.objects.create(meeting_type=meeting_type, meeting_number="F1",
                                                             meeting_date=meeting_date,
                                                             meeting_time=meeting_time
                                                             )
                new_finance_meeting.save()
                print("new meeting", new_finance_meeting)
            return redirect(create_meeting, meeting_number=new_finance_meeting.meeting_number)
        elif meeting_type == "Project Team Leaders":
            prefix = "PTL"
            try:
                last_ptl_meeting = Meeting.objects.filter(meeting_type=meeting_type).latest("created_on")
                print("last meeting", last_ptl_meeting)
                new_ptl_meeting = Meeting.objects.create(meeting_type=meeting_type,
                                                         meeting_number=f"PTL{int(last_ptl_meeting.meeting_number.replace('PTL', '')) + 1}",
                                                         meeting_date=meeting_date,
                                                         meeting_time=meeting_time
                                                         )
                new_ptl_meeting.save()
                print("new meeting", new_ptl_meeting)

            except ObjectDoesNotExist:
                new_ptl_meeting = Meeting.objects.create(meeting_type=meeting_type, meeting_number="PTL1",
                                                         meeting_date=meeting_date,
                                                         meeting_time=meeting_time
                                                         )
                new_ptl_meeting.save()
                print("new meeting", new_ptl_meeting)
            return redirect(create_meeting, meeting_number=new_ptl_meeting.meeting_number)
        else:
            return HttpResponseRedirect(request.path_info)

    return render(request, 'meetings.html', locals())


def create_meeting(request, meeting_number):
    meeting = Meeting.objects.get(meeting_number=meeting_number)
    # get count of meeting type
    count = re.sub('\D', '', meeting_number)
    print(count)
    prefix = ''.join([i for i in meeting_number if not i.isdigit()])
    print(prefix)
    if int(count) < 2:
        previous_meeting = None
        meeting_items = None
    else:
        previous_meeting = prefix + str(int(count) - 1)
        previous_meeting_obj = Meeting.objects.get(meeting_number=previous_meeting)
        meeting_items = MeetingItem.objects.filter(meeting=previous_meeting_obj)
        if meeting_items.count() == 0:
            blank_items = True
        else:
            blank_items = False

    if request.method == 'POST':
        if 'create_blank' in request.POST:
            meeting.updated_on = timezone.now()
            meeting.save()
        if 'create_previous' in request.POST:
            for key, value in request.POST.items():
                if key.startswith("item_"):
                    this_item = MeetingItem.objects.get(id=value)
                    this_item.meeting = meeting
                    this_item.save()
            meeting.updated_on = timezone.now()
            meeting.save()
        return redirect('meeting', meeting_number=meeting.meeting_number)
    return render(request, 'create_meeting.html', locals())


def meeting(request, meeting_number):
    meeting = Meeting.objects.get(meeting_number=meeting_number)
    meeting_items = MeetingItem.objects.filter(meeting=meeting)
    existing_staff = Staff.objects.all()
    if request.method == 'POST' and 'item' in request.POST:
        meeting_item = request.POST.get("item")
        staff_str = request.POST.get("staff")
        item_due_date = request.POST.get("date")
        person_responsible = Staff.objects.get(id=staff_str)
        print("meeting item: ", meeting_item)
        item = MeetingItem.objects.create(meeting=meeting, name=meeting_item)
        item.person_responsible = person_responsible
        item.due_date = item_due_date
        item.count = meeting_items.count()
        item.label = (num2words((meeting_items.count()))).replace("-", " ").capitalize()
        item.save()
        meeting.updated_on = timezone.now()
        meeting.save()
        return HttpResponseRedirect(request.path_info)
    if request.method == 'POST' and 'edit_item_id' in request.POST:
        item_name = request.POST.get("edit_name")
        staff_name = request.POST.get("edit_staff")
        due_date = request.POST.get("edit_date")
        person_responsible = Staff.objects.get(names=staff_name)
        item_id = request.POST.get("edit_item_id")

        item = MeetingItem.objects.get(id=item_id)
        item.person_responsible = person_responsible
        item.due_date = due_date
        item.name = item_name
        item.updated_on = timezone.now()
        item.save()

        meeting.updated_on = timezone.now()
        meeting.save()
        return HttpResponseRedirect(request.path_info)
    return render(request, 'meeting.html', locals())


def items(request, meeting_number, id):
    meeting = Meeting.objects.get(meeting_number=meeting_number)
    item = MeetingItem.objects.get(id=id)
    statuses = ['Open', 'In Development', 'Awaiting Invoicing', 'Closed']
    existing_staff = Staff.objects.all()
    items_statuses = MeetingItemStatus.objects.filter(meeting_item=id)
    if request.method == 'POST' and 'action' in request.POST and 'staff' in request.POST and 'status' in request.POST:
        action = request.POST.get("action")
        staff_id = request.POST.get("staff")
        staff = Staff.objects.get(id=staff_id)
        status = request.POST.get('status')

        meeting_item_status = MeetingItemStatus.objects.create(meeting_item=item, action=action,
                                                               person_responsible=staff, status=status)
        meeting_item_status.count = items_statuses.count()
        meeting_item_status.label = (num2words((items_statuses.count()))).replace("-", " ").capitalize()
        meeting_item_status.save()
        item.updated_on = timezone.now()
        item.save()
        meeting.updated_on = timezone.now()
        meeting.save()
        return HttpResponseRedirect(request.path_info)

    return render(request, 'item.html', locals())


def history(request, meeting_number, id):
    meeting = Meeting.objects.get(meeting_number=meeting_number)
    item = MeetingItem.objects.get(id=id)
    return render(request, 'history.html', locals())


def staff(request):
    all_staff = Staff.objects.all()
    return render(request, 'staff.html', locals())


def get_item_details(request):
    item_id = request.GET.get("item_id")
    item = MeetingItem.objects.get(id=int(item_id))
    data = {"id": item.id, "due date": item.due_date, "staff": item.person_responsible.names, "name": item.name}
    return JsonResponse(data, status=200)
