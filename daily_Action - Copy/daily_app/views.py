from django.shortcuts import render
from django.contrib.auth import authenticate
from django.shortcuts import render, HttpResponse, redirect
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime, timedelta, time
import datetime
from datetime import datetime as dt



from daily_app.models import * 
# Create your views here.


class TestDat:
    def __init__(self , id , created_time , status , estimated_time , description , updated_at , time_taken,  user_name , project_name , group_name , group_id , user_id): # , count):
        self.id = id
        self.created_at = created_time
        self.status = status
        self.estimated_time = estimated_time
        self.description = description
        self.updated_at = updated_at
        self.time_taken = time_taken
        self.first_name = user_name
        self.project_name = project_name
        self.group_name = group_name
        self.group_id = group_id
        self.user_id = user_id

        # self.s_count = count
class Msg:
    def __init__(self , u_name , l_name, mg , created_time):
        self.uname = u_name
        self.l_name = l_name
        self.msg = mg
        self.created_time = created_time



class GRP_MEMBER:
    def __init__(self , group_id , fname , lname, email ):
        self.group_id = group_id
        self.f_name = fname
        self.l_name = lname
        self.email = email

class ProjNotes:
    def __init__(self , id , user_id , project_id , project_name , catagory , date , description):
        self.project_notes_id = id
        self.user_id = user_id
        self.project_id = project_id
        self.project_name = project_name
        self.catagory = catagory
        self.date = date
        self.description = description

class TaskList:
    def __init__(self , user_email,  project_name , group_name , module_name , created_at , updated_at , estimated_time , time_taken , status , description):
        self.user_email = user_email
        self.project_name = project_name
        self.group_name = group_name
        self.module_name = module_name
        self.created_at = created_at
        self.updated_at = updated_at
        self.estimated_time = estimated_time
        self.time_taken = time_taken
        self.status = status
        self.description = description

def index(request):
    return render(request , "index.html")


def register(request):
    return render(request , "registration.html")


def register(request):

    return render(request , "registration.html")


def login(request):
    return render(request , "signin.html")





