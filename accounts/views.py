from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.models import User as UserModel
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from . import forms
from .models import(
    Relation as RelationModel,
    Profile as ProfileModel,
)
from utils.base_alerts import BaseAlert


class UserRegistrationView(View):
    form_class = forms.UserRegistrationForm
    template_name = 'accounts/register_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('media:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        context = {'form': form}
        return render(
            request,
            self.template_name,
            context=context
        )

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            UserModel.objects.create_user(
                username=form_data['username'],
                email=form_data['email'],
                password=form_data['password'],
            )
            messages.success(
                request,
                message=BaseAlert.success_registration,
                extra_tags='success',
            )
            return redirect('media:home')

        return render(
            request,
            self.template_name,
            {'form': form}
        )


class UserLoginView(View):
    form_class = forms.UserLoginForm
    template_name = 'accounts/login_form.html'

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next', None)
        return super().setup(
            request,
            *args,
            **kwargs,
        )

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('media:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(
            request,
            self.template_name,
            {'form': form}
        )

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            forms_data = form.cleaned_data
            user = authenticate(
                request,
                username=forms_data['username'],
                password=forms_data['password'],
            )
            if user:
                login(request, user)
                messages.success(
                    request,
                    message=BaseAlert.logged_in,
                    extra_tags='success',
                )
                if self.next:
                    return redirect(self.next)
                return redirect('media:home')

            messages.error(
                request,
                BaseAlert.wrong_username_password,
                'warning'
            )
        return render(
            request,
            self.template_name,
            {'form': form}
        )


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(
            request,
            BaseAlert.logged_out,
            'success'
        )
        return redirect('media:home')


class UserProfileView(LoginRequiredMixin, View):
    profile_template = 'accounts/user_profile.html'

    def get(self, request, user_id):
        is_following = False
        user = get_object_or_404(
            UserModel,
            pk=user_id
        )
        posts = user.posts.all()
        relation = RelationModel.objects.filter(
            from_user=request.user,
            to_user=user_id,
        )
        if relation.exists():
            is_following = True

        return render(
            request,
            self.profile_template,
            {
                'user': user,
                'posts': posts,
                'is_following': is_following,
            },
        )


class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    email_template_name = 'accounts/password_reset_email.html'


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'


class UserFollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(
            UserModel,
            pk=user_id
        )
        is_relation = RelationModel.objects.filter(
            from_user=request.user,
            to_user=user,
        )
        if is_relation.exists():
            messages.error(
                request,
                BaseAlert.already_follow,
                'danger',
            )
        else:
            RelationModel.objects.create(
                from_user=request.user,
                to_user=user,
            )
            messages.success(
                request,
                BaseAlert.success_follow,
                'success',
            )
        return redirect(
            'accounts:user_profile',
            user.id
        )


class UserUnFollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(
            UserModel,
            pk=user_id,
        )
        is_relation = RelationModel.objects.filter(
            from_user=request.user,
            to_user=user,
        )
        if is_relation.exists():
            is_relation.delete()
            messages.success(
                request,
                BaseAlert.success_delete_relation,
                'success',
            )
        else:
            messages.error(
                request,
                BaseAlert.wrong_delete_relation,
                'danger',
            )

        return redirect(
            'accounts:user_profile',
            user.id
        )


class UserProfileEdit(LoginRequiredMixin, View):
    form_class = forms.UserProfileEditForm
    template_name = 'accounts/profile_edit.html'

    def setup(self, request, *args, **kwargs):
        self.profile = request.user.profile
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        user_id = kwargs['user_id']
        if request.user.id != user_id:
            return redirect(
                'accounts:user_login'
            )
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(
            instance=request.user,
            initial={
                'age': self.profile.age,
                'bio': self.profile.bio,
                'address': self.profile.address,
            }
        )
        return render(
            request,
            self.template_name,
            {
                'form': form,
            }
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            self.profile.age = form.cleaned_data.get('age')
            self.profile.bio = form.cleaned_data.get('bio')
            self.profile.address = form.cleaned_data.get('address')
            self.profile.save()
            messages.success(
                request,
                BaseAlert.success_edite_profile,
                'success',
            )
            return redirect(
                'accounts:user_profile',
                request.user.id
            )

        return render(
            request,
            self.template_name,
            {'form': form}
        )
