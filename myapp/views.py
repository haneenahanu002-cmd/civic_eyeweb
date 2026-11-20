import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render, redirect


# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from pip._vendor.distro.distro import name

from myapp.models import Department, Complaint, Appreview, Registration, Action


def login_get(request):
    return render(request,'login_index.html')
@csrf_exempt
def login_post(request):
    username=request.POST['username']
    password=request.POST['password']



    print("====================",username,password)
    log=authenticate(username=username,password=password)


    print(log,"jjjjjj")
    if log is not None:
        login(request,log)


        if log.groups.filter(name='admin'):
            return redirect('/myapp/admin_view_dashboard/#abc')
        elif log.groups.filter(name='Department').exists():
            print("llllllllllllllllllllll")
            return redirect('/myapp/dept_home/')
        else:
            messages.warning(request,'Invalid username or password')
            return redirect('/myapp/login/')
    else:
        messages.warning(request,'Invalid username or password')
        return redirect('/myapp/login/')


# user=User.objects.get(username="waterdept@gmail.com")
# user.set_password(4567654123)
# user.save()

@login_required(login_url='/myapp/login/')
def a_home(request):
    return render(request,'admin/home_index.html')
    # return render(request,'admin/home.html')

@login_required(login_url='/myapp/login/')
def add_department(request):
    return render(request,'admin/add department.html')

@login_required(login_url='/myapp/login/')
def add_department_post(request):
    department_name=request.POST['name']
    Email_address=request.POST['Email']
    phone_number=request.POST['telephone']
    Description=request.POST['Description']




    if User.objects.filter(username=Email_address).exists():
        messages.error(request, 'Username already existed ')

        return redirect('/myapp/add_department/')

    elif Department.objects.filter(dname=department_name).exists():
        messages.error(request, 'Depatment name already existed')

        return redirect('/myapp/add_department/')

    elif Department.objects.filter(email=Email_address).exists():
        messages.error(request, 'Email already existed')

        return redirect('/myapp/add_department/')

    import random
    new_pass = random.randint(00000000, 99999999)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("civiceyeofficial@gmail.com", " qkwx axxw nitl avui")  # App Password
    to = Email_address
    subject = "Test Email"
    body = "Your new password is " + str(new_pass)
    msg = f"Subject: {subject}\n\n{body}"
    server.sendmail("s@gmail.com", to, msg)  # Disconnect from the server
    server.quit()

    dept=User.objects.create_user(username=Email_address,password=new_pass)
    dept.groups.add(Group.objects.get(name="Department"))
    dept.save()

    data=Department()
    data.dname=department_name
    data.description=Description
    data.email=Email_address
    data.phone=phone_number
    data.USER=dept
    data.save()
    messages.success(request,'Department added successfully')
    return redirect('/myapp/view_department/')





@login_required(login_url='/myapp/login/')
def view_department(request):
    data=Department.objects.all()
    return render(request,'admin/view department.html',{'data':data})

@login_required(login_url='/myapp/login/')
def edit_department(request,id):
    data=Department.objects.get(id=id)
    return render(request,'admin/edit department.html',{'data':data})
@login_required(login_url='/myapp/login/')
def edit_department_post(request):
    Department_name=request.POST['name']
    Email_address=request.POST['Email']
    phone_number=request.POST['number']
    Description=request.POST['description']
    id=request.POST['id']
    data=Department.objects.get(id=id)
    data.dname=Department_name
    data.description=Description
    data.email=Email_address
    data.phone=phone_number
    data.save()
    messages.success(request,'Department edited successfully')
    return redirect('/myapp/view_department/#abc')


@login_required(login_url='/myapp/login/')
def view_registered(request):
    data=Registration.objects.all()
    return render(request,'admin/view registered users.html',{'data':data})

@login_required(login_url='/myapp/login/')
def change_password(request):
    return render(request,'admin/change password.html')

@login_required(login_url='/myapp/login/')
def change_password_post(request):
    old_password=request.POST['old_password']
    new_password=request.POST['new_password']
    confirm_password=request.POST['confirm_password']
    data=request.user
    if not data.check_password(old_password):
        messages.error(request,"invalid password")
        return render(request,'admin/change password.html')
    elif new_password==confirm_password:
        data.set_password(new_password)
        data.save()
        messages.success(request,"password changed successfully")
        return redirect('/myapp/login/')