@login_required(login_url = "/login/")
def profile_reg(request):
    

    if request.method == "POST":
        uname = request.POST.get('uname')
        fname = request.POST.get('uname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        mob = request.POST.get('mobile') 
        user_type = request.POST.get('user_type')
        print(uname)
        print(fname)
        print(lname)
        print(email)
        print(mob)
        print(user_type)
        print(user_type.lower())

        context = {
            'f1': fname,
            'f2': lname,
            'f7': email,
            'fp': request.POST.get('mobile'),

        }

        try:
            if NewUser.objects.filter(user_name=email).first():
                messages.error(request, "Email Already Registered")
                # return redirect('/registration')
                return render(request, 'registration.html', context)

            if NewUser.objects.filter(email=email).first():
                messages.error(request, "Email Already Registered")
                return render(request, 'registration.html', context)

            if user_type.lower() == "lead":
                password = "cntx@123"
                user = NewUser(user_name=email, email=email, first_name=fname, last_name=lname,
                            mobno=mob, is_active=True,role='LEAD',)
            # password = "cntx@123"
                user.set_password(password)
                user.save()
                message = "Lead Registered successfully"
                return render(request , "registration.html" , {"message":message} )
                # return HttpResponse("REgistered Successfully")
            elif user_type.lower() == "admin":
                password = "admin@123"
                user = NewUser(user_name=email, email=email, first_name=fname, last_name=lname,
                            mobno=mob, is_active=True,role='ADMIN',)

                user.set_password(password)
                user.save() 
                message = "Admin Registered successfully"
                return render(request , "registration.html" , {"message":message} )
            elif user_type.lower() == "member":
                password = "Mcntx@123"
                user = NewUser(user_name=email, email=email, first_name=fname, last_name=lname,
                            mobno=mob, is_active=True,role='MEMBER',)

                user.set_password(password)
                user.save() 
                message = "Member Registered successfully"
                return render(request , "registration.html" , {"message":message} )
                # return HttpResponse("REgistered Successfully")

            return HttpResponse("Not REgistered Successfully")

        except Exception as e:
            print(e)
            return HttpResponse("Registration Failed")
            # return render(request, 'registration.html',
            #               {'stat': stat, 'months': MONTHS, 'year': YEAR_CHOICES, 'img': str_num,
            #                'state_ch': STATE_CHOICES,'all_labels' : all_labels})

    else:
        print("REquest is not POST")
        return HttpResponse("REquest is not POST")

def loginUser(request):
    # print(request.user)
    if request.method == "POST":
        error_message = ''
        username = request.POST.get('uname')
        password = request.POST.get('password')
        print(username, password)
        user_obj = NewUser.objects.filter(email=username).first()
        print(user_obj)
        if user_obj is None:
            messages.error(request, 'User not found.')
            # return HttpResponse("USER NOT FOUND")  
            message = "User Is not Found"
            return render(request , "signin.html" , {"message" : message})
            # return redirect('/login')


            # return render(request, 'signin.html', {'message': message})

        user = authenticate(email=username, password=password)

        if user is not None:
            print("user object role is " ,user_obj.role)
            # if not request.POST.get('remember_me', None):
            #     request.session.set_expiry(0)
            auth_login(request, user)
            # if user.is_super():
            #     # return HttpResponse("Welcome ADmin")
            #     print("Welcome super")
            #     return render(request , "super_admin_dashboard.html")
            #     # return redirect('/admindash')
            if user_obj.is_superuser:
                # message = 'Login not allowed'
                print("Welcome super")
                return render(request , "super_admin_dashboard.html")
            if user_obj.role == 'ADMIN':
                # return HttpResponse("Welcome ADmin")
                print("Welcome Admin")
                return render(request , "admin_dashboard.html")
                # return redirect('/admindash')
                # return redirect('/lead_dashboard/'+ str(user_obj.id))

            if user_obj.role == 'LEAD':
                print("Welcome Lead")
                return redirect('/lead_dashboard/'+ str(user_obj.id))
            
            if user_obj.role == 'MEMBER':
                # return HttpResponse("Welcome MEMBER")
                print("welcome Member")
                print(user_obj.id)
                # return render(request , "member_dashboard.html")
                return redirect('/member_dashboard/'+ str(user_obj.id))
            return redirect("/")

        else:
            message = 'Invalid Credentials'
            return render(request, 'signin.html', {'message': message})
            # No backend authenticated the credentials

    # if request.user.id is not None:
    #     return redirect('/')
    return render(request, 'signin.html')


@login_required(login_url = "/login/")
def create_group(request ,id):
    print("the group" , id)
    return render(request , "group_form.html")
@login_required(login_url = "/login/")
def group_create(request , id):
    print(id)
    try:
        if request.method == "POST":
            nm = request.POST.get('gname')
            print(nm)
            try:
                obj = Egroup(lead_id = id , name = nm)
                obj.save()
                print("Group saved Successfully")
                message = "Group created   Successfully"
                return render(request , "group_form.html" , {"message":message})
            except Exception as e:
                print(e)
                return HttpResponse("FAiled to save in database for group")
            
            
        # return HttpResponse("Group has been succesfully Created")
    except Exception as e:
        print(e)
        return HttpResponse(e)

    
    return render(request , "group_form.html")
# Lead dashboard as per template starts here

@login_required(login_url = "/login/")
def lead_dashboard(request , id):
    print(id)
    try:

        projects = Project.objects.all()
        total_groups = Egroup.objects.filter(lead_id = id)
        # total_groups = Egroup.objects.all()

        # filter to get the groups of the current user or lead
        user_filter = NewUser.objects.filter(id = id)
        for u in user_filter:
            groups = u.group_id
            # print(groups)
        
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)       
        to_do_list = ToDoList.objects.filter(user_id = id)

        group = ""
        proj = ""


        # if request.method == "POST" :#and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # print("========Ajax called===========")
        gid = request.POST.get("group_id")

        user_filtr = NewUser.objects.filter(role = "MEMBER")
        print(user_filtr)

        # alll the leads tasks
        
        # SAving task details from dashboard page of the member
        if request.method == "POST":
            pr_id = request.POST.get("project_id")
            usr_id =  request.POST.get("user_id") 
            group_id = request.POST.get("select_group")
            mod_name = request.POST.get("module_name")
            est_tm = request.POST.get("estimated_time")
            stat =  request.POST.get("status")
            desc =  request.POST.get("description")
            if (str(group_id) == str(0)):
                group_id = 1
            if (str(pr_id) == str(0)):
                pr_id = 1

            if (stat.lower() == "started"or stat == str(0) ) :
                status = "STARTED"
            elif (stat.lower() == "pending" ) :
                status = "PENDING"
            elif (stat.lower() == "completed" ) :
                status = "COMPLETED"
            elif (stat.lower() == "in-progress" ) :
                status = "IN PROGRESS"
            else:
                status = "NULL"
            task = Tasks(project_id = pr_id , user_id = usr_id , goup_id = group_id , module_name = mod_name , estimated_time = est_tm , status = status  , description = desc)
            task.save()

        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)

        user_list = []
        for u in user_filtr:
            if u.group_id != None:
                for i in u.group_id:
                    if (i ==  gid):
                        print(u)
                        print("This member EXists in this group")
                        user_list.append(u)

        test_list = []              
        for g in total_groups:
            # tasks = Tasks.objects.filter( goup_id = g.id ,user_id__gte=today, created_at__lt=tomorrow)
            tasks = Tasks.objects.filter( goup_id = g.id ,created_at__gte=today, created_at__lt=tomorrow)
            print("The length of the tasks is" , len(tasks))
            print("the group id is " , g.id)
            print("the group id type is " , type(g.id))
            # li = []
            # proj = []
            # usr = []
            # test_list = []
            if tasks:
                for t in tasks:
                    group = Egroup.objects.filter(id = t.goup_id)
                    for g in group:
                        group_name = g.name # let python is the group name
                    proj_obj = Project.objects.filter(id = t.project_id)
                    # proj.append(proj_obj)
                    for p in proj_obj:
                        project_name = p.name # let dpp
                    usr_obj = NewUser.objects.filter(id = t.user_id) # user id let 2
                    for u in usr_obj:
                        user_name = u.first_name # first name let user
                        user_id = u.id
                    # usr.append(usr_obj)
                    # test_list.append(TestDat(user_name ,project_name , group_name ))
                    
                    test_list.append(TestDat(t.id , t.created_at , t.status , t.estimated_time , t.description , t.updated_at , t.time_taken , user_name ,project_name , group_name , int(t.goup_id) , int(user_id)))

                    # print(test_list)
                    print("===========test list =====")
                    print("the length of the test list is " , len(test_list))
                    for t in test_list:
                        # print(t.id)
                        # print(t.first_name)
                        # print(t.project_name)
                        print("the task id is " ,t.id )
                        print("the group id is " , t.group_id)
                        print("the type group id is " , type(t.group_id))
                        print("task created on" ,t.created_at)
                        print("task status is " ,t.status)
                        print("estimated time is", t.estimated_time)
                        print("Task description is" ,t.description )
                        print("task updated at" ,t.updated_at)
                        print("time taken for the task is" ,t.time_taken )
                        print("First name of the task added by" ,t.first_name )
                        print("project name for which the task has been added" , t.project_name )
                        print("The group name for which the task has been addedd " , t.group_name )
                        # break

        # messages starts here
        message_list = []

        chat_message_obj = ChatMessage.objects.filter( receiver_id = id, created_at__gte=today, created_at__lt=tomorrow).order_by('-id')
        
        if chat_message_obj:
            for c in chat_message_obj:
                print(c.id)
                print(c.sender_id)
                print(c.receiver_id)
                print(c.text)
                usr = NewUser.objects.filter(id = c.sender_id)
                for u in usr:
                    u_name = u.first_name
                    l_name = u.last_name
                mg = c.text
                created_time = c.created_at
                                    
                message_list.append(Msg(u_name ,l_name, mg , created_time ))
        # messages ends here
        current_page = "Dashboard"

        return render(request , "lead/lead_dashboard.html" , { "tasks_list":test_list  , "total_groups":total_groups , "to_do_list":to_do_list , "message_list":message_list , "projects":projects ,"groups":groups , "currentPage":current_page  })# ,  , "test_list":test_list})# ,project_name":proj , "group_name":group , "usr":usr})
            # return render(request , "lead/lead_dashboard.html" , { "tasks":tasks , "total_groups":total_groups ,"project_name":proj , "group_name":group , "usr":usr})
        # else:
        #     return render(request , "lead/lead_dashboard.html" , { "total_groups":total_groups , "to_do_list":to_do_list })

        
        # else:    
        #     default_group = Egroup.objects.filter(lead_id=id).first()
        #     if default_group :
        #         print(default_group)
        #         print(default_group.id)


        #         # for d in default_group:
        #         #     print(d)
        #         tasks = Tasks.objects.filter(goup_id = default_group.id , created_at__gte=today, created_at__lt=tomorrow)                    
        #         proj = []
        #         usr = []
        #         test_list = []
        #         if tasks:
        #             for t in tasks:
        #                 group = Egroup.objects.filter(id = t.goup_id)
        #                 for g in group:
        #                     group_name = g.name
        #                 proj_obj = Project.objects.filter(id = t.project_id)
        #                 proj.append(proj_obj)
        #                 for p in proj_obj:
        #                     project_name = p.name
        #                 usr_obj = NewUser.objects.filter(id = t.user_id)
        #                 for u in usr_obj:
        #                     user_name = u.first_name
        #                 usr.append(usr_obj)

        #                 test_list.append(TestDat(t.id , t.created_at , t.status , t.estimated_time , t.description , t.updated_at , t.time_taken , user_name ,project_name , group_name ))

        #             # print("===========test list =====")
        #             for t in test_list:
        #                     print(t.id)
        #                     print(t.first_name)
        #                     print(t.project_name)
        #                     break
        #             return render(request , "lead/lead_dashboard.html" , { "tasks":test_list , "total_groups":total_groups ,"to_do_list":to_do_list})# ,  "test_list":test_list})#"project_name":proj , "group_name":group , "usr":usr})
        #         else:
        #             return render(request , "lead/lead_dashboard.html" , {"total_groups":total_groups , "to_do_list":to_do_list})
        #     else:
        #         return render(request , "lead/lead_dashboard.html" , {"total_groups":total_groups , "to_do_list":to_do_list})

    except Exception as e:
        print(e)
        return HttpResponse(e)

    # return render(request , "lead/lead_dashboard.html")

