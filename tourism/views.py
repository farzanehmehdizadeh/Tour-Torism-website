from .forms import tourism, tourismform
from django.shortcuts import render, redirect, get_object_or_404
from .models import tourism
from django.contrib.auth.decorators import login_required
# from .forms import SearchForm
from .forms import TourismSearchForm
from django.http import HttpResponseForbidden
from django.contrib import messages
from .models import tourism, Purchase,Profile


list = []
form = tourismform()

#
# @login_required(login_url='/accounts/login')
# def tourism_create(request):
#     user = request.user
#     list = []
#
#     if request.method == 'POST':
#         form = tourismform(request.POST, request.FILES)  # necessary if user wants to upload a picture
#         if form.is_valid():
#             instance = form.save(commit=False)  # lets us make some changes on the form before saving it on database
#             instance.clas = user  # Associate the tour with the logged-in user
#             instance.pic = request.FILES.get('image', False)  # Get the uploaded image
#
#             # Check if the title already exists in the list
#             if instance.title in list:
#                 tourisms = tourism.objects.filter(title=instance.title)
#                 tourisms.delete()  # Delete existing tours with the same title
#             instance.save()  # Save the new tour
#             return redirect('tourism:tourismpage')  # Redirect to the tour list or add page
#
#     else:
#         form = tourismform()  # Create a new form instance if not a POST request
#
#     # Get the tours created by the logged-in user
#     query = tourism.objects.filter(clas=user)
#
#     for tourww in query:
#         list.append(tourww.title)
#
#     return render(request, 'tourism/addtourism_page.html', {'form': form, 'tourisms': query})
# این پایینی کد قبلی بود
# def tourism_create(request):
#     user = request.user
#     existing_titles = []  # Use a different name
#
#     if request.method == 'POST':
#         form = tourismform(request.POST, request.FILES)
#         if form.is_valid():
#             instance = form.save(commit=False)
#             instance.clas = user
#             instance.image = form.cleaned_data.get('image')  # Properly assign the image
#
#             # Check if the title already exists in the list
#             if instance.title in existing_titles:
#                 tourism.objects.filter(title=instance.title).delete()
#
#             instance.save()
#             return redirect('tourism:tourismpage')
#
#     else:
#         form = tourismform()
#
#     # Get the tours created by the logged-in user
#     query = tourism.objects.filter(clas=user)
#     for tour in query:
#         existing_titles.append(tour.title)
#
#     return render(request, 'tourism/addtourism_page.html', {'form': form, 'tourisms': query})
def user_is_authorized(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.email == 'bita4akhgar@gmail.com':
                print("User is authorized")
                return view_func(request, *args, **kwargs)
        print("User is not authorized")
        return HttpResponseForbidden("شما مجاز به انجام این عملیات نیستید!")
    return wrapper

@login_required
@user_is_authorized
def tourism_create(request):
    user = request.user
    tourism_titles = set(tourism.objects.values_list('title_tourism', flat=True))  # دریافت عناوین تور های موجود

    if request.method == 'POST':
        form = tourismform(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.clas = user  # افزودن کاربر به عنوان فیلد ForeignKey
            # استفاده از نام فیلد جدید
            if instance.title_tourism in tourism_titles:
                tours = tourism.objects.filter(title_tourism=instance.title_tourism)
                tours.delete()
            instance.save()
            return redirect('tourism:tourismpage')

    else:
        form = tourismform()

    user_tours = tourism.objects.filter(clas=user)

    is_authorized = (user.email == 'bita4akhgar@gmail.com')
    print("is_authorized:", is_authorized)  # پیام دیباگینگ

    return render(request, 'tourism/addtourism_page.html', {
        'form': form,
        'tours_list': user_tours,
        'is_authorized': is_authorized
    })
# def tourism_create(request):
#     user = request.user
#     tourism_titles = set()
#
#     if request.method == 'POST':
#         form = tourismform(request.POST, request.FILES)
#         if form.is_valid():
#             instance = form.save(commit=False)
#             instance.clas = user
#             # instance.image = form.cleaned_data['image']
#             if instance.title in tourism_titles:
#                 tours = tourism.objects.filter(title=instance.title)
#                 tours.delete()
#             instance.save()
#             return redirect('tourism:tourismpage')
#
#     else:
#         form = tourismform()
#
#     user_tours = tourism.objects.filter(clas=user)
#
#     is_authorized = (user.email == 'darya.yazdanpanah22@gmail.com')
#     print("is_authorized:", is_authorized)  # پیام دیباگینگ
#
#     return render(request, 'tourism/addtourism_page.html', {
#         'form': form,
#         'tours_list': user_tours,
#         'is_authorized': is_authorized
#     })

def tourism_view(request):

    tourisms = tourism.objects.all()  # نام مدل باید با حرف بزرگ باشد: Tour
    form = TourismSearchForm(request.GET)  # دریافت داده‌های فرم جستجو

    if form.is_valid():
        origin = form.cleaned_data.get('firstdistination_tourism')
        # destination = form.cleaned_data.get('lastDestination')
        # startdate = form.cleaned_data.get('startdate_persian')  # تاریخ رفت
        # finishdate = form.cleaned_data.get('finishdate')  # تاریخ برگشت



            # فیلتر کردن تورها بر اساس مبدا و مقصد
        if origin:
            tourisms = tourisms.filter(firstdistination_tourism__icontains=origin)
        # if destination:
        #     tourisms = tourisms.filter(lastDestination__icontains=destination)
        # if startdate:
        #     tourisms = tourisms.filter(startdate__gte=startdate)  # تاریخ شروع باید بزرگتر یا مساوی تاریخ انتخابی باشد
        # if finishdate:
        #     tourisms = tourisms.filter(finishdate__lte=finishdate)  # تاریخ برگشت باید کوچکتر یا مساوی تاریخ انتخابی باشد

    return render(request, 'tourism/tourism_page.html', {'tourisms': tourisms, 'form': form})



@login_required
def deletetourism(request, pk):
    # بررسی اینکه آیا کاربر مجاز است
    if request.user.email != 'bita4akhgar@gmail.com':
        return HttpResponseForbidden("شما مجاز به انجام این عمل نیستید.")

    # استفاده از get_object_or_404 برای یافتن تور با PK
    item = get_object_or_404(tourism, id=pk)

    # حذف تور
    item.delete()

    messages.success(request, "تور با موفقیت حذف شد.")
    return redirect('tourism:tourismpage')


# def edittourism(request, pk):
#     # بررسی اینکه آیا کاربر مجاز است
#     if request.user.email != 'bita4akhgar@gmail.com':
#         return HttpResponseForbidden("شما مجاز به انجام این عمل نیستید.")
#
#     try:
#         tour_id = get_object_or_404(tourism, id=pk)
#     except tourism.DoesNotExist:
#         messages.error(request, "تور مورد نظر پیدا نشد.")
#         return redirect('tourism:tourismpage')
#
#     form = tourismform(instance=tour_id)
#
#     if request.method == "POST":
#         form = tourismform(request.POST, instance=tour_id)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "تور با موفقیت به‌روزرسانی شد.")
#             return redirect('tourism:tourismpage')
#
#     return render(request, 'tourism/addtourism_page.html', {'form': form})

@login_required
def edittourism(request, pk):
    # بررسی اینکه آیا کاربر مجاز است
    if request.user.email != 'bita4akhgar@gmail.com':
        return HttpResponseForbidden("شما مجاز به انجام این عمل نیستید.")

    # دریافت شیء تور
    tour_id = get_object_or_404(tourism, id=pk)

    # بررسی نوع درخواست
    if request.method == "POST":
        form = tourismform(request.POST, instance=tour_id)  # بارگذاری اطلاعات فرم با instance
        if form.is_valid():
            form.save()  # ذخیره تغییرات
            messages.success(request, "تور با موفقیت به‌روزرسانی شد.")
            return redirect('tourism:tourismpage')  # انتقال به صفحه مربوطه
    else:
        form = tourismform(instance=tour_id)  # بارگذاری فرم با اطلاعات قبلی برای GET

    # نمایش فرم
    context = {
        'form': form,
        'tour_id': tour_id,  # ارسال شیء تور برای نمایش در template
    }
    return render(request, 'tourism/addtourism_page.html', context)

def tourism_detail(request, tourism_id):
    # دریافت تور با id مشخص شده یا 404 در صورتی که تور پیدا نشود
    tourisms = get_object_or_404(tourism, id=tourism_id)
    return render(request, 'tourism/tourism_detail.html', {'tour': tourisms})

def main_page(request):
    tourisms = tourism.objects.all()
    context = {
        'tourisms': tourisms
    }

    return render(request, 'tour/main_page.html', context)

# def main_page(request):
#     tours = tour.objects.all()  # تمام تورها را از پایگاه‌داده بگیرید
#     context = {
#         'tours': tours  # ارسال تورها به قالب
#     }
#     return render(request, 'tour/main_page.html', context)  # از context استفاده کنید


def buy_tourism(request, tourism_id):
    # ابتدا بررسی می‌کنیم که کاربر احراز هویت شده است
    if not request.user.is_authenticated:
        messages.error(request, "لطفاً ابتدا وارد حساب کاربری خود شوید.")
        return redirect('accounts:login')  # یا صفحه‌ای که می‌خواهید کاربر را به آن هدایت کنید

    # حالا می‌خواهیم تور منتخب را پیدا کنیم
    try:
        tour_to_buy = tourism.objects.get(id=tourism_id)  # اطمینان از نام مدل
    except tourism.DoesNotExist:
        messages.error(request, "تور مورد نظر یافت نشد.")
        return redirect('tourism:profile_view')  # یا به هر صفحه دلخواه

    # بررسی می‌کنیم که آیا ظرفیت بیشتر از صفر است
    if tour_to_buy.capacity_tourism <= 0:  # به‌روزرسانی نام فیلد ظرفیت
        messages.error(request, "متأسفانه این تور پر شده است.")
        return redirect('tourism:profile_view')

    # خرید ثبت می‌شود
    Purchase.objects.create(user=request.user, tour=tour_to_buy)

    # کاهش ظرفیت تور
    tour_to_buy.capacity_tourism -= 1  # به‌روزرسانی نام فیلد ظرفیت
    tour_to_buy.save()  # ذخیره تغییرات ظرفیت در پایگاه داده

    # ارسال پیام تأیید به کاربر
    messages.success(request, f"{tour_to_buy.title_tourism} به درستی خریداری شد.")

    return redirect('tourism:profile_view')  # به صفحه‌ای که می‌خواهید کاربر را به آن هدایت کنید


@login_required(login_url='accounts/signup/')
def profile_view(request):
    user = request.user
    # دریافت لیست تورهای کاربر از پروفایل
    profile, created = Profile.objects.get_or_create(user=user)
    tours = profile.tours.all()
    purchases = Purchase.objects.filter(user=user)  # خریدهای کاربر
    available_tours = tourism.objects.all()  # لیست تورهای موجود

    return render(request, 'tourism/profile_view.html', {
        'user': user,
        'purchases': purchases,
        'available_tours': available_tours,  # ارسال لیست تورهای موجود به قالب
        'tours': tours  # ارسال لیست تورهای کاربر به قالب
    })
