from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.views import LoginView
# from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse

from django.http import HttpResponse, JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from .forms import CustomAuthenticationForm, ProfileForm, SignupForm, UserAddressForm
from .tokens import account_activation_token
from .models import User, UserAddress, UserWishList
from product.models import Product

# Create your views here.


# def register(request):
# 	User = get_user_model()

# 	form_class = RegisterForm(request.POST or None)

# 	if form_class.is_valid():
# 		username = form_class.cleaned_data.get('username')
# 		email = form_class.cleaned_data.get('email')
# 		password = form_class.cleaned_data.get('password1')
# 		print(form_class.cleaned_data)
# 		user = User.objects.create_user(username=username,email=email,password=password)

# 	context = {
# 		'form' : form_class,
# 	}

# 	return render(request, 'users/register.html',context)

# ===========================================================================================

class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    redirect_authenticated_user = True
    # def get_success_url(self):
    #     user = self.request.user
    #     if user.is_authenticated:
    #         return reverse('product:home')
    #     else:
    #         return reverse('login')


# def navbar_login(request, *args, **kwargs):
#     form_class = AuthenticationForm(request, request.POST or None)

#     if form_class.is_valid():
#         print(form_class.cleaned_data)
#         username = form_class.cleaned_data.get('username')
#         password = form_class.cleaned_data.get('password')
#         user = authenticate(request, username=username, password=password)

#         if not user is None:
#             login(request, user)
#             form_class = AuthenticationForm()

#     context = {
#         'form': form_class,
#     }

#     return render(request, 'product/navbar.html', context)


class Profile(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    template_name = 'account/profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)

    def get_form_kwargs(self):
        kwargs = super(Profile, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


def signup(request):
    if request.user.is_authenticated:
        return redirect('product:home')
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)
        # return redirect('home')
        return HttpResponse('<p>Thank you for your email confirmation. Now you can login your account.</p>\n<p><a href="/login">login</a></p>')
    else:
        return HttpResponse('Activation link is invalid!')


class AddressCreateView(LoginRequiredMixin, CreateView):
    model = UserAddress
    form_class = UserAddressForm
    template_name = "account/list_create_address.html"
    success_url = reverse_lazy('users:address')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        addresses = UserAddress.objects.filter(user=self.request.user)
        context['addresses'] = addresses
        return context


class AddressUpdateView(LoginRequiredMixin, UpdateView):
    model = UserAddress
    fields = ("city", "address", "post_code", )
    template_name = 'account/update_address.html'
    success_url = reverse_lazy('users:address')


class AddressDeleteView(LoginRequiredMixin, DeleteView):
    model = UserAddress
    success_url = reverse_lazy('users:address')


class UserWishListView(LoginRequiredMixin, ListView):
    model = UserWishList
    template_name = 'account/wishlist.html'

    def get_queryset(self):
        try:
            wish_list = UserWishList.objects.get(user=self.request.user)
        except:
            wish_list = UserWishList.objects.create(user=self.request.user)

        products = wish_list.items.all()

        return products


@csrf_exempt
def add_item_wishlist(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            wish_list = UserWishList.objects.get(user=request.user)
            if (wish_list.contains(request.POST.get("product_id"))):
                return JsonResponse({'success': False, 'error': 'محصول در لیست علاقه مندی وجود دارد.'})

            product = Product.objects.get(pk=request.POST.get("product_id"))
            wish_list.items.add(product)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'وارد حساب کاربری خود نشده اید.'})
    else:
        return JsonResponse({'success': False, 'error': 'درخواست اشتباه است.'})


@csrf_exempt
def remove_item_wishlist(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            wish_list = UserWishList.objects.get(user=request.user)
            product = Product.objects.get(pk=request.POST.get("product_id"))
            wish_list.items.remove(product)
            return JsonResponse({'success': True})
