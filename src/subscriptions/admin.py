from django.contrib import admin
from .models import Companies, Service, Plan, Subscription, Client, User, Profile, AutomationsClients, UsersPlans, Invites, PagarmePlans, PagarmeSubscriptions
from django.contrib.auth.admin import UserAdmin as BaseAdmin
from .forms import UserCreationForm, PasswordResetForm


class SubscriptionInline(admin.TabularInline):
    model = Subscription


class ClientAdmin(admin.ModelAdmin):
    model = Client
    inlines = [
        SubscriptionInline,
    ]

    list_display = [
        'id',
        'name',
        'get_users_count',
        'get_subscription_plan',
        'get_subscription_begin',
        'get_subscription_end',
        'get_subscription_value',
        'is_subscription_active',
        'get_company_name'
    ]

    list_filter = (
        'subscription__plan',
        'subscription__value',
        'subscription__active',
    )

    def get_users_count(self, instance):
        users = User.objects.filter(profile__client=instance)
        return users.count()
    get_users_count.short_description = "Users"

    def get_subscription_plan(self, instance):
        return instance.subscription.plan
    get_subscription_plan.short_description = "Plan"

    def get_subscription_begin(self, instance):
        return instance.subscription.begin
    get_subscription_begin.short_description = "Begin"

    def get_subscription_end(self, instance):
        return instance.subscription.end
    get_subscription_end.short_description = "End"

    def get_subscription_value(self, instance):
        return instance.subscription.value
    get_subscription_value.short_description = "Value"

    def is_subscription_active(self, instance):
        return instance.subscription.active
    is_subscription_active.short_description = "Active"
    is_subscription_active.boolean = True

    def get_company_name(self, instance):
        if instance.get_company():
            return instance.get_company().get_razao_social()
        else:
            return 'Não Fornecido'
    get_company_name.short_description = 'Company'


class ProfileInline(admin.TabularInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class UserAdmin(BaseAdmin):
    add_form = UserCreationForm
    add_fieldsets = (
        (
            None, {
                'description': ("Enter the new user's name and email address and click save."
                                " The user will be emailed a link allowing them to login to"
                                " the site and set their password."),
                'fields': ('email', 'first_name', 'last_name', 'client'),
            }),
        (
            'Password', {
                'description': "Optionally, you may set the user's password here",
                'fields': ('password1', 'password2'),
            }
        ),
    )

    def save_model(self, request, obj, form, change):
        if not change and (not form.cleaned_data['password1'] or not form.cleaned_data['password2']):
            obj.set_unusable_password()
            welcome_email = True
        else:
            welcome_email = False

        super(UserAdmin, self).save_model(request, obj, form, change)

        if welcome_email:
            reset_form = PasswordResetForm({'email': obj.email})
            assert reset_form.is_valid()
            reset_form.save(
                request=request,
                use_https=request.is_secure(),
                subject_template_name='registration/welcome_email_subject.txt',
                html_email_template_name='registration/welcome_email.html'
            )

    readonly_fields = ('username',)
    inlines = [ProfileInline]
    list_display = ('email', 'first_name', 'last_name', 'get_role',
                    'get_client_name', 'is_staff', 'is_superuser', 'is_active')
    list_filter = ['profile__client', 'profile__role',
                   'is_active', 'is_staff', 'is_superuser']

    def get_role(self, instance):
        USER_ROLES = (
            (1, 'Service Account'),
            (2, 'Client'),
            (3, 'Admin'),
            (4, 'Main'),
            (5, 'Editor Account'),
            (6, 'View Account'),
        )
        return USER_ROLES[instance.profile.role - 1][1]
    get_role.short_description = 'Role'

    def get_client_name(self, instance):
        return instance.profile.client

    get_client_name.short_description = "Client"

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj=obj)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'client', 'language',
                    'department', 'role', 'phone', 'email_confirmed']


class PlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'value',  'get_clients_count', 'qnt_automations',
                    'qnt_queries', 'qnt_extra_queries', 'extra_price']

    def get_clients_count(self, instance):
        subscriptions = Subscription.objects.filter(plan=instance)
        return subscriptions.count()
    get_clients_count.short_description = "Clients with this plan"


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['client', 'plan', 'value', 'active', 'with_dashboard', 'trial_period',
                    'number_of_hired_services', 'payment_period', 'queries_limit', 'extra_queries', 'status', 'begin', 'end']


class AutomationsClientsAdmin(admin.ModelAdmin):
    def get_can_create_model(self, instance):
        CREATE_MODEL_STATES = (
            (1, 'LIBERADO'),
            (2, 'AGUARDANDO'),
            (3, 'NÃO-LIBERADO'),
        )
        return CREATE_MODEL_STATES[instance.AutomationsClients.can_create_model - 1][1]
    get_can_create_model.short_description = 'can_create_model'

    list_display = ['client', 'automation',
                    'qnt_automations', 'created_at', 'can_create_model']


class UsersPlansAdmin(admin.ModelAdmin):
    list_display = ['user', 'client', 'automation', 'created_at']


class InvitesAdmin(admin.ModelAdmin):
    list_display = ['email', 'token', 'active', 'created_at']


class CompaniesAdmin(admin.ModelAdmin):
    list_display = ['get_razao_social',
                    'get_company_cnpj', 'number_of_clients']

    def get_razao_social(self, instance):
        return instance.get_razao_social().title()
    get_razao_social.short_description = 'Razão Social'

    def get_company_cnpj(self, instance):
        return instance.get_formatted_cnpj()
    get_company_cnpj.short_description = "CNPJ"

    def number_of_clients(self, instance):
        return Client.objects.filter(company=instance).count()

    number_of_clients.short_description = 'Número de Equipes'


class PagarmePlansAdmin(admin.ModelAdmin):
    list_display = ['plan_pagarme_id', 'amount',
                    'plan_pagarme_name', 'is_test', 'created_at']


class PagarmeSubscriptionsAdmin(admin.ModelAdmin):
    list_display = ['client', 'subscription_pagarme_id', 'plan_pagarme_id',
                    'is_test', 'created_at', 'payment_type', 'current_period_start', 'current_period_end']


admin.site.register([Service])
admin.site.register(Client, ClientAdmin)

admin.site.register(User, UserAdmin)
admin.site.register(Plan, PlanAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(AutomationsClients, AutomationsClientsAdmin)
admin.site.register(UsersPlans, UsersPlansAdmin)
admin.site.register(Invites, InvitesAdmin)
admin.site.register(Companies, CompaniesAdmin)
admin.site.register(PagarmePlans, PagarmePlansAdmin)
admin.site.register(PagarmeSubscriptions, PagarmeSubscriptionsAdmin)