@login_required(login_url='/myapp/login/')
def view_appreview(request):
    data=Appreview.objects.all()
    return render(request,'admin/view  appreview.html',{'data':data})
@login_required(login_url='/myapp/login/')
def view_complaint(request):
    data=Complaint.objects.all()
    return render(request,'admin/view complaint.html',{'data':data})
@login_required(login_url='/myapp/login/')
def viewcomplaint_more(request,id):
    data=Complaint.objects.get(id=id)
    dataaction= Action.objects.filter(COMPLAINT_id=id)
    return render(request,'admin/viewcomplaint more.html',{'data':data,'dataaction':dataaction})

@login_required(login_url='/myapp/login/')
def delete_department(request,id):
    Department.objects.filter(USER_id=id).delete()
    User.objects.filter(id=id).delete()
    messages.success(request,'Department deleted successfully')
    return redirect('/myapp/view_department/#abc')
@login_required(login_url='/myapp/login/')
def dept_view_profile(request):
    data=Department.objects.get(USER=request.user)
    return render(request, 'department/dept view_profile.html',{'data':data})

@login_required(login_url='/myapp/login/')
def dept_change_password(request):
    return render(request, 'Department/dept change password.html')

@login_required(login_url='/myapp/login/')
def dept_change_password_post(request):
    old_password=request.POST['old_password']
    new_password=request.POST['new_password']
    confirm_password=request.POST['confirm_password']
    data=request.user
    if not data.check_password(old_password):
        messages.error(request,"invalid password")
        return render(request,'Department/dept change password.html')
    elif new_password==confirm_password:
        data.set_password(new_password)
        data.save()
        messages.success(request,"password changed successfully")
        return redirect('/myapp/login/')

@login_required(login_url='/myapp/login/')
def viewfiltered_complaint(request):
    # did=Department.objects.get(USER=request.user)
    data=Complaint.objects.filter(DEPARTMENT__USER_id=request.user.id)
    return render(request,'department/viewfiltered complaint.html',{'data':data})


def change_status(request):
    status=request.POST['status']
    id=request.POST['id']
    Complaint.objects.filter(id=id).update(solvedstatus=status)
    return redirect('/myapp/viewfiltered_complaint/#abc')


@login_required(login_url='/myapp/login/')
def take_action(request,id):
    data=Complaint.objects.get(id=id)

    ac=Action.objects.filter(COMPLAINT_id=id)


    return render(request,'department/take action.html',{'data':data,'data1':ac})


@login_required(login_url='/myapp/login/')
def create_action(request,id):
    return render(request,'department/create action.html',{'id':id})
@login_required(login_url='/myapp/login/')
def create_action_post(request):
    action=request.POST['action']
    id=request.POST['id']
    # Complaint.objects.filter(id=id).update(solvedstatus='replied')

    v=Complaint.objects.get(id=id)
    email= v.REGISTRATION.email

    print(email,"hhhhhhhhhhhhhhhhh")

    a=Action()
    a.COMPLAINT_id=id
    from datetime import datetime
    a.date_of_action_taken=datetime.now().today()
    a.action=action
    a.save()

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("civiceyeofficial@gmail.com", "qkwx axxw nitl avui")  # App Password
    to = email
    subject = "Test Email"
    body = "The action taken is " + str(action)
    msg = f"Subject: {subject}\n\n{body}"
    server.sendmail("s@gmail.com", to, msg)  # Disconnect from the server
    server.quit()




    messages.success(request,'Action taken successfully')

    return redirect('/myapp/viewfiltered_complaint/')
@login_required(login_url='/myapp/login/')
def dept_home(request):
    return render(request,'department/home_index.html')

#===============User===================