# Lead Dashboard as per templates ends here 

@login_required(login_url = "/login/")
def lead_dashboard_(request , id):
    print(id)

    try:

        projects = Project.objects.all()
        total_groups = Egroup.objects.filter(lead_id = id)
        # total_groups = Egroup.objects.all()

        # filter to get the groups of the current user or lead
        user_filter = NewUser.objects.filter(id = id)
        for u in user_filter:
            groups = u.group_id
            # print(groups)
        
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)       
        to_do_list = ToDoList.objects.filter(user_id = id)

        group = ""
        proj = ""


        if request.method == "POST" :#and request.headers.get('x-requested-with') == 'XMLHttpRequest':
            print("========Ajax called===========")
            gid = request.POST.get("group_id")

            user_filtr = NewUser.objects.filter(role = "MEMBER")
            print(user_filtr)

            today = datetime.date.today()
            tomorrow = today + datetime.timedelta(days=1)

            user_list = []
            for u in user_filtr:
                if u.group_id != None:
                    for i in u.group_id:
                        if (i ==  gid):
                            # print(u)
                            print("This member EXists in this group")
                            user_list.append(u)
                                

            tasks = Tasks.objects.filter( goup_id = gid ,created_at__gte=today, created_at__lt=tomorrow)
            # print("The length od the tasks is")
            li = []
            proj = []
            usr = []
            test_list = []
            if tasks:
                for t in tasks:
                    group = Egroup.objects.filter(id = t.goup_id)
                    for g in group:
                        group_name = g.name
                    proj_obj = Project.objects.filter(id = t.project_id)
                    proj.append(proj_obj)
                    for p in proj_obj:
                        project_name = p.name
                    usr_obj = NewUser.objects.filter(id = t.user_id)
                    for u in usr_obj:
                        user_name = u.first_name
                    usr.append(usr_obj)
                    # test_list.append(TestDat(user_name ,project_name , group_name ))
                    
                    test_list.append(TestDat(t.id , t.created_at , t.status , t.estimated_time , t.description , t.updated_at , t.time_taken , user_name ,project_name , group_name  ))

                    # print(test_list)
                    print("===========test list =====")
                    for t in test_list:
                        print(t.id)
                        print(t.first_name)
                        print(t.project_name)
                        break

                return render(request , "lead/lead_dashboard.html" , { "tasks":test_list  , "total_groups":total_groups , "to_do_list":to_do_list })# ,  , "test_list":test_list})# ,project_name":proj , "group_name":group , "usr":usr})
                # return render(request , "lead/lead_dashboard.html" , { "tasks":tasks , "total_groups":total_groups ,"project_name":proj , "group_name":group , "usr":usr})
            else:
                return render(request , "lead/lead_dashboard.html" , { "total_groups":total_groups , "to_do_list":to_do_list })

        
        else:    
            default_group = Egroup.objects.filter(lead_id=id).first()
            if default_group :
                print(default_group)
                print(default_group.id)


                # for d in default_group:
                #     print(d)
                tasks = Tasks.objects.filter(goup_id = default_group.id , created_at__gte=today, created_at__lt=tomorrow)                    
                proj = []
                usr = []
                test_list = []
                if tasks:
                    for t in tasks:
                        group = Egroup.objects.filter(id = t.goup_id)
                        for g in group:
                            group_name = g.name
                        proj_obj = Project.objects.filter(id = t.project_id)
                        proj.append(proj_obj)
                        for p in proj_obj:
                            project_name = p.name
                        usr_obj = NewUser.objects.filter(id = t.user_id)
                        for u in usr_obj:
                            user_name = u.first_name
                        usr.append(usr_obj)

                        test_list.append(TestDat(t.id , t.created_at , t.status , t.estimated_time , t.description , t.updated_at , t.time_taken , user_name ,project_name , group_name ))

                    # print("===========test list =====")
                    for t in test_list:
                            print(t.id)
                            print(t.first_name)
                            print(t.project_name)
                            break
                    return render(request , "lead/lead_dashboard.html" , { "tasks":test_list , "total_groups":total_groups ,"to_do_list":to_do_list})# ,  "test_list":test_list})#"project_name":proj , "group_name":group , "usr":usr})
                else:
                    return render(request , "lead/lead_dashboard.html" , {"total_groups":total_groups , "to_do_list":to_do_list})
            else:
                return render(request , "lead/lead_dashboard.html" , {"total_groups":total_groups , "to_do_list":to_do_list})

    except Exception as e:
        print(e)
        return HttpResponse(e)

    # return render(request , "lead/lead_dashboard.html")

