from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout, get_user_model
from scholarsys.models import Student, Staff, Achievement, Material, Scholarship, all_cate
from scholarsys.forms import SignupForm, AchievementForm, ApplyScholarshipForm, AddScholarshipForm


def login_required(func):
    def wrapper(request, *args):
        if request.user.is_authenticated():
            return func(request, *args)
        else:
            return redirect("/login")
    return wrapper


def staff_login_required(func):
    def wrapper(request, *args):
        if request.user.is_authenticated() and request.user.is_staff is False:
            logout(request)
            return redirect("/login")
        elif request.user.is_authenticated() and request.user.is_staff is True:
            return func(request, *args)
        else:
            return redirect("/login")
    return wrapper


def login(request):
    if request.method != 'POST':
        return render(request, 'scholarsys/login.html')

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = authenticate(username=username, password=password)

    if user is not None and user.is_active:
        # Correct password, and the user is marked "active"
        auth_login(request, user)
        # Redirect to a success page.
        return render(request, 'scholarsys/index.html')
    else:
        # Show an error page
        return render(request, 'scholarsys/login.html')


@login_required
def home(request):
        if request.user.is_staff is True:
            staff = Staff.objects.get(user_id=request.user.id)
        else:
            stu = Student.objects.get(user_id=request.user.id)
            achi = Achievement.objects.filter(student=stu).values()
        scho = Scholarship.objects.filter(is_active=True)
        return render(request, 'scholarsys/index.html', locals())


def signup(request):
    path = request.get_full_path()
    if request.method == 'POST':
        form = SignupForm(data=request.POST, auto_id="%s")
        if form.is_valid():
            user_model = get_user_model()
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user_type = form.cleaned_data['user_type']
            cus_id = form.cleaned_data['cus_id']
            if user_type == 'True':
                user = user_model.objects.create_user(username=username,
                                                      email=email, password=password,
                                                      is_active=False, is_staff=True)
                user.save()
                Staff.objects.create(user=user, staff_id=cus_id)
                auth_user = authenticate(username=username, password=password)
                auth_login(request, auth_user)
            else:
                user = user_model.objects.create_user(username=username,
                                                      email=email, password=password,
                                                      is_active=True, is_staff=False)
                user.save()
                Student.objects.create(user=user, stu_id=cus_id)
                auth_user = authenticate(username=username, password=password,
                                         is_active=True, is_staff=False)
                auth_login(request, auth_user)

            return redirect("home")
    else:
        form = SignupForm(auto_id="%s")
    return render(request, 'scholarsys/signup.html', locals())


def logout_view(request):
    logout(request)
    return redirect('home')


# For student user, 
#   show all the Applied Scholarship's info belongs to it
#   cancle an Scholarship application
#   add new Scholarship application
# For staff user, 
#   show all the Scholarship
#   add new Scholarship
@login_required
def manage_scholarship(request):
    if request.method == 'POST':
        return HttpResponse("MethodError")
    stu = Student.objects.filter(user_id=request.user.id)
    tea = Staff.objects.filter(user_id=request.user.id)
    if request.user.is_staff is not True:
        schos = Scholarship.objects.filter(student=stu, is_active=True)
        av_scho = Scholarship.objects.filter(is_active=True).exclude(student=stu)
        return render(request, "scholarsys/scholarship.html", locals())
    else:
        schos = Scholarship.objects.filter(is_active=True)
        form = AddScholarshipForm()
        return render(request, "scholarsys/scholarship.html", locals())


@login_required
def cancel_scholarship(request):
    if request.method == "POST":
        if request.user.is_staff is not True:
            stu = Student.objects.get(user_id=request.user.id)
            scho_id = Scholarship.objects.get(student=stu, id=int(request.POST['id'])).id
            stu.scholarship.remove(scho_id)
            return redirect('manage_Scholarship')
        else:
            return HttpResponse("Error:)")
    else:
        return HttpResponse("Method Error:)")


@login_required
def apply_scholarship(request):
    if request.method == 'POST':
        stu = Student.objects.get(user_id=request.user.id)
        form = ApplyScholarshipForm(request.POST)
        cd = form.data
        applied_scho_id = Scholarship.objects.get(id=int(cd["id"][0])).id
        stu.scholarship.add(applied_scho_id)
        stu.save()
        return redirect('manage_Scholarship')


@staff_login_required
def add_scholarship(request):
    if request.method == 'POST':
        teacher = Staff.objects.get(user_id=request.user.id)
        form = AddScholarshipForm(request.POST)
        cd = form.data
        new_scho = Scholarship.objects.create(category=cd["category"], bonus=cd['bonus'],
                                              capacity=cd['capacity'], is_active=True,
                                              distributer=teacher)
        new_scho.save()
        return redirect('/Scholarship')
    else:
        return HttpResponse("MethodError")


@staff_login_required
def delete_scholarship(request):
    # need teacher auth
    if request.method == 'POST' and request.user.is_staff is True:
        delete_id = int(request.POST["id"])
        ds = Scholarship.objects.get(id=delete_id)
        ds.is_active = False
        ds.save()
        return redirect('/Scholarship')
    else:
        return HttpResponse("MethodError")


# For student user, 
#   show all the stated Achievement's info(name/category/status)
#   delete stated Achievement
#   add new stated Achievement
# For staff user, 
#   show all the Achievement
#   verify the Achievement(change the status)
@login_required
def manage_achievement(request):
    if request.method == "POST":
        return HttpResponse("Method Error")
    if request.user.is_staff is True:
        staff = Staff.objects.get(user_id=request.user.id)
        achis = Achievement.objects.all()
        return render(request, 'scholarsys/achievement.html', locals())
    else:
        stu = Student.objects.filter(user_id=request.user.id)
        achis = Achievement.objects.filter(student=stu)
        form = AchievementForm()
        return render(request, 'scholarsys/achievement.html', locals())


@staff_login_required
def verify_achievement(request):
    # need auth
    if request.method != 'POST':
        return HttpResponse("Method Error")
    verified_id = request.POST["id"]
    ds = Achievement.objects.get(id=verified_id)
    ds.status = not ds.status
    ds.save()
    return redirect('/Achievement')


@staff_login_required
def delete_achievement(request):
    # auth problem, this is only auth to teacher and it's owner
    if request.method != 'POST':
        return HttpResponse("Method Error")
    delete_id = request.POST["id"]
    ds = Achievement.objects.get(id=delete_id)
    Achievement.delete(ds)
    return redirect('index')


@login_required
def add_achievement(request):
    if request.method == 'POST':
        stu = Student.objects.get(user_id=request.user.id)

        form = AchievementForm(request.POST)
        cd = form.data
        # save the material and achievement
        achi = Achievement.objects.create(name=cd['name'], category=cd['category'], 
                                          score=cd['score'], student=stu)
        achi.save()
        material = Material.objects.create(evidence=cd['evidence'], achievement=achi)
        material.save()
        return redirect('/index')


@staff_login_required
def generate_report(request):
    stus = Student.objects.all()
    report = {}
    for stu in stus:
        report[stu.user.id] = {}
        for cate in all_cate:
            cate = cate[0]
            achis = stu.achievement_set.filter(category=cate)
            score_sum = 0
            for achi in achis:
                score_sum += achi.score
            report[stu.user.id][cate] = score_sum
    return render(request, 'scholarsys/report.html', locals())