@csrf_exempt
def user_signup(request):
    name=request.POST['uname']
    email=request.POST['uemail']
    phone=request.POST['uphoneno']
    place=request.POST['uplace']
    city=request.POST['ucity']
    state=request.POST['ustate']
    pincode=request.POST['upincode']
    password=request.POST['upassword']
    gender=request.POST['ugender']
    confirmpassword=request.POST['uconfirmpassword']
    photo=request.FILES['photo']

    from datetime import  datetime
    date=datetime.now().strftime("%Y%m%d-%H%M%S")+".jpg"
    fs=FileSystemStorage()
    fs.save(date,photo)
    path=fs.url(date)

    if User.objects.filter(username=email).exists():
        return JsonResponse({'status':'no'})

    elif Registration.objects.filter(email=email,phone=phone).exists():
        return JsonResponse({'status':'no'})


    elif Registration.objects.filter(phone=phone).exists():
        return JsonResponse({'status':'no'})

    else:
        user=User.objects.create_user(username=email,password=confirmpassword)
        user.groups.add(Group.objects.get(name='user'))
        user.save()

        r=Registration()
        r.name=name
        r.gender=gender
        r.photo=path
        r.email=email
        r.phone=phone
        r.place=place
        r.city=city
        r.state=state
        r.pincode=pincode
        r.USER=user

        r.save()
        return JsonResponse({'status':'ok'})



@csrf_exempt
def user_login(request):
    username=request.POST['username']
    password=request.POST['password']
    log = authenticate(request, username=username, password=password)
    print(log)
    if log is not None:
        login(request, log)
        dd=request.user
        if log.groups.filter(name='user'):
            return JsonResponse({'status':'ok','lid':str(dd.id)})
        else:
            return JsonResponse({'status': 'no'})
    else:
        return JsonResponse({'status':'no'})

@csrf_exempt
def user_viewprofile(request):
    lid=request.POST['lid']
    data=Registration.objects.get(USER=lid)
    return JsonResponse({'status':'ok','name':data.name,
                         'gender':data.gender,'photo':data.photo,
                         'email':data.email,'phone':data.phone,
                         'place':data.place,'city':data.city,
                         'state':data.state,'pincode':data.pincode})

@csrf_exempt
def user_editprofile(request):
    username=request.POST['username']
    email=request.POST['email']
    phone=request.POST['phone']
    place=request.POST['place']
    city=request.POST['city']
    state=request.POST['state']
    pincode=request.POST['pincode']
    gender=request.POST['gender']
    lid = request.POST['lid']
    r = Registration.objects.get(USER=lid)


    if 'photo' in request.FILES:
        photo = request.FILES['photo']
        if photo !="":


            from datetime import datetime
            date = datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg"
            fs = FileSystemStorage()
            fs.save(date, photo)
            path = fs.url(date)
            r.photo = path

    r.name = username
    r.gender = gender
    r.email = email
    r.phone = phone
    r.place = place
    r.city = city
    r.state = state
    r.pincode = pincode
    r.save()
    return JsonResponse({'status': 'ok'})

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from .models import Complaint, Department, Registration  # Adjust as per your app structure


def getdepartmentnamefromtext(complaint):
    deps = ""

    d = Department.objects.all()
    for i in d:
        deps = deps + " " + i.dname + ","

    deps = deps[: len(deps) - 1]

    import google.generativeai as genai
    from PIL import Image

    genai.configure(api_key="AIzaSyB9w_Ow_JnZm17_lMj7XmOE00A8Bbuxhrw")  # Replace with your actual key

    def load_image(image_path):
        try:
            image = Image.open(image_path)
            return image
        except Exception as e:
            print("Error loading image:", e)
            return None

    def interpret_prescription():
        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content(
                [
                    "My Complaint is "+complaint+".I need to get department for the complaint. Department are " + deps + ". Give only the department name",

                ],
                stream=False
            )
            return response.text.replace("*", "")  # Remove asterisks
        except Exception as e:
            for m in genai.list_models():
                print("model name", m.name)

            return "Gemini API Error:"

    # image_path = image  # Change this if needed
    # image = load_image(image_path)
    # if image is None:
    #     return
    result = interpret_prescription()
    print(result)

    return result