@login_required(login_url= "login/")
def view_tasks_as_per_group(request):
    if request.method == "POST":
        gid = request.POST.get("group_id")

        user_filtr = NewUser.objects.filter(role = "MEMBER")
        print(user_filtr)

        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)

        user_list = []
        for u in user_filtr:
            if u.group_id != None:
                for i in u.group_id:
                    # print("+++++++")
                    # print(i)
                    if (i ==  gid):
                        print(u)
                        print("This member EXists in this group")
                        user_list.append(u)
                                

        tasks = Tasks.objects.filter( group_id = gid ,created_at__gte=today, created_at__lt=tomorrow)

        print(user_list)

        print("The group id is = {} ".format (str(gid)))

    return HttpResponse("Viewed group successfully")

@login_required(login_url = "/login/")
def dashboard(request):
    
    return render (request , "dashboard.html")


@login_required(login_url = "/login/")
def view_employee(request):
    users = NewUser.objects.all()
    print(users)

    return render (request , "view_employee.html" , {"users":users})


@login_required(login_url = "/login/")
def view_group(request , id):
    print(id)
    groups = Egroup.objects.filter(lead_id = id)
    print(groups)

    return render(request , "view_group.html" , {"groups":groups})

@login_required(login_url = "/login/")
def view_lead_groups(request , id):
    print(id)
    groups = Egroup.objects.filter(lead_id = id)
    print(groups)
    currentPage = "Groups"
    if request.method == "POST":
        nm = request.POST.get('group_name')
        # logo = request.POST.get('group_logo')
        print(nm)
        try:
            obj = Egroup(lead_id = id , name = nm)
            obj.save()
            print("Group saved Successfully")
            message = "Group created   Successfully"
            return render(request , "lead/groups.html" , {"groups":groups , "currentPage":currentPage})
        except Exception as e:
            print(e)

    return render(request , "lead/groups.html" , {"groups":groups , "currentPage":currentPage})
    # return render(request , "lead/groups.html")


@login_required(login_url = "/login/")
def view_member(request):
    users = NewUser.objects.all()
    print(users)
    currentPage = "Members"
    

    return render(request , "view_member.html" ,{"users":users , "currentPage":currentPage})

@login_required(login_url = "/login/")
def individual_group(request , gid):
    # print(id)
    try:
        # if request.method == "POST":
        print("Individual group function from views get called")
        # uid = request.POST['user_id']
        # gid = request.POST['group_id']
        gid = gid
        # print("user id is " + str(uid)) # here user id i.e coming from js is the id of the lead , here it is 2 , that means it is the user lead .
        # so we cant do anything with this group id . 
        # Need to filter the users those are belongs to the group whose id is coming from the js in the form of group id.

        print("group id is " + str(gid))

        # user_filtr = NewUser.objects.filter(group_id != "null")
        # user_filtr = NewUser.objects.all()
        #  View all the members while adding in the group
        user_filtr = NewUser.objects.filter(role = "MEMBER")
        print(user_filtr)

        user_list = []
        for u in user_filtr:
            if u.group_id != None:
                for i in u.group_id:
                    # print("+++++++")
                    # print(i)
                    if (i ==  gid):
                        print(u)
                        print("This member EXists in this group")
                        user_list.append(u)
        print("The user list are" , user_list)
        # return HttpResponse(user_list)
        g_name = Egroup.objects.filter(id = gid)

        return render(request , "lead/group-member.html", {"user_list":user_list , "group_name":g_name , "user_filter":user_filtr , "group_id":gid})
    except Exception as e:
        print(e)
        return HttpResponse(e)
        
    # user_filter = NewUser.objects.filter()
    # g_name = Egroup.objects.filter(id = id)
    # return render(request , "individual_group.html" ,{"group_name":g_name} )  

