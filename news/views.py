from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from .models import News
from .forms import NewsForm
from django.shortcuts import render


@login_required
def news_list(request):
    news_items = News.objects.all()
    return render(request, 'news/news_list.html', {'news_items': news_items})


def user_is_authorized(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.email == 'bita4akhgar@gmail.com':
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("شما مجاز به انجام این عملیات نیستید!")

    return wrapper


@login_required
@user_is_authorized
def news_create(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news_instance = form.save(commit=False)
            news_instance.owner = request.user  # ارتباط خبر با کاربر
            news_instance.save()
            messages.success(request, "خبر با موفقیت اضافه شد.")
            return redirect('news:news_list')  # یا هر URL مربوط به لیست اخبار
    else:
        form = NewsForm()

    return render(request, 'news/add_news.html', {'form': form})



@login_required
@user_is_authorized  # اطمینان از این‌که کاربر مجاز به ویرایش است
def edit_news(request, pk):
    # تلاش برای دریافت شیء خبر از پایگاه داده
    news_item = get_object_or_404(News, id=pk)

    if request.method == "POST":
        form = NewsForm(request.POST, request.FILES, instance=news_item)  # بارگذاری فایل‌ها
        if form.is_valid():
            form.save()
            messages.success(request, "خبر با موفقیت به‌روزرسانی شد.")
            return redirect('news:news_list')  # یا هر URL مربوط به لیست اخبار
    else:
        form = NewsForm(instance=news_item)  # فرم با اطلاعات قبلی پر می‌شود

    # بررسی مجوز کاربر
    is_authorized = (request.user.email == 'bita4akhgar@gmail.com')
    context = {
        'form': form,
        'is_authorized': is_authorized,
        'news_item': news_item  # می‌توانید شیء خبر را به context اضافه کنید
    }

    return render(request, 'news/add_news.html', context)  # نمایش فرم ویرایش
@login_required
@user_is_authorized
def delete_news(request, pk):
    news_item = get_object_or_404(News, id=pk)  # استفاده از get_object_or_404 برای یافتن خبر با PK

    if request.method == "POST":
        news_item.delete()
        messages.success(request, "خبر با موفقیت حذف شد.")
        return redirect('news:news_list')  # یا هر URL مربوط به لیست اخبار


# ----------------------------------------------#