# def getdepartmentnamefromimage(image):
#
#     deps=""
#
#     d=Department.objects.all()
#     for i in d:
#         deps= deps+" "+i.dname +","
#
#     deps= deps[: len(deps)-1]
#
#
#     import google.generativeai as genai
#     from PIL import Image
#
#     # genai.configure(api_key="AIzaSyB9w_Ow_JnZm17_lMj7XmOE00A8Bbuxhrw")  # Replace with your actual key
#     genai.configure(api_key="AIzaSyDun2ueeWXf8T8WfWvuhj2jdI8RKj2sUJ4")
#
#
#
#     # Replace with your actual key
#
#     def load_image(image_path):
#         try:
#             image = Image.open(image_path)
#             return image
#         except Exception as e:
#             print("Error loading image:",e)
#             return None
#
#     def interpret_prescription(image):
#         try:
#
#
#             model = genai.GenerativeModel('gemini-2.5-pro')
#
#
#
#             response = model.generate_content(
#                 [
#                     "Here am uploading a problem image need to identify which department get this problem. Department are "+deps+". Give only the department name",
#                     image
#                 ],
#                 stream=False
#             )
#             return response.text.replace("*", "")  # Remove asterisks
#         except Exception as e:
#
#
#             return "Gemini API Error:"
#
#     image_path = image  # Change this if needed
#     image = load_image(image_path)
#     if image is None:
#         return
#     result = interpret_prescription(image)
#     print(result,"================================================================")
#
#     return result



@csrf_exempt
def user_sendcomplaint(request):
    complaint = request.POST['complaint']
    lid = request.POST['lid']
    latitude = request.POST['latitude']
    longitude = request.POST['longitude']
    location = request.POST['location_name']
    print(location, "================")




    department = getdepartmentnamefromtext(complaint)

    c = Complaint()
    if 'photo' in request.FILES:
        photo = request.FILES['photo']
        from datetime import datetime
        date = datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg"
        fs = FileSystemStorage()
        fs.save(date, photo)
        path = fs.url(date)
        c.photoproof = path



        # mediapath="C:\\Riss\\CivicEyeWeb\\Civic_Eye\\media\\"+date

        # imagedepartment= getdepartmentnamefromimage(mediapath)




    from datetime import datetime
    c.date = datetime.now().today()
    c.complaint = complaint
    c.category = department

    ############priority logic#############
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    import torch

    # Choose a model that has severity/priority-like labels
    model_name = "CIRCL/vulnerability-severity-classification-roberta-base"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)

    labels = ["low", "medium", "high", "critical"]
    # Function to predict priority/severity from input text
    def predict_priority(text):
        # Tokenize the input text for the model
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        # Disable gradient calculation for inference
        with torch.no_grad():
            # Get model outputs (logits)
            outputs = model(**inputs)
            # Convert logits to probabilities using softmax
            probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        # Find the index of the highest probability
        max_idx = torch.argmax(probs, dim=-1).item()
        # Return the label and its confidence score
        return labels[max_idx], probs[0][max_idx].item()

    # Example
    # complaint = "The street light near my house is flickering."
    priority, confidence = predict_priority(complaint)
    print( priority)



    c.priority = priority
    c.solvedstatus = "pending"
    c.latitude = latitude
    c.longitude = longitude
    c.placename = location
    c.REGISTRATION = Registration.objects.get(USER=lid)

    print(department,"likhil")
    print("ggggg")


    a=Department.objects.filter(dname=department)
    print("hhhhhh",a)
    c.DEPARTMENT = Department.objects.get(dname=department)  # ✅ Auto-assigned
    c.save()

    return JsonResponse({'status': 'ok'})





@csrf_exempt
def user_viewcomplaint(request):
    lid=request.POST['lid']
    data=Action.objects.filter(COMPLAINT__REGISTRATION__USER_id=lid)
    l=[]
    for i in data:
        l.append({
            'id':i.id,
            'date':i.COMPLAINT.date,
            'complaint':i.COMPLAINT.complaint,
            'photoproof':i.COMPLAINT.photoproof,
            'category':i.COMPLAINT.category,
            'priority':i.COMPLAINT.priority,
            'solvedstatus':i.COMPLAINT.solvedstatus,
            'latitude':i.COMPLAINT.latitude,
            'longitude':i.COMPLAINT.longitude,
            'placename':i.COMPLAINT.placename,
            'departmentname':i.COMPLAINT.DEPARTMENT.dname,
            'action':i.action
        })
    print(l)
    return JsonResponse({'status': 'ok','data':l})