@login_required(login_url = "/login/")
def member_dashboard(request , id):
    try:

        projects = Project.objects.all()
        user_filter = NewUser.objects.filter(id = id)
        for u in user_filter:
            groups = u.group_id
            print(groups) 
        to_do_list = ToDoList.objects.filter(user_id = id)

        
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        tasks = Tasks.objects.filter(user_id = id , created_at__gte=today, created_at__lt=tomorrow)

        print(tasks)
        group = ""
        proj = ""
        
        if tasks:
            for t in tasks:
                print("the grouop id is from member dashboard function is = {}" .format(str(t.goup_id)))
                print("the Project id is from member dashboard function is = {}" .format(str(t.project_id)))
                group = Egroup.objects.filter(id = t.goup_id)
                proj = Project.objects.filter(id = t.project_id)

        chat_message_obj = ChatMessage.objects.filter( receiver_id = id, created_at__gte=today, created_at__lt=tomorrow).order_by('-id')

        # print("The length of the chat_message_object is" , len(chat_message_obj))

        test_list = []
        test_list_2 = []
        if chat_message_obj:
            for c in chat_message_obj:
                # print(c.id)
                # print(c.sender_id)
                # print(c.receiver_id)
                # print(c.text)
                usr = NewUser.objects.filter(id = c.sender_id)
                for u in usr:
                    u_name = u.first_name
                    l_name = u.last_name
                mg = c.text
                created_time = c.created_at
                                    
                test_list.append(Msg(u_name ,l_name, mg , created_time ))
            # test_list.append(c.text)
        

        # SAving task details from dashboard page of the member
        if request.method == "POST":
            pr_id = request.POST.get("project_id")
            usr_id =  request.POST.get("user_id") 
            group_id = request.POST.get("select_group")
            mod_name = request.POST.get("module_name")
            est_tm = request.POST.get("estimated_time")
            stat =  request.POST.get("status")
            desc =  request.POST.get("description")
            if (str(group_id) == str(0)):
                group_id = 1
            if (str(pr_id) == str(0)):
                pr_id = 1

            if (stat.lower() == "started"or stat == str(0) ) :
                status = "STARTED"
            elif (stat.lower() == "pending" ) :
                status = "PENDING"
            elif (stat.lower() == "completed" ) :
                status = "COMPLETED"
            elif (stat.lower() == "in-progress" ) :
                status = "IN PROGRESS"
            else:
                status = "NULL"
            task = Tasks(project_id = pr_id , user_id = usr_id , goup_id = group_id , module_name = mod_name , estimated_time = est_tm , status = status  , description = desc)
            task.save()
        # saving add task ends here

        # display the task details on the member dashboard starts here
            # tasks = Tasks.objects.filter( goup_id = gid ,created_at__gte=today, created_at__lt=tomorrow)
            # print("The length od the tasks is")
        li = []
        proj = []
        usr = []
        if tasks:
            for t in tasks:
                group = Egroup.objects.filter(id = t.goup_id)
                for g in group:
                    group_name = g.name
                proj_obj = Project.objects.filter(id = t.project_id)
                proj.append(proj_obj)
                for p in proj_obj:
                    project_name = p.name
                usr_obj = NewUser.objects.filter(id = t.user_id)
                for u in usr_obj:
                    user_name = u.first_name
                    user_id = u.id

                usr.append(usr_obj)
                # test_list_2.append(TestDat(user_name ,project_name , group_name ))
                
                test_list_2.append(TestDat(t.id , t.created_at , t.status , t.estimated_time , t.description , t.updated_at , t.time_taken , user_name ,project_name , group_name , t.goup_id  , int(user_id)))
        # display the task details on the member dashboard ends here
        print("the test list 2 is ")
        print(test_list_2)
        current_page = "Dashboard"

        if group != "":
            return render(request , "member_dashboard.html" ,{"tasks":test_list_2 , "group_name":group , "project_name":proj , "projects":projects , "groups":groups , "test_list":test_list , "test_list_2":test_list_2 , "currentPage":current_page , "to_do_list":to_do_list})
        else:
            return render(request , "member_dashboard.html" ,{"tasks":tasks , "projects":projects , "groups":groups , "test_list":test_list , "currentPage":current_page , "to_do_list":to_do_list})


    # else:
    #     return render(request , "member_dashboard.html" ,{"tasks":tasks ,  "projects":projects , "groups":groups})
    except Exception as e:
        print(e)
        return HttpResponse(e)


@login_required(login_url = "/login/")
def admin_dashboard(request):
    return render(request , "admin_dashboard.html")

def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res

@login_required(login_url = "/login/")
def add_members(request , id):
    print("======ADD Members function get called=====")
    # group_id = id
    group_id = id 
    print("=========================")
    print("the group id from add members function is " ,group_id)
    print("=========================")

    if request.method == "POST":
        var = request.POST.getlist('checks[]')
       
        for i in var:
            print("user id is ",i)
            filter_user = NewUser.objects.filter(id = int(i))
            filter_groups = Egroup.objects.filter(id = group_id)
            for g in filter_groups:
                print("THe group name is " ,g.name)
                for f in filter_user:
                    print(f.group_id)
                    if(f.group_id ):
                        update_group = {group_id : g.name }
                        f.group_id = Merge(f.group_id , update_group)
                        f.save()
                    else:
                        f.group_id = {group_id : g.name }
                        f.save()
        # After adding the members to the group redirect to the individual groups where each members of group can be visible
        user_filtr = NewUser.objects.filter(role = "MEMBER")
        print(user_filtr)

        user_list = []
        for u in user_filtr:
            if u.group_id != None:
                for i in u.group_id:
                    # print("+++++++")
                    # print(i)
                    if (i ==  group_id):
                        print(u)
                        print("This member EXists in this group")
                        user_list.append(u)
        print("The user list are" , user_list)
        # return HttpResponse(user_list)
        g_name = Egroup.objects.filter(id = id)
        user_filtr = NewUser.objects.filter(role = "MEMBER")
        # print(user_filtr)
        # return render(request , "individual_group.html", {"user_list":user_list , "group_name":g_name})
        return render(request , "lead/group-member.html", {"user_list":user_list , "group_name":g_name , "user_filter":user_filtr , "group_id":id})


    return redirect ('/individual_group/' + str(id))