@csrf_exempt
def user_changepassword(request):
    old_password = request.POST['old_password']
    new_password = request.POST['new_password']
    confirm_password = request.POST['confirm_password']
    lid=request.POST['lid']
    data=User.objects.get(id=lid)
    if not data.check_password(old_password):
        return JsonResponse({'status': 'no'})

    elif(new_password==confirm_password):
        data.set_password(confirm_password)
        data.save()
        return JsonResponse({'status':'ok'})

    else:

        return JsonResponse({'status': 'no'})


@csrf_exempt
def user_sendappreview(request):
    review=request.POST['review']
    rating=request.POST['rating']
    lid=request.POST['lid']

    from datetime import datetime


    c = Appreview()

    c.date = datetime.now().today()
    c.rating =  rating
    c.review =  review
    c.REGISTRATION = Registration.objects.get(USER=lid)
    c.save()
    return JsonResponse({'status': 'ok'})

@csrf_exempt
def user_viewappreview(request):
    lid = request.POST['lid']
    data = Appreview.objects.filter(REGISTRATION__USER=lid)
    l = []
    for i in data:
        l.append({
            'id': i.id,
            'rating': i.rating,
            'date': i.date,
            'review': i.review,
        })
    print(l)
    return JsonResponse({'status': 'ok', 'data': l})



def logout_get(request):
    logout(request)
    return redirect('/myapp/login/')



@csrf_exempt
def android_forget_password_post(request):
    email = request.POST['emailid']
    if not email:
        return JsonResponse({'status': 'error', 'message': 'Email is required'})

    try:
        user = User.objects.get(username=email)
        print(email)

        # Generate new password
        new_pass = str(random.randint(10000000, 99999999))
        user.password = make_password(new_pass)
        user.save()


        print("kkkkkkkkkkkk")
        # Email configuration
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "civiceyeofficial@gmail.com"
        app_password = "qkwx axxw nitl avui"

        subject = "Your New Password"
        body = f"Your new password is: {new_pass}"
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, app_password)
        server.send_message(message)
        server.quit()
        print("llllllllllllll")

        return JsonResponse({'status': 'ok', 'message': 'Password sent to your email'})

    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Email not found'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Email send error: {str(e)}'})



@login_required(login_url='/myapp/login/')
def admin_view_dashboard(request):

    dep=Department.objects.all()

    deps=[]
    complaintcnt=[]

    for i in dep:

        totdep=Department.objects.all().count()
        deps.append(i.dname)
        totalcomplaintcnt= Complaint.objects.filter(DEPARTMENT=i).count()
        totalrepliedcnt= Complaint.objects.filter(DEPARTMENT=i,solvedstatus="replied").count()
        totalpendingcnt= Complaint.objects.filter(DEPARTMENT=i,solvedstatus="pending").count()

        deps.append(
            {
                'dname': i.dname,
                'totalcomplaintcnt': totalcomplaintcnt,
                'totalrepliedcnt': totalrepliedcnt,
                'totalpendingcnt': totalpendingcnt,
            }
        )
    return render(request,"admin/admin_view_dashboard.html",{'data':deps,'totdep':totdep})





def forget_password(request):

    if request.method=='POST':
        
        emailid= request.POST["emailid"]
        print(emailid,"==")
        d=User.objects.filter(username=emailid)
        if d.exists():

            import  random
            r=random.randint(1000,10000000000)

            d=d[0]
            d.set_password(str(r))
            d.last_name=str(r)
            d.save()


            



            messages.success(request,'New password has been sent to your email id')

            return redirect('/myapp/login/')
        
        else:
            messages.error(request,'Email id not found')

            return redirect('/myapp/forget_password/')
        

    return render(request,'forget_password.html')   




def check(request):

    print(request.user)

    try:
        id=int(request.user.id)

        print("yes")
        return JsonResponse(
            {
                'status':'ok'
            }
        )
    except Exception as a:

        print("no")
        return JsonResponse(
            {
                'status':'no'
            }
        )