def remove_member_from_group(request):
    if request.method == "POST":
        uid = request.POST.get("user_id")
        gid = request.POST.get("group_id")
        print(uid)
        print(gid)
        user_filter = NewUser.objects.filter(id = uid)
        for u in user_filter:
            print(u.group_id)
            print(len(u.group_id))
            before_del = u.group_id
            # del_dict = del before_del[gid]
            after_del = {}
            for key, value in before_del.items():
                if key != gid:
                    after_del[key] = value
            # update_group = {group_id : g.name }
            u.group_id = after_del # Merge(f.group_id , update_group)
            u.save()
        
        return HttpResponse("success")
    # print(id)
    return HttpResponse("The member is successfully removed from the group")



def view_groups_for_member(request , id):
    print(id)
    user_filter = NewUser.objects.filter(id = id)
    group_members = []
    for u in user_filter:
        groups = u.group_id
        # for key , value in groups.items :
        #     group_id = key
        
        # group_members.append(GRP_MEMBER(group_id , u.email , u.first_name , u.last_name ))

        print(groups)
    
    currentPage = "Groups"

    return render(request , "view_groups_for_member.html" , {"groups":groups , "currentPage":currentPage})


def create_project(request , id ):
    print(id)
    projects = Project.objects.filter(lead_id = id)
    print(projects)
    try:
        if request.method == "POST":
            lid = id
            pname = request.POST.get("project_name")
            project = Project(lead_id = lid , name = pname )
            project.save()
            print("The lead id and project names are ")
            print(lid)
            print(pname)
            return render(request , "create_project.html" , {"projects":projects})
    except Exception as e:
        print(e)
        return render(request , "create_project.html" )



    return render(request , "create_project.html" , {"projects":projects})



def member_tasks(request , id ):

    current_page = "View Task"

    projects = Project.objects.all()
    tasks = Tasks.objects.filter(user_id = id).order_by('-id')
    user_filter = NewUser.objects.filter(id = id)
    total_groups = Egroup.objects.filter(lead_id = id)


    # groups = []
    for u in user_filter:
        groups = u.group_id
        user_role = u.role

        print(groups) 
    if request.method == "POST":
        pr_id = request.POST.get("project_id")
        usr_id =  request.POST.get("user_id") 
        group_id = request.POST.get("select_group")
        mod_name = request.POST.get("module_name")
        est_tm = request.POST.get("estimated_time")
        stat =  request.POST.get("status")
        desc =  request.POST.get("description")
        if (str(group_id) == str(0)):
            group_id = 1
        if (str(pr_id) == str(0)):
            pr_id = 1
        print(pr_id)
        print(group_id)
        print(mod_name)
        print(est_tm)
        print(stat)
        print(desc)
        if (stat.lower() == "started"or stat == str(0) ) :
            status = "STARTED"
        elif (stat.lower() == "pending" ) :
            status = "PENDING"
        elif (stat.lower() == "completed" ) :
            status = "COMPLETED"
        elif (stat.lower() == "in-progress" ) :
            status = "IN PROGRESS"
        else:
            status = "NULL"
        
        cur_time = datetime.datetime.now()

        task = Tasks(project_id = pr_id , user_id = usr_id , goup_id = group_id , module_name = mod_name , estimated_time = est_tm , status = status  , description = desc , created_at = cur_time )


        task.save()
        

        


    return render (request , "member_tasks.html" , {"projects":projects , "groups":groups , "tasks":tasks , "currentPage":current_page , "user_role":user_role , "total_groups":total_groups})

def lead_view_members_task(request, id):
    print("The lead id is " , id)
    tasks_obj = Tasks.objects.all().order_by('-id')
    context = {}
    task_lists = []
    if len(tasks_obj) > 0:
        for task in tasks_obj:
            project_id = task.project_id
            project_name =""
            project_obj = Project.objects.filter(id = int(project_id))
            if len(project_obj) > 0:
                for proj in project_obj:
                    project_name = proj.name
            group_id = task.goup_id
            group_name = ""
            group_obj = Egroup.objects.filter(id = int(group_id))
            if len(group_obj) > 0:
                for group in group_obj:
                    group_name = group.name
            user_id = task.user_id
            user_obj = NewUser.objects.filter(id = int(user_id))
            user_email = ""
            if len(group_obj) > 0:
                for user in user_obj:
                    user_email = user.email
            module_name = task.module_name
            created_at = task.created_at
            updated_at = task.updated_at
            estimated_time = task.estimated_time
            time_taken = task.time_taken
            status = task.status
            description = task.description

            task_lists.append(TaskList(user_email,  project_name , group_name , module_name , created_at , updated_at , estimated_time , time_taken , status , description))

        
        context['task_lists'] = task_lists      

        return render(request , "lead/lead_view_member_tasks.html" , context )
    return render(request , "lead/lead_view_member_tasks.html" , context )
    

def update_task(request):
    print("update task function get called")

    if request.method == "POST":
        print("Post method get called")
        print(request.POST.get("task_id"))
        tid = request.POST.get("task_id")
        # data received after submitting the update button on task
        # print(tid)
        tasks = Tasks.objects.filter(id = tid)
        for t in tasks:
            print(t.id)
            print(t.project_id)
            print(t.module_name)

        return HttpResponse(tasks)

    return HttpResponse(tasks)


def update_task_after_submit(request):
    print("update task after submit function get called")
    if request.method == "POST":
        pr_id = request.POST.get("project_id_2")
        usr_id =  request.POST.get("user_id") 
        group_id = request.POST.get("select_group_2")
        mod_name = request.POST.get("module_name_2")
        est_tm = request.POST.get("estimated_time_2")
        stat =  request.POST.get("status_2")
        desc =  request.POST.get("description_2")
        tas_id =  request.POST.get("task_id")

        if (str(group_id) == str(0)):
            group_id = 1
        if (str(pr_id) == str(0)):
            pr_id = 1
        # print(pr_id)
        # print(group_id)
        # print(mod_name)
        # print(est_tm)
        print(stat.lower())
        # print(desc)
        if (stat.lower() == "started" or stat == str(0) ) :
            stats = "STARTED"
        elif (stat.lower() == "pending" ) :
            stats = "PENDING"
        elif (stat.lower() == "completed" ) :
            stats = "COMPLETED"
        elif (stat.lower() == "in-progress" ) :
            stats = "IN PROGRESS"
        else:
            stats = "NULL"
        
        upd_task = Tasks.objects.filter(id = int(tas_id)).update(project_id = pr_id , user_id = usr_id , goup_id = group_id , module_name = mod_name , estimated_time = est_tm , status = stats , description = desc)
    
        projects = Project.objects.all()
        tasks = Tasks.objects.filter(user_id = usr_id)
        user_filter = NewUser.objects.filter(id = usr_id)
        for u in user_filter:
            groups = u.group_id
            print(groups) 
    

        
        return redirect('/member_tasks/'+usr_id)

    return redirect('/member_tasks/'+usr_id)

def update_task_after_closed(request):
    print("Closed update get called ")

    if request.method == "POST":
        usr_id =  request.POST.get("user_id") 
        desc =  request.POST.get("remark")
        tas_id =  request.POST.get("task_id")
        stat = request.POST.get("status_for_close")

        print("The task id is" , tas_id)
        print("The user id id is" , usr_id)
        # print("The task id is" , tas_id)
        # print("The task id is" , tas_id)

        user = NewUser.objects.filter(id = usr_id)
        for u in user:
            user_role = u.role

        if (desc == ""):
            desc = "Default Remark"
        # print(stat.lower())
        # print(desc)
        if (stat.lower() == "started" or stat == str(0) ) :
            stats = "STARTED"
        elif (stat.lower() == "pending" ) :
            stats = "PENDING"
        elif (stat.lower() == "completed" ) :
            stats = "COMPLETED"
        elif (stat.lower() == "in-progress" ) :
            stats = "IN PROGRESS"
        else:
            stats = "NULL"

        print("The task id is ")
        print(tas_id)

        # print(stats)

        task  = Tasks.objects.filter(id = int(tas_id))
        st = ""
        for t in task:
            start_time = t.created_at
            st = st + t.description

        start_time = start_time.replace(tzinfo=None)

        cur_time = datetime.datetime.now()

        date_diff = cur_time - start_time
        print(date_diff)
        secs = date_diff.total_seconds() / 3600
        print(secs)
        h = date_diff.total_seconds()//3600
        m = (date_diff.total_seconds()%3600) // 60
        sec =(date_diff.total_seconds()%3600)%60

        # h = abs(int(h) - 5)
        # m = abs(int(m) - 30)
        print("==================The started  time is ============")
        print(start_time)
        print("==================The Current time  is ============")
        print(cur_time)
        print("==================The total time taken to complete the task is ============")
        print ("%d:%d:%d" %(h,m,sec))



        diff_hours = ("%d:%d:%d" %(h,m,sec))


      
        remark = "*****"+desc
        descript = st + remark

        # print(st)
        # print(remark)
        # print(descript)
        print("The status of the task to be " , stat)
        if (stats == "COMPLETED"):
            upd_task = Tasks.objects.filter(id = int(tas_id)).update( status = stats , description = descript , time_taken = diff_hours ,updated_at = cur_time)
        else:
            upd_task = Tasks.objects.filter(id = int(tas_id)).update( status = stats , description = descript , updated_at = cur_time)
    

        # print("user role is" , user_role)
        if user_role == "MEMBER":
            return redirect("/member_dashboard/"+str(usr_id))
        if user_role == "LEAD":
            return redirect("/lead_dashboard/"+str(usr_id))
        # return redirect('/member_dashboard/'+usr_id)

    if user_role == "MEMBER":
        return redirect("/member_dashboard/"+str(usr_id))
    if user_role == "LEAD":
        return redirect("/lead_dashboard/"+str(usr_id))
    # return redirect('/member_dashboard/'+usr_id)




def add_notes(request , id):

    
    user = NewUser.objects.filter(id = id)
    for u in user:
        user_role = u.role

    if request.method == "POST":

        uid = id
        title = request.POST.get("notes_title")
        des = request.POST.get("note")

        add_note = ToDoList(user_id = uid , title = title , description = des)
        add_note.save()

        print("user role is" , user_role)
        if user_role == "MEMBER":
            return redirect("/member_dashboard/"+str(id))
        if user_role == "LEAD":
            return redirect("/lead_dashboard/"+str(id))
    
    if user_role == "MEMBER":
        return redirect("/member_dashboard/"+str(id))
    if user_role == "LEAD":
        return redirect("/lead_dashboard/"+str(id))



def to_do_update(request , id):
    print("-------to_be done notes ajax get caelld-------")
    user = NewUser.objects.filter(id = id)
    for u in user:
        user_role = u.role
    if request.method == "POST"  and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        todo_id = request.POST.get("todo_id")
        print(id)
        print(todo_id)
        todo = ToDoList.objects.filter(user_id = id , id = todo_id).update(status="DONE")

        if user_role == "MEMBER":
            return redirect("/member_dashboard/"+str(id))
        if user_role == "LEAD":
            return redirect("/lead_dashboard/"+str(id))

        return HttpResponse("notes updated from views ")
        # return redirect("/lead_dashboard/" + str(id))
    
    if user_role == "MEMBER":
        return redirect("/member_dashboard/"+str(id))
    if user_role == "LEAD":
        return redirect("/lead_dashboard/"+str(id))

    # return redirect("/lead_dashboard/" + str(id))




def to_do_remove(request , id):
    print("-------to_be done notes ajax get caelld-------")
    user = NewUser.objects.filter(id = uid)
    for u in user:
        user_role = u.role

    if request.method == "POST"  and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        todo_id = request.POST.get("todo_id")
        print(id)
        print(todo_id)
        todo = ToDoList.objects.filter(user_id = id , id = todo_id).update(status="REMOVE")

        if user_role == "MEMBER":
            return redirect("/member_dashboard/"+str(id))
        if user_role == "LEAD":
            return redirect("/lead_dashboard/"+str(id))

        return HttpResponse("notes removed from views ")
        # return redirect("/lead_dashboard/" + str(id))

    if user_role == "MEMBER":
        return redirect("/member_dashboard/"+str(id))
    if user_role == "LEAD":
        return redirect("/lead_dashboard/"+str(id))

    # return redirect("/lead_dashboard/" + str(id))




def  to_do_hold_for_now(request , id):
    print("-------to_be done notes ajax get caelld-------")

    user = NewUser.objects.filter(id = uid)
    for u in user:
        user_role = u.role

    if request.method == "POST"  and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        todo_id = request.POST.get("todo_id")
        print(id)
        print(todo_id)
        todo = ToDoList.objects.filter(user_id = id , id = todo_id).update(status="HOLD_FOR_NOW")

        if user_role == "MEMBER":
            return redirect("/member_dashboard/"+str(id))
        if user_role == "LEAD":
            return redirect("/lead_dashboard/"+str(id))

        return HttpResponse("notes HOLD_FOR_NOW from views ")
        # return redirect("/lead_dashboard/" + str(id))

    if user_role == "MEMBER":
        return redirect("/member_dashboard/"+str(id))
    if user_role == "LEAD":
        return redirect("/lead_dashboard/"+str(id))
    # return redirect("/lead_dashboard/" + str(id))



def chat(request , user_name):
    print(user_name)
    user = NewUser.objects.filter(user_name = user_name)
    messages = Message.objects.all()
    for u in user:

        print(u.id)
        msg = Message.objects.filter(sender_id = u.id)

    return render(request , "chat_message.html" , {"messages":msg} )



# def view_leads(request):
#     leads = NewUser.objects,filter(role = "LEAD")
#     return render("view_leads.html" , {"leads":""})

def save_message(request):
    print("Save message get called from ajax")
    if request.method == "POST" :# and request.headers.get('x-requested-with') == 'XMLHttpRequest':

        sndr_id = request.POST.get("sender_id")
        rcvr_id = request.POST.get("receiver_id")
        msg = request.POST.get("message")

        new_msg = ChatMessage(sender_id = sndr_id , receiver_id = rcvr_id , text = msg)
        new_msg.save()
        return redirect('/view_member/')


    return redirect('/view_member/')



def view_message(request):
    return render(request , "messages.html")



def group_member(request):
    return render(request , "lead/group-member.html")

def project_notes(request , id):

    projects = Project.objects.all()
    project_notes_obj = ProjectNotes.objects.filter(user_id=id)
    project_notes = []

    for notes in project_notes_obj:
        note_id = notes.id
        user_id = notes.user_id
        catagory = notes.catagory
        date = notes.date
        description = notes.description
        prid = notes.project_id
        proj_name = ""
        #  Using id filter the project object
        proj_obj = Project.objects.filter(id = int(prid))
        # Get the project name
        for proj in  proj_obj:
            proj_name = proj.name
        
        project_notes.append(ProjNotes(note_id ,user_id,prid , proj_name , catagory ,date , description ))
        
    currentPage = 'Project Notes'

    # project_notes = ProjectNotes.objects.filter()

    if request.method == "POST":
        prj = request.POST.get("project")
        cat = request.POST.get("catagory")
        dt = request.POST.get("date")
        desc = request.POST.get("description")
        print("project id is" , prj)
        print("cat id is" , cat)
        print("dt id is" , dt)
        print("desc is" , desc)

        prj_note = ProjectNotes(user_id = id ,project_id = prj , catagory = cat , date = dt , description = desc)
        prj_note.save()

        return redirect('/project_notes/'+str(id))

        # return render(request , "project_notes.html" ,{"currentPage":currentPage , "projects":projects , "project_notes":project_notes} )

    return render(request , "lead/project_notes.html" ,{"currentPage":currentPage , "projects":projects , "project_notes":project_notes} )




def member_project_notes(request , id):

    projects = Project.objects.all()
    project_notes_obj = ProjectNotes.objects.filter(user_id=id)
    project_notes = []

    for notes in project_notes_obj:
        note_id = notes.id
        user_id = notes.user_id
        catagory = notes.catagory
        date = notes.date
        description = notes.description
        prid = notes.project_id
        proj_name = ""
        #  Using id filter the project object
        proj_obj = Project.objects.filter(id = int(prid))
        # Get the project name
        for proj in  proj_obj:
            proj_name = proj.name
        
        project_notes.append(ProjNotes(note_id ,user_id,prid , proj_name , catagory ,date , description ))
        
    currentPage = 'Project Notes'

    # project_notes = ProjectNotes.objects.filter()

    if request.method == "POST":
        prj = request.POST.get("project")
        cat = request.POST.get("catagory")
        dt = request.POST.get("date")
        desc = request.POST.get("description")
        print("project id is" , prj)
        print("cat id is" , cat)
        print("dt id is" , dt)
        print("desc is" , desc)

        prj_note = ProjectNotes(user_id = id ,project_id = prj , catagory = cat , date = dt , description = desc)
        prj_note.save()

        return redirect('/project_notes/'+str(id))

        # return render(request , "project_notes.html" ,{"currentPage":currentPage , "projects":projects , "project_notes":project_notes} )

    return render(request , "project_notes.html" ,{"currentPage":currentPage , "projects":projects , "project_notes":project_notes} )