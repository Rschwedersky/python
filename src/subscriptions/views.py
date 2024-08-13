from uuid import uuid4
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm
from django.db.models.query_utils import Q
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import reverse
from django.db.utils import IntegrityError
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.utils.translation import get_language
from my_solutions.templatetags.mysolutions_tags import sort_dict_by_key
from portal.functions import get_ip_address
from rest_framework import status
from smt_orchestrator.models import Automation, Schedule, Task
from subscriptions.templatetags.pagarme_tags import getPagarmePlan, setPagarmeSubscription, updatePagarmeSubscription, getPagarmeSecretKey, getPagarmeTest, getPagarmeAPIKey, cancelPagarmeSubscription, getSubscriptionPeriodFromJson
from .forms import UserCreationForm
from django.core.validators import validate_email
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from django.views.decorators.http import require_http_methods
from rest_framework.decorators import permission_classes, authentication_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt
from .models import Invites, PagarmeSubscriptions, SessionInfo, User, Subscription, Plan, Profile, Client, AutomationsClients, UsersPlans
from portal.functions import get_client_from_request
from portal.templatetags.general_tags import check_if_automation_name_is_in_query, translate, get_automation_display_name
from dashboard.templatetags.dashboard_tags import getLanguage, get_automation_by_name, isClientMainUser, get_name_initials, get_people_to_send_email
from .templatetags.subscriptions_tags import check_email_domain, create_new_client_subscription, delete_schedules_from_user, erase_schedule_in_s3_and_database, get_users_from_client, getHubUrl, getUserPlan, sendEmail, get_plan_info, set_company_info_with_cnpj, get_client_services_and_utilizations, is_plan_upgrade

from .tokens import account_activation_token

from datetime import datetime, timezone, timedelta, time
import pytz
import jwt
import json

import binascii
import hmac
import re
from hashlib import sha1


def help_center(request):
    language = getLanguage(request)
    tituloslogos = [
        {'titulo': 'Introdução', 'logo': 'introducao', 'href': '#introdução'},
        {'titulo': 'Dashboard de RPA', 'logo': 'dashboard_rpa', 'href': '#dashboardrpa'},
        {'titulo': 'Serviços', 'logo': 'servicos', 'href': '#serviços'},
        {'titulo': 'Licenças', 'logo': 'permissoes', 'href': '#licenças'},
        {'titulo': 'Segurança e LGPD', 'logo': 'secure', 'href': '#segurançalgpd'},
        {'titulo': 'Resultados', 'logo': 'resultado', 'href': '#resultados'}
    ]

    help_center = [
        {
            'title': 'Introdução',
            'sections': [
                {
                    'title': 'Sobre o Smarthis Hub',
                    'items':
                    [
                        {'title': 'O que é o Smarthis Hub?',
                         'text': 'O Smarthis Hub é uma plataforma por assinatura que concentra serviços de Automação de Processos, Inteligência Artificial e Analytics. É um SaaS (Software as a Service), ou seja, a manutenção e a atualização estão sob responsabilidade da Smarthis. Dessa forma, você não precisa se preocupar com essas etapas, apenas aproveitar em utilizar a nossa plataforma.'},
                        {'title': 'Quais são os serviços oferecidos no Smarthis Hub?',
                         'text': 'Você pode conferir a nossa lista completa de serviços na página <a href="discover" target="_blank">Descobrir</a>. Nosso catálogo está em constante expansão e você também pode sugerir serviços.'},
                    ]
                },
                {
                    'title': 'Dispositivos e navegadores',
                    'items': [
                        {'title': 'Preciso instalar alguma aplicação no meu computador?', 'text': 'Não, de forma geral nossos serviços são plug and play. Isso significa que você pode acessar a plataforma do Smarthis Hub e todos os seus serviços pelo seu navegador do seu computador. Para melhores resultados, recomendamos o uso das versões mais atualizadas do Google Chrome ou Mozilla Firefox. Alguns serviços mais específicos, como o Dashboard de RPA podem depender de integração com outras plataformas. Nesse caso, entraremos em contato fornecendo os detalhes necessários.'},
                        {'title': 'Posso acessar de qualquer dispositivo?',
                         'text': 'Por enquanto o Smarthis Hub está disponível apenas para Desktops, Notebooks e Laptops. Assim que for possível acessar de outros dispositivos, você será notificado.'},
                    ]
                },
            ]
        },
        {
            'title': 'Dashboard RPA',
            'sections': [
                {
                    'title': 'Contratação e integração',
                    'items': [
                        {'title': 'O Dashboard de RPA funciona com qualquer serviço de RPA?',
                         'text': 'Não, por enquanto o Dashboard de RPA possui integração apenas com serviços UiPath.'},
                    ]
                },
                {
                    'title': 'Dados',
                    'items': [
                        {'title': 'De onde vêm os dados?',
                         'text': 'Os dados dos seus processos vêm diretamente do orquestrador UiPath.'},
                        {'title': 'Preciso cadastrar um processo novo?', 'text': 'Não. As informações dos seus processos irão aparecer automaticamente após serem identificados no orquestrador UiPath.Depois disso, pode ser necessário fornecer mais informações como área de atuação, tempo de execução etc..'},
                        {'title': 'Quem pode visualizar o Dashboard de RPA?',
                         'text': 'O dashboard RPA poderá ser visualizado pelo administrador e pessoas convidadas para o Dashboard. '},
                    ]
                },
                {
                    'title': 'Visualização e filtros',
                    'items': [
                        {'title': 'Quais análises o Dashboad RPA disponibiliza?', 'text': 'Você poderá visualizar gráficos detalhados sobre a execução de processos pelo UI Path, como a ocupação média por hora do seu robô, número de processos executados em um determinado período, a taxa de ocupação de cada robô, o retorno financeiro e por hora de cada processo e muito mais.'},
                        {'title': 'Consigo visualizar os tipos de erro ocorridos?',
                         'text': 'Ainda não é possível especificar os tipos de erros ocorridos, essa informação depende do que está disponível no orquestrador.'},
                        {'title': 'Posso visualizar dados de um robô específico?',
                         'text': 'Sim. O Dashboard de RPA conta com vários tipos de filtro para te ajudar a visualizar diferentes tipos de informação, incluindo o filtro para os robôs.'},
                        {'title': 'Como visualizo apenas informações de uma área?',
                         'text': 'Utilizando o filtro no menu lateral do Dashboard de RPA, você pode indicar qual área deseja visualizar as informações e muito mais.'}

                    ]
                },
            ]
        },
        {
            'title': 'Serviços',
            'sections': [

                {
                    'title': 'Utilizando serviços',
                    'items': [
                        {'title': 'Como utilizo um serviço?', 'text': 'Na página <a class="text_decoration" href="services" target="_blank">Serviços → Meus Serviços</a> você encontrará todos os serviços atribuídos a você. Acesse o serviço desejado e configure um Modelo de acordo com as instruções da página. Você poderá utilizar esse modelo sempre que desejar clicando em Iniciar.'},
                        {'title': 'Por que preciso informar minhas credenciais?',
                         'text': 'Para te entregar os resultados, alguns serviços do Smarthis Hub precisam acessar os sites e fazer login, assim como se você estivesse fazendo este processo manualmente, mas muito mais rápido! Mas não se preocupe, seus dados estão seguros.'},
                        {'title': 'Posso executar serviços simultaneamente?',
                         'text': 'Sim, serviços podem ser executados de forma simultânea.'},
                        {'title': 'Posso executar modelos de um serviços simultaneamente?',
                         'text': 'Sim. Com 01 (uma) licença você pode criar quantos modelos desejar, mas para executar o processo de mais de um modelo ao mesmo tempo você precisa ter 02 (duas) ou mais licenças.'},
                        {'title': 'Contratei um serviço pela plataforma e ele ainda não está disponível',
                         'text': f'Os serviços contratados ou trocados serão disponibilizados no prazo de até 24h (em dias úteis). Caso o serviço ainda não esteja disponível após o prazo, entre em contato pelo e-mail {translate("hub_contact_email", language)}'},
                        {'title': 'A execução de um serviço deu erro.', 'text': 'Veja o que pode ter acontecido: <strong class="light-bold">Arquivo -</strong> <strong class="text_margin--help-center">O arquivo .csv/.xlsx fornecido para este modelo não coincide com o padrão necessários para sua execução. Atualize o modelo e tente novamente.</strong><strong class="light-bold"> Credenciais -</strong> <strong>Não foi possível acessar o site deste serviço por que as credenciais fornecidas neste modelo estão desatualizas. Verifique suas credenciais e tente novamente.O website necessário para executar este serviço está fora do ar no momento. Por favor aguarde antes de tentar novamente.</strong>'},
                        {'title': 'Posso usar o mesmo arquivo de upload para serviços diferentes?',
                         'text': 'Não. Cada serviço funciona com um arquivo de upload próprio que deve ser preenchido com campos específicos. '},
                    ]
                },
            ]
        },
        {
            'title': 'Resultados',
            'sections': [
                {'title': '',
                 'items':
                 [
                     {'title': 'Não recebi resultado de um serviço.', 'text': 'Verifique seu e-mail e caixa de SPAM, por padrão enviamos para a conta cadastrada no Smarthis Hub, mas você pode adicionar outros contas como destinatários. Se mesmo assim não receber o e-mail com os resultados, certifique-se que indicou os e-mails corretamente no seu modelo, ou verifique se o seu serviço ainda está em execução.'},
                     {'title': 'Não consigo mais fazer download do resultado, o que aconteceu?',
                      'text': 'Ao finalizar uma execução, enviaremos um e-mail com resultados e link para download. Este link ficará disponível por até X dias. Após, ele expirará. Mas você pode executar o modelo quantas vezes quiser, sem cobrança extra.'},
                     {'title': 'Uma pessoa precisa ter licença de um serviço para receber os resultados?',
                      'text': 'Não, ao configurar modelo você pode adicionar outros destinatários, assim eles também receberão os resultados por e-mail.'},
                     {'title': 'Posso enviar os resultados para mais de uma pessoa?',
                      'text': 'Sim, ao configurar modelo você pode adicionar outros destinatários, assim eles também receberão os resultados por e-mail.'},
                     {'title': 'Em quais formatos posso receber os resultados?',
                      'text': 'O resumo dos resultados pode ser disponibilizado nos formatos .xlsx (excel) ou .csv. Caso o seu serviço gere outros resultados como boletos ou certidões, eles serão disponibilizados no formato PDF.'},
                 ]
                 },
            ]
        },
        {'title': 'Licenças',
            'sections': [
                {'title': '',
                 'items':
                 [
                  {'title': 'O que é uma licença?', 'text': 'Uma licença é como um acesso ou tíquete para um serviço. Para utilizar um serviço, o colaborador ou administrador precisa ter pelo menos uma licença para aquele serviço. Cada licença é única e só pode ser atribuída a uma pessoa. Com ela, é possível configurar e salvar modelos e reutilizá-los sempre que precisar, de forma ilimitada.'},
                  {'title': 'Por que ter mais de uma licença para o mesmo serviço?',
                      'text': 'Caso a demanda por um serviço seja mais alta na sua empresa e você precise que mais de um colaborador a utilize ou que mais de um processo seja executado ao mesmo tempo, é necessário ter mais licenças para esse serviço.'},
                 ]
                 },
            ]
         },
        {
            'title': 'Segurança LGPD',
            'sections': [
                {'title': '',
                 'items':
                 [
                     {'title': 'Meus dados estão seguros?', 'text': 'Seguimos a LGPD, temos criptografia. Você pode saber mais detalhes na nossa  <strong class="text_decoration"><a  href="static\instructions\Política_de_Privacidade.pdf" target="_blank">Política de Privacidade</a></strong> e  <strong class="text_decoration"><a  href="static\instructions\Termos_de_uso.pdf" target="_blank">Termos de uso</a></strong>.'},
                     {'title': 'Quais dados meus e da minha empresa estão sendo coletados?', 'text': 'Coletamos os dados que são fornecidos com seu conhecimento ao se cadastrar na plataforma. Também coletamos dados de navegação via cookies para pode continuar melhorando a sua experiência de uso. Você pode saber mais detalhes na nossa <strong class="text_decoration"><a href="static\instructions\Política_de_Privacidade.pdf" target="_blank">Política de Privacidade</a></strong> e <strong class="text_decoration"><a  href="static\instructions\Termos_de_uso.pdf" target="_blank">Termos de uso</a></strong>.'},
                     {'title': 'Quem tem acesso a esses dados?',
                      'text': 'Todos os dados obtidos são de uso único e exclusivo interno do Smarthis Hub.'},
                 ]
                 },
            ]
        },
    ]

    if isClientMainUser(request.user):
        adminservicetext = {
            'title': 'Contratei um serviço, mas ele não aparece para mim. ', 'text': f'Os serviços podem levar até 24h (em dias úteis) para serem atualizados após troca ou nova contratação. Em caso de upgrade de assinatura ou atraso de pagamento, esse prazo passa a contar a partir da compensação do boleto. Se depois deste prazo você ainda não estiver visualizando o serviço, entre em contato conosco pelo e-mail {translate("hub_contact_email", language)}.'

        }
        help_center[2]['sections'][0]['items'].insert(1, adminservicetext)
        adminservicetext = {
            'title': 'Desejo utilizar somente um serviço, como devo proceder? ', 'text': 'Você pode contratar o nosso Plano User para ter acesso à 1 licença. Assim, você poderá utilizar um serviço, ou transferir essa licença para um colaborador da sua equipe. Visite <strong class="text_decoration c-pointer"  data-toggle="modal" data-target="#modalsettings" id="dropdown-config-button">Configurações → Plano</strong> para saber mais.'

        }
        help_center[2]['sections'][0]['items'].insert(6, adminservicetext)

        adminservicetext = {
            'title': 'Posso transferir licenças do meu plano para outros usuários? ', 'text': 'Sim. Para transferir licenças para seus colaboradores ou retorná-las ao Administrador vá até <strong class="text_decoration"><a  href="services" target="_blank">Serviços</a> → Gerenciar licenças</strong>. Lá você terá acesso à todos serviços contratados e consegue transferir suas licenças para os colaboradores dentro do serviço designado.'

        }
        help_center[4]['sections'][0]['items'].insert(2, adminservicetext)

        adminservicetext = {
            'title': 'Atribuí uma licença a pessoa errada, o que faço? ', 'text': 'Para gerenciar suas licenças, vá até <strong class="text_decoration"><a  href="services" target="_blank">Serviços → Gerenciar licenças</a></strong>, encontre o serviço desejado, retire as licenças do colaborador que recebeu por engano, e compartilhe a licença com o colaborador correto.'

        }
        help_center[4]['sections'][0]['items'].insert(3, adminservicetext)

        adminservicetext = {
            'title': 'Como retirar a licença de alguém? ', 'text': 'Para gerenciar suas licenças, vá até <strong class="text_decoration"><a  href="services" target="_blank">Serviços → Gerenciar licenças</a></strong> encontre o serviço desejado e retire as licenças do colaborador.'

        }
        help_center[4]['sections'][0]['items'].insert(4, adminservicetext)

        adminservicetext = {
            'title': 'Pagamento ',
            'sections': [
                {'title': '',
                 'items':
                 [
                     {'title': 'Quais formas de pagamento são aceitas?', 'text': 'É possível pagar pela sua assinatura no Smarthis Hub com cartão de crédito ou por boleto. Você fornece as informações no momento da contratação do seu plano e logo depois recebe um e-mail informando se o pagamento foi processado. No caso de pagamento por boleto, este e-mail pode demorar até 24h.<p class="text--content-help m-0 w-100">Todos os pagamentos realizados no Smarthis Hub são processado pela <a class="text_decoration" href="https://pagar.me/" target="_blank">Pagar.me.</a></p>'},
                     {'title': 'É possível mudar o dia de vencimento da minha assinatura?',
                      'text': f'Sim, é possível. Por favor, envie um e-mail para {translate("hub_contact_email", language)} com a sua solicitação.'},
                     {'title': 'É possível mudar as minhas informações de pagamento?',
                      'text': f'Sim, é possível. Visite <strong class="text_decoration c-pointer" data-toggle="modal" data-target="#modalsettings" id="dropdown-config-button">Configurações → Plano</strong> e clique em <strong class="text_decoration">"Editar informações"</strong> para alterar as informações.'},
                     {'title': 'Não recebi e-mail sobre pagamento',
                      'text': f'O e-mail de confirmação de pagamento será enviado para o endereço fornecido no momento da contratação. Verifique a caixa de entrada e SPAM do e-mail indicado e então classifique o endereço do Smarthis Hub e da <a class="text_decoration" href="https://pagar.me/" target="_blank">Pagar.me.</a> como "Não é SPAM".<p class="text--content-help m-0 w-100">No caso de pagamento por boleto, este email pode demorar até 24h.</p><p class="text--content-help m-0 w-100">Se mesmo assim não tiver recebido o e-mail, entre com contato pelo formulário ao lado, ou pelo e-mail {translate("hub_contact_email", language)}</p>'},
                 ]
                 },
            ]
        }
        help_center.insert(6, adminservicetext)

        adminservice = {
            'title': 'Troca e gerenciamento de serviços',
            'items': [
                # SOMENTE ADMINISTRADOR
                {'title': 'Preciso de mais serviços, o que faço?',
                    'text': f'Você pode fazer upgrade para contratar mais licenças e ter acesso a mais serviços em <strong class="text_decoration c-pointer"  data-toggle="modal" data-target="#modalsettings" id="dropdown-config-button">Configurações → Plano</strong>. Ao tentar contratar um novo serviço na página <a href="discover" target="_blank">Descobrir</a>, a opção de upgrade também irá aparecer. Se preferir, você também pode entrar em contato com o suporte do Smarthis Hub pelo email {translate("hub_contact_email", language)}.'},
                {'title': 'Como permito que mais de uma pessoa utilize o mesmo serviço?',
                    'text': 'Contrate mais licenças para o mesmo serviço e transfira pelo menos uma delas a cada pessoa, de acordo com a necessidade da sua empresa.'},
                {'title': 'Contratei um serviço e me arrependi, posso trocar por outro?',
                    'text': 'Sim, ao selecionar o novo serviço que deseja adicionar ao seu plano será possível indicar que deseja fazer uma troca pelo serviço antigo. Visite a página <a href="discover" target="_blank">Descobrir</a> e conheça todos os serviços disponíveis.'},
                {'title': 'Quantas pessoas posso convidar pra plataforma?',
                    'text': 'O Smarthis HUB não limita a quantidade de colaboradores que podem ser convidados para a plataforma. Para utilizar os serviços, no entanto, é preciso ter licenças. Assim, o número de colaboradores utilizando os serviços dependerá do plano contratado.'},
            ]
        }
        help_center[2]['sections'].insert(0, adminservice)

        adminservice = {
            'titulo': 'Pagamento', 'logo': 'pagamento', 'href': '#pagamento'
        }
        tituloslogos.insert(5, adminservice)

        adminservicetext = {
            'title': 'Cancelamento ',
            'sections': [
                {'title': '',
                 'items':
                 [
                     {'title': 'Quero cancelar minha assinatura, o que faço?', 'text': 'Você pode cancelar a sua assinatura a qualquer momento em  <strong class="text_decoration c-pointer"  data-toggle="modal" data-target="#modalsettings" id="dropdown-config-button">Configurações → Plano</strong>. Sua conta continuará ativa e poderá utilizar seus serviços até o final do período de contratação atual.'},
                     {'title': 'Contratei o plano errado, posso cancelar/trocar?',
                      'text': f'Sim, é possível. Envie sua solicitação explicando o ocorrido para {translate("hub_contact_email", language)}.'},
                     {'title': 'Quanto tempo os modelos dos meus serviços ficam salvos depois que cancelei minha conta?',
                      'text': 'Depois do cancelamento da sua assinatura, os seus dados, e de colaboradores convidados e modelos configurados ficam salvos nos nossos servidores por até <strong class="light-bold">2 meses</strong>. Caso você queria voltar a utilizar o Hub dentro deste período, não terá perdido nenhuma informação.'},
                 ]
                 },
            ]
        }
        help_center.insert(7, adminservicetext)

    else:
        colaboradorservice = {
            # SOMENTE COLABORADOR
            'title': 'O serviço que preciso utilizar não aparece pra mim.', 'text': 'Solicite licença para este serviço ao seu Administrador.'
        }
        help_center[2]['sections'][0]['items'].insert(1, colaboradorservice)

        colaboradorservice = {
            # SOMENTE COLABORADOR
            'title': 'Posso transferir licenças do meu plano para outros usuários?', 'text': 'Não. A única pessoa que pode transferir licenças entre colaboradores é o Administrador do seu plano. Se necessário, solicite essa transferência ao seu Administrador.'
        }
        help_center[4]['sections'][0]['items'].insert(3, colaboradorservice)

    context = {
        'language': language,
        'tituloslogos': tituloslogos,
        'help_center': help_center
    }

    return render(request, "help_center.html", context)


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@require_http_methods(["POST"])
def faq_doubts(request):
    formAssunto = request.POST.get('formAssunto')
    formMensagem = request.POST.get('formMensagem')
    email_context = {'language': 'pt-BR', 'formAssunto': formAssunto, 'formMensagem': formMensagem,
                     'user': request.user}
    sendEmail('faqDoubts', 'Central de Ajuda' + ' Smarthis Hub',
              ['guilherme.favoreto@smarthis.com.br', 'luiz.pinho@smarthis.com.br'], email_context)
    return JsonResponse({'status': 200, 'assunto': formAssunto, 'mensagem': formMensagem}, status=status.HTTP_201_CREATED)


def registration(request, token=None):
    if not request.user.is_anonymous:
        return HttpResponseRedirect(reverse('onboarding'))

    language = getLanguage(request)

    if request.method == 'POST':
        converted_request_body = json.loads(request.body)

        name = converted_request_body.get('name', '')
        email = converted_request_body.get('email', '').strip()
        client = converted_request_body.get('client', '')
        phone = re.sub('\D', '', converted_request_body.get('phone', ''))
        password = converted_request_body.get('password', '')
        department = converted_request_body.get('area', '')
        job_title = converted_request_body.get('role', '')
        user_role = int(converted_request_body.get('user_role', ''))

        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({'status': 400, 'msg': translate('invalid_email', language), 'field': 'email'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            if user_role == 4:
                user = {}
                user = User.objects.create_user(email=email, password=password)
                if user.id != None:
                    client_domain = email.split('@')[-1]

                    domain_is_standard = check_email_domain(client_domain)

                    if domain_is_standard:
                        client_identifier = uuid4()
                    else:
                        client_identifier = client_domain

                    try:
                        client = Client.objects.create(
                            name=client.strip(), domain=client_domain, identifier=client_identifier)
                        create_new_client_subscription(client)
                    except IntegrityError:
                        client = Client.objects.get(
                            identifier=client_identifier)

                    name_splitted = name.split(' ')
                    user.first_name = name_splitted[0]
                    if len(name_splitted) > 1:
                        user.last_name = name.split(' ')[1]
                    user.save()

                    profile = Profile.objects.get(user=user)

                    profile.set_client(client)
                    profile.set_language(language)
                    profile.set_department(department)
                    profile.set_job_title(job_title)

                    if phone:
                        profile.set_phone(phone)

                    admin = Profile.objects.filter(
                        role=4, client=client)
                    if len(admin) > 0:
                        user_role = 1
                    profile.set_role(user_role)
                    profile.save()

                    user_authenticated = authenticate(
                        request, username=email, password=password)
                    login(request, user_authenticated)

                    return JsonResponse({'status': 200}, status=status.HTTP_201_CREATED)

            else:
                user = User.objects.get(email=email)
                user_profile = Profile.objects.get(user=user)

                name_splitted = name.split(' ')
                user.first_name = name_splitted[0]
                if len(name_splitted) > 1:
                    user.last_name = name.split(' ')[1]

                user.set_password(password)
                user_profile.set_department(department)
                user_profile.set_job_title(job_title)
                user_profile.set_email_confirmed(True)

                if phone:
                    user_profile.set_phone(phone)

                update_session_auth_hash(request, user)

                user.save()
                user_profile.save()
                user_authenticated = authenticate(
                    request, username=email, password=password)
                login(request, user_authenticated)

                user_invites = Invites.objects.filter(email=user.email)
                for invite in user_invites:
                    invite.active = False
                    invite.save()

                return JsonResponse({'status': 200}, status=status.HTTP_201_CREATED)

        except IntegrityError as error:
            try:
                error_message = error.args[0]
                if 'email' in error_message:
                    message = translate(
                        'there_is_already_an_email_for_this_user', language)
                    field = 'email'
                else:
                    message = translate('error', language)
                    field = ''
            except:
                message = translate('error', language)
            finally:
                return JsonResponse({'status': 400, 'msg': message, 'field': field}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            try:
                if user != {} and user.id != None:
                    user.delete()
            except Exception as e:
                pass
            finally:
                return JsonResponse({'status': 401, 'msg': translate('error', language)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        first_step_inputs = [
            {
                'label': translate('name_surname', language),
                'type': 'text',
                'classes': '',
                'id': 'name-id',
                'name': 'name',
                'placeholder': translate('name_surname', language),
                'required': True,
                'error_message': translate('name_requirements', language),
            },
            {
                'label': 'E-mail',
                'type': 'email',
                'classes': '',
                'id': 'email-id',
                'name': 'email',
                'placeholder': 'E-mail',
                'required': True,
                'pattern': "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9_-]+\..[a-zA-Z0-9-.]{2,61}",
                'error_message': translate('email_requirements', language),
            },
            {
                'label': translate('password', language),
                'type': 'password',
                'classes': '',
                'id': 'password-id',
                'name': 'password',
                'placeholder': translate('password', language),
                'required': True,
                'pattern': "^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!@#$%^&*()_+]).{8,}$",
                'error_message': f"{translate('passwords_requirements', language)}.",
            },
        ]

        second_step_inputs = [
            {
                "label": translate('company', language),
                "id": "client-id",
                "name": "client",
                "type": "text",
                "classes": " input-company",
                "placeholder": translate('company', language),
                "required": True
            },

            {
                "label": translate('cell', language),
                "id": "phone-id",
                "name": "phone",
                "type": "text",
                "classes": "input-cel tooltip-phone form-group has-danger",
                "placeholder": "",
                "required": False
            },

            {
                "label": translate('job_title', language),
                "id": "role-id",
                "name": "role",
                "type": "select",
                "classes": " input-job-title",
                "placeholder": translate('job_title', language),
                "required": True,
                "options": [
                    {
                        "text": translate('select_position', language),
                        "value": "",
                    },
                    {
                        "text": translate('analyst', language),
                        "value": "Analista",
                    },
                    {
                        "text": translate('manager', language),
                        "value": "Gerente",
                    },
                    {
                        "text": translate('director', language),
                        "value": "Diretor",
                    },
                    {
                        "text": translate('specialist', language),
                        "value": "Especialista",
                    },
                    {
                        "text": translate('other', language),
                        "value": "other",
                    },
                ]
            },
            {
                "label": "",
                "id": "other-role-id",
                "name": "otherRole",
                "type": "text",
                "classes": "mb-3 d-none",
                "placeholder": translate('fill_in_your_position', language),
                "required": False
            },
            {
                "label": translate('sector_of_activity', language),
                "id": "area-id",
                "name": "area",
                "type": "select",
                "classes": " input-setor",
                "placeholder": translate('sector_of_activity', language),
                "required": True,
                "options": [
                    {
                        "text": translate('select_sector_of_activity', language),
                        "value": "",
                    },
                    {
                        "text": translate('administrative', language),
                        "value": "Administrativo",
                    },
                    {
                        "text": translate('customer_service', language),
                        "value": "Atendimento ao Cliente",
                    },
                    {
                        "text": translate('center_of_excellence_in_rpa', language),
                        "value": "Centro de Excelência -CoE- em RPA",
                    },
                    {
                        "text": translate('purchasing_and_supplies', language),
                        "value": "Compras e Suprimentos",
                    },
                    {
                        "text": translate('consultancy', language),
                        "value": "Consultoria",
                    },
                    {
                        "text": translate('finance_and_accounting', language),
                        "value": "Finanças e Contabilidade",
                    },
                    {
                        "text": translate('supervisor', language),
                        "value": "Fiscal",
                    },
                    {
                        "text": translate('legal', language),
                        "value": "Jurídico",
                    },
                    {
                        "text": translate('marketing', language),
                        "value": "Marketing",
                    },
                    {
                        "text": translate('operations', language),
                        "value": "Operações",
                    },
                    {
                        "text": translate('human_resources', language),
                        "value": "Recursos Humanos",
                    },
                    {
                        "text": translate('information_technology', language),
                        "value": "Tecnologia da Informação",
                    },
                    {
                        "text": translate('other', language),
                        "value": "other",
                    },

                ]

            },
            {
                "label": "",
                "id": "other-area-id",
                "name": "otherArea",
                "type": "text",
                "classes": "mb-3 d-none",
                "placeholder": translate('fill_in_the_sector_of_activity', language),
                "required": False
            },
        ]

        context = {
            'language': language,
            'mandatory_form_identifier': '/register',
            'optional_form_identifier': '/register/extra-info',
            'hidenavbar': 1,
            'hidehole_navbar': True,
            'hide_warnings': True,
            'body_class': 'whitebackcolor',
            'first_step_inputs': first_step_inputs,
            'second_step_inputs': second_step_inputs,
            'not_websocket': True
        }
        if token != None:
            try:
                user_invitation = Invites.objects.filter(token=token)
                if len(user_invitation) == 1 and user_invitation.first().active == True:
                    user_invitation = user_invitation.first()

                    context['invite_with_service'] = True
                    context['new_user_email'] = user_invitation.get_email()
                    context['new_user_company'] = user_invitation.get_client(
                    ).get_client_name()

                else:
                    return HttpResponseRedirect(reverse('registration'))

            except Exception:
                return HttpResponseRedirect(reverse('registration'))

        return render(request, "registration.html", context)


def conclude_registry(request):
    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse('login'))
    elif not isClientMainUser(request.user):
        return HttpResponseRedirect(reverse('onboarding'))

    client = get_client_from_request(request)

    subscription = Subscription.getSubscriptionByClient(client)
    automations_clients = AutomationsClients.objects.values('id').filter(
        client=client)

    if subscription != None and len(automations_clients) > 0:
        return HttpResponseRedirect(reverse('onboarding'))  # or http response

    language = getLanguage(request)

    filters = {}
    number_of_total_services = 0

    all_permitted_automations = Automation.get_automations_with_ui(
        language, client)

    for automation in all_permitted_automations:
        automation_group = translate(automation.group, language)
        if not automation_group in filters:
            filters[automation_group] = 0

        filters[automation_group] += 1
        number_of_total_services += 1

    sorted_filters = sort_dict_by_key(filters)
    all_filters = {"all_male": number_of_total_services}

    filters_with_all_first = {**all_filters, **sorted_filters}

    context = {
        'language': language,
        'hidehole_navbar': 1,
        'hide_warnings': True,
        'all_automations': all_permitted_automations,
        'filters': filters_with_all_first,
        'not_websocket': True
    }
    return render(request, "choosing_services.html", context)


def submit_registry(request):

    def update_new_client_subscription(qnt_services_allocated, dashboard):
        client = get_client_from_request(request)
        subscription = Subscription.objects.get(client=client)

        subscription.set_number_of_hired_services(qnt_services_allocated)
        subscription.set_value(0)
        subscription.set_dashboard(dashboard)
        subscription.set_active(True)

        subscription.save()

    language = getLanguage(request)
    user = request.user

    try:
        converted_request_body = json.loads(request.body)
        dashboard = int(converted_request_body.get('with_dashboard', 0))
        automations_allocated = converted_request_body.get(
            'automations_allocated', '')

        client = get_client_from_request(request)

        number_of_allocated_licenses = 0

        # ficar atento, pois o cara que tirar o dashboard, vai ganhar um serviço a mais
        AutomationsClients.objects.filter(
            client=client).delete()
        UsersPlans.objects.filter(client=client).delete()
        all_showcase = {}

        if len(automations_allocated) > 0:
            for index, automation_name in enumerate(automations_allocated):
                automation_obj = get_automation_by_name(automation_name)
                ac = AutomationsClients(client=client, automation=automation_obj,
                                        qnt_automations=automations_allocated[automation_name])
                if automation_name == 'extrato-bancario':
                    ac.can_create_model = 3
                ac.save()
                number_of_allocated_licenses += automations_allocated[automation_name]

                if automation_obj.get_is_showcase() and automation_name not in all_showcase:
                    all_showcase[automation_name] = automations_allocated[automation_name]
                elif automation_name in all_showcase:
                    all_showcase[automation_name] += automations_allocated[automation_name]

        if dashboard == 1:
            with_dashboard = True
            number_of_allocated_licenses += 1
        else:
            with_dashboard = False

        update_new_client_subscription(
            qnt_services_allocated=number_of_allocated_licenses, dashboard=with_dashboard)

        AutomationsClients.resetAutomationsClientsByClient(client)
        UsersPlans.resetUsersPlansByClientAndAutomationsIds(client)

        if bool(all_showcase):
            email_context = {
                'language': language,
                'user': request.user,
                'all_showcase': all_showcase,
            }
            sendEmail('showcaseRequest', '[Cadastro Free Trial] Solicitação de Automação Vitrine' +
                      ' Smarthis Hub', get_people_to_send_email('product'), email_context)

        user_uid = urlsafe_base64_encode(force_bytes(user.pk))
        token_to_verify_email = account_activation_token.make_token(user)

        link_to_verify_email = f"{getHubUrl()}accounts/email-confirmation/{user_uid}/{token_to_verify_email}"

        sendEmail('freeTrial', translate('your_smarthis_hub_trial_period_has_begun',
                  language), request.user.email, {'language': language, 'link': link_to_verify_email, 'user': request.user})

        return JsonResponse({'status': 200}, status=status.HTTP_201_CREATED)
    except Exception as e:
        print(e)
        return JsonResponse({'status': 400, 'msg': translate('error', language)}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


def email_confirmation(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        user_profile = user.profile
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    token_is_valid = account_activation_token.check_token(user, token)
    if user is not None and token_is_valid:
        user_profile.set_email_confirmed(True)
        user_profile.save()
        return HttpResponseRedirect(reverse('email_confirmed_view'))
    else:
        return HttpResponseRedirect(reverse('login'))


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@require_http_methods(["POST"])
def edit_profile_user(request):

    language = getLanguage(request)
    converted_request_body = json.loads(request.body)
    email = converted_request_body.get('email', None)
    user_name = converted_request_body.get('user', None)
    department = converted_request_body.get('department', None)
    phone = converted_request_body.get('phone', None)
    old_password = converted_request_body.get('old_password', None)
    new_password = converted_request_body.get('new_password', None)
    try:
        user = request.user
        user_profile = Profile.objects.get(user=user)
        if old_password and new_password:
            if request.user.check_password(old_password):
                request.user.set_password(new_password)

                request.user.save()
                update_session_auth_hash(request, request.user)
                sendEmail('mudancaSenha', translate('password_change', language) + ' Smarthis Hub',
                          request.user.email, {'language': language, 'user': request.user})
            else:
                return JsonResponse({'status': 400, 'msg': translate('old_password_does_not_match', language)}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        if email:
            try:
                validate_email(email)
            except ValidationError:
                return JsonResponse({'status': 400, 'msg': translate('invalid_email', language)}, status=status.HTTP_400_BAD_REQUEST)

            user.set_email(email)
        if user_name:
            name_splitted = user_name.split(' ')
            user.first_name = name_splitted[0]
            if len(name_splitted) > 1:
                user.last_name = user_name.split(' ')[1]
            else:
                user.last_name = ''
        user.save()
        if department:
            user_profile.set_department(department)
            user_profile.save()

        if phone:
            user_profile.set_phone(phone)
            user_profile.save()

        return JsonResponse({'status': 200}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return JsonResponse({'status': 400, 'msg': translate('there_was_an_error_saving_your_profile', language)}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@csrf_exempt
def generate_authetication_token(request):
    # check if is a POST request
    if request.method != 'POST':
        return HttpResponseBadRequest()

    request_body = json.loads(request.body.decode('utf-8'))

    email = request_body['email']
    password = request_body['password']

    # guard empty values
    if email == '' or email == None:
        return HttpResponseBadRequest()
    if password == '' or password == None:
        return HttpResponseBadRequest()

    # check password
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return HttpResponseForbidden()

    valid_password = check_password(password, user.password)
    if not valid_password:
        return HttpResponseForbidden()

    # check if has active subscription
    subscriptions = Subscription.objects.filter(
        client=user.profile.client, active=True).prefetch_related('plan__services')

    if subscriptions.count() < 1:
        return HttpResponseForbidden()

    role = (
        (1, 'Service Account'),
        (2, 'Client'),
        (3, 'Admin'),
        (4, 'Main'),
        (5, 'Editor Account'),
        (6, 'View Account'),
    )[user.profile.role - 1][1]

    response = {
        'user': {
            'name': "%s %s" % (user.first_name, user.last_name),
            'email': user.email,
            'is_active': user.is_active,
            'client': user.profile.client.name,
            'role': role
        },
        'token': '',
    }

    to_sign = {
        'iss': 'Smarthis',
        'aud': 'dev.silvalabs.space',
        'exp': datetime.utcnow() + timedelta(hours=1)
    }

    to_sign.update(response)

    token = jwt.encode(
        to_sign, 'ghjhgtyr675isfd656756453ghfdhgfljjh', algorithm='HS256')

    response.update({'token': "%s" % (token.decode('ascii'))})
    print(token)
    return JsonResponse(response)


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@require_http_methods(["POST"])
def exclude_user(request):

    data = {}
    converted_request_body = json.loads(request.body)
    all_users_remove = converted_request_body.get('all_users_remove')

    try:
        Profile.objects.filter(user__id__in=all_users_remove).delete()
        UsersPlans.objects.filter(
            user__id__in=all_users_remove).delete()
        delete_schedules_from_user(
            all_users_remove_list=all_users_remove)
        User.objects.filter(id__in=all_users_remove).delete()
        UsersPlans.resetUsersPlansByClientAndAutomationsIds(
            get_client_from_request(request))

    except Exception as e:
        print(e)
        return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return JsonResponse(data, status=status.HTTP_200_OK)


@require_http_methods(["POST"])
def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            user_email = password_reset_form.cleaned_data['email']
            try:
                user = User.objects.get(email=user_email)
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                sendEmail('html_password_reset_email',
                          'Mudança de Senha', user_email, {'user_reset': user, 'link': f'{getHubUrl()}accounts/reset/{uid}/{token}'})
            except User.DoesNotExist:
                context = {'email_not_exist': True,
                           'language': getLanguage(request)}
                return render(request, template_name='registration/password_reset_form.html', context=context)
            except:
                return reverse('password_reset')
            return HttpResponseRedirect(reverse('password_reset_done'))


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@require_http_methods(["POST"])
def get_user_by_email_and_client(request):
    language = getLanguage(request)
    converted_request_body = json.loads(request.body)
    email_to_invite = converted_request_body.get('email')
    try:
        profile_to_invite = Profile.get_user_by_email_and_client(
            email_to_invite, request.user.profile.client)
        name = profile_to_invite.user.get_full_name()
        return JsonResponse({'status': 200, 'id': profile_to_invite.user.id, 'name': name, 'initials': get_name_initials(name)}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return JsonResponse({'status': 400, 'msg': translate('user_not_found', language) + '. ' + translate('are_you_sure_this_user_works_with_you', language), 'error': str(e)}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@require_http_methods(["POST"])
def save_login_infos(request):
    data = {}
    converted_request_body = json.loads(request.body)
    session_start = converted_request_body.get('session_start')
    session_end = converted_request_body.get('session_end')

    def get_duration(duration):
        hours = int(duration / 3600)
        minutes = int(duration % 3600 / 60)
        seconds = int((duration % 3600) % 60)
        return [hours, minutes, seconds]

    try:
        user_ip_address = get_ip_address(request)
        user_id = request.user.id
        converted_session_start = datetime.fromtimestamp(
            session_start/1000, tz=pytz.utc)
        converted_session_end = datetime.fromtimestamp(
            session_end/1000, tz=pytz.utc)
        if converted_session_end > converted_session_start:
            difference_between_dates = (
                converted_session_end - converted_session_start).total_seconds()

            session_duration = get_duration(difference_between_dates)

            converted_session_duration = time(
                session_duration[0], session_duration[1], session_duration[2])
            new_session_info_entry = SessionInfo.objects.create(
                user_id=user_id, session_start=converted_session_start, session_end=converted_session_end, session_duration=converted_session_duration, user_ip_address=user_ip_address)

            new_session_info_entry.save()

            return JsonResponse(data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        print(e)
        return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def end_of_trial_summary(request):
    client = get_client_from_request(request)
    previous_plan = getUserPlan(request=request)

    client_is_awaiting_evaluation = previous_plan.get_plan_name() == 'Business Trial'

    if not request.free_trial_ended and not client_is_awaiting_evaluation:
        return HttpResponseRedirect(reverse('onboarding'))

    language = getLanguage(request)

    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse('login'))
    elif not isClientMainUser(request.user):
        return HttpResponseRedirect(reverse('onboarding'))

    client = get_client_from_request(request)

    previous_subscription = request.subscription

    hired_services = AutomationsClients.objects.filter(
        client=client).count()
    dashboard = previous_subscription.get_dashboard()

    client_users = get_users_from_client(client)
    schedules_created = Schedule.objects.filter(user__in=client_users)
    related_tasks = Task.objects.filter(schedule__in=schedules_created)

    number_of_licenses_used = 0

    for task in related_tasks:
        if task.state != 2:
            number_of_licenses_used += 1

    client = get_client_from_request(request)

    has_plan_negotiation = True if previous_plan.get_plan_name(
    ) == 'Business Trial' else False

    if number_of_licenses_used + dashboard <= 1 and has_plan_negotiation == False:
        recommended_plan = 'starter'
    elif number_of_licenses_used + dashboard <= 3 and has_plan_negotiation == False:
        recommended_plan = 'advanced'
    else:
        recommended_plan = 'business'

    if recommended_plan != 'business':
        plan = Plan.objects.get(
            name=recommended_plan.capitalize())
    elif has_plan_negotiation == False:
        plan = get_plan_info(recommended_plan)
    else:
        plan = previous_plan

    help_questions = [{
        'title': f"{translate('can_i_change_my_plan_after_hiring', language)}?",
        'text': f"{translate('can_i_change_my_plan_after_hiring_answer_1', language)} <strong class=text_decoration>{translate('can_i_change_my_plan_after_hiring_answer_2', language)}</strong>"
    }, {
        'title': f"{translate('what_forms_of_payment_hub_accepts', language)}?",
        'text': f"{translate('what_forms_of_payment_hub_accepts_answer_1', language)}<p class=text--content-help m-0 w-100>{translate('what_forms_of_payment_hub_accepts_answer_2', language)} <a class=text_decoration href=https://pagar.me/ target=_blank>Pagar.me.</a></p>"
    }, {
        'title': f"{translate('will_i_receive_an_invoice_after_hiring', language)}?",
        'text': translate('will_i_receive_an_invoice_after_hiring_answer', language)
    }]

    context = {
        'language': language,
        'hidehole_navbar': 1,
        'hide_warnings': True,
        'help_questions': help_questions,
        'services_used': f'{hired_services:02}',
        'dashboard': dashboard,
        'licenses_used': f'{number_of_licenses_used:02}',
        'plan': plan,
        'recommended_plan': recommended_plan,
        'all_plans': get_plan_info(),
        'has_plan_negotiation': has_plan_negotiation,
        'subscription': previous_subscription
    }
    return render(request, "free_trial_summary.html", context)


def end_of_trial_choose_plan(request, desired_plan, period=None):
    plan = getUserPlan(request=request)
    has_plan_negotiation = True if plan.get_plan_name(
    ) == 'Business Trial' else False
    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse('login'))
    elif not request.free_trial_ended and not has_plan_negotiation:
        return HttpResponseRedirect(reverse('onboarding'))
    elif not isClientMainUser(request.user):
        return HttpResponseRedirect(reverse('onboarding'))

    language = getLanguage(request)
    client = get_client_from_request(request)

    all_plans_info = get_plan_info()

    if desired_plan not in all_plans_info and 'business trial' not in plan.get_plan_name().lower():
        return HttpResponseRedirect(reverse('end_of_trial_summary'))

    if desired_plan == 'business':
        # can only calculate has_plan_negotiation if desired plan is business
        if has_plan_negotiation:
            desired_plan_info = plan
        else:
            desired_plan_info = all_plans_info[desired_plan]
    else:
        desired_plan_info = all_plans_info[desired_plan]

    if (period == None and desired_plan != 'business') or ((period != None and has_plan_negotiation == False) and desired_plan == 'business'):
        return HttpResponseRedirect(reverse('end_of_trial_summary'))

    is_upgrade = False
    if plan != False and desired_plan != 'business':
        is_upgrade = is_plan_upgrade(
            request.subscription, desired_plan_info, period)
    elif desired_plan == 'business':
        is_upgrade = True

    if is_upgrade:
        if request.subscription.get_payment_period().lower() == 'yearly':
            # in case user has year plan saved and wants to get a monthly payment, is problematic because can be a downgrade
            period = 'yearly'

        services_obj = get_client_services_and_utilizations(
            client, language, desired_plan, desired_plan_info, has_plan_negotiation, request.subscription)

        context = {
            'language': language,
            'hidehole_navbar': 1,
            'hide_warnings': True,
            'plan': desired_plan,
            'plan_info': desired_plan_info,
            'services': services_obj['services'],
            'dashboard': request.subscription.get_dashboard(),
            'period': period,
            'licenses_limit': request.subscription.get_number_of_hired_services(),
            'licenses_used': services_obj['licenses_used'],
            'dashboard_checked': services_obj['dashboard_checked'],
            'pagarme': getPagarmeSecretKey(getPagarmeTest()),
            'has_plan_negotiation': has_plan_negotiation
        }

        if has_plan_negotiation and desired_plan == 'business':
            context['subscription'] = request.subscription

        return render(request, "free_trial_choose_plan.html", context)
    else:
        return HttpResponseRedirect(reverse('end_of_trial_summary'))


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def update_plan(request, desired_plan, period, plus=None):
    if not isClientMainUser(request.user):
        return HttpResponseRedirect(reverse('onboarding'))

    language = getLanguage(request)
    client = get_client_from_request(request)
    subscription = request.subscription

    plan = getUserPlan(request=request)

    all_plans_info = get_plan_info()

    if desired_plan not in all_plans_info and 'business trial' not in plan.get_plan_name().lower():
        return HttpResponseRedirect(reverse('onboarding'))

    has_plan_negotiation = True if plan.get_plan_name(
    ) == 'Business Trial' else False

    if desired_plan == 'business':
        # TODO: quando for um upgrade no plano, selecionar todos os serviços da pessoa
        if has_plan_negotiation:
            desired_plan_info = plan
        else:
            desired_plan_info = all_plans_info[desired_plan]
    else:
        desired_plan_info = all_plans_info[desired_plan]

    is_upgrade = False
    if plan != False and desired_plan != 'business':
        is_upgrade = is_plan_upgrade(
            subscription, desired_plan_info, period, plus)
    elif desired_plan == 'business':
        is_upgrade = True

    if is_upgrade and not has_plan_negotiation:
        services_obj = get_client_services_and_utilizations(
            client, language, desired_plan, desired_plan_info, has_plan_negotiation, subscription,  is_upgrade)

        context = {
            'language': language,
            'hidehole_navbar': 1,
            'hide_end_of_trial_warning': 1,
            'plan': desired_plan,
            'plan_info': desired_plan_info,
            'services': services_obj['services'],
            'dashboard': subscription.get_dashboard(),
            'period': period,
            'licenses_limit': subscription.get_number_of_hired_services(),
            'licenses_used': services_obj['licenses_used'],
            'dashboard_checked': services_obj['dashboard_checked'],
            'pagarme': getPagarmeSecretKey(getPagarmeTest()),
            'has_plan_negotiation': has_plan_negotiation,
            'plus': plus,
            'chosen_queries': subscription.get_queries_limit(),
            'subscription': subscription
        }
        return render(request, "free_trial_choose_plan.html", context)
    elif has_plan_negotiation:
        return HttpResponseRedirect(reverse('end_of_trial_summary'))
    else:
        return HttpResponseRedirect(reverse('onboarding'))


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@require_http_methods(["POST"])
def save_chosen_plan(request):
    data = {}

    people_to_send_email = get_people_to_send_email()
    try:
        language = getLanguage(request)
        user = request.user
        client = get_client_from_request(request)
        client_subscription = request.subscription
        converted_request_body = json.loads(request.body)
        plan = converted_request_body.get('chosen_plan')
        chosen_services = converted_request_body.get('chosen_services', [])
        lost_services = converted_request_body.get('lost_services', {})
        plan_value = converted_request_body.get('plan_value', 0)
        schedules_to_be_deleted = converted_request_body.get(
            'schedules_to_be_deleted', [])
        forbidden_schedules = converted_request_body.get(
            'forbidden_schedules', {})

        if 'dashboard' in chosen_services:
            with_dashboard = True
        else:
            with_dashboard = False

        automations_plans_to_reduce_quantity = {}
        for service in lost_services:
            service_name = list(service.keys())[0]
            user_that_used_this_service = list(service.values())[0]

            if user_that_used_this_service != None and service_name != 'dashboard':
                user_that_used_this_service = int(user_that_used_this_service)

                target_licenses = UsersPlans.objects.filter(
                    client=client, automation__name=service_name, user__id=user_that_used_this_service)

                target_licenses.delete()

            if service_name not in automations_plans_to_reduce_quantity:
                automations_plans_to_reduce_quantity[service_name] = 0
            automations_plans_to_reduce_quantity[service_name] += 1

        all_schedules_to_be_deleted = Schedule.objects.filter(
            id__in=schedules_to_be_deleted).exclude(id__in=forbidden_schedules.keys(), user__id__in=forbidden_schedules.values())

        for schedule in all_schedules_to_be_deleted:
            erase_schedule_in_s3_and_database(schedule)

        target_automation_clients = AutomationsClients.objects.filter(
            client=client, automation__name__in=automations_plans_to_reduce_quantity.keys())

        automations_with_one_license = []
        automations_plan_with_one_license = target_automation_clients.filter(
            qnt_automations=1)

        deleted_automations = {}
        for automation_plan in automations_plan_with_one_license:
            automation_name = automation_plan.automation.name
            if automation_name not in deleted_automations:
                deleted_automations[automation_name] = 0

            if deleted_automations[automation_name] < automations_plans_to_reduce_quantity[automation_name]:
                automations_with_one_license.append(
                    automation_plan.automation)
                automation_plan.delete()
                deleted_automations[automation_name] += 1

        automations_with_one_license_users_plans = UsersPlans.objects.filter(
            client=client, automation__in=automations_with_one_license)
        automations_with_one_license_users_plans.delete()

        automation_plan_with_more_than_one_license = target_automation_clients.exclude(
            qnt_automations=1)

        for automation_plan in automation_plan_with_more_than_one_license:
            automation_name = automation_plan.automation.name
            quantity_to_subtract = automations_plans_to_reduce_quantity[automation_name]
            automation_plan.subtract_qnt_automations(quantity_to_subtract)
            how_many_licenses_left = automation_plan.get_qnt_automations()
            if how_many_licenses_left > 0:
                automation_plan.save()
            else:
                automation_plan.delete()
                all_service_licenses = UsersPlans.objects.filter(
                    client=client, automation__name=automation_name)
                all_service_licenses.delete()
        UsersPlans.resetUsersPlansByClientAndAutomationsIds(
            client)

        if plan == 'business':
            chosen_number_of_licenses = int(
                converted_request_body.get('chosen_number_of_licenses'))

            chosen_number_of_queries = converted_request_body.get(
                'chosen_number_of_queries')
            if chosen_number_of_queries != 'unlimited':
                number_of_queries = int(
                    chosen_number_of_queries)
            else:
                number_of_queries = 0

            number_of_services = chosen_number_of_licenses

            email_context = {'language': 'pt-BR', 'number_of_licenses': number_of_services,
                             'number_of_queries': chosen_number_of_queries, 'services': chosen_services,  'client': client, 'user': request.user}

            if plan_value == 0:
                plan_name = 'Business Trial'
                email_template = 'avaliacaoPlanoBusiness'
                email_title = 'Nova avaliação de Plano Business solicitada'
                # in this case, no payment is necessary
                now = datetime.today().date()
                data = Subscription.updateSubscriptionAfterPayment(
                    {'status': 200}, client, now, None, 'waiting-product-team')
                client_subscription = Subscription.getSubscriptionByClient(
                    client)
            else:
                cnpj = converted_request_body.get('cnpj')
                chosen_period = converted_request_body.get('chosen_period')

                email_context['cnpj'] = cnpj
                set_company_info_with_cnpj(client=client, cnpj=cnpj)
                plan_name = 'Business'
                if 'yearly' in chosen_period:
                    client_subscription.set_payment_period('YEARLY')
                email_template = 'novoPlanoCadastrado'
                email_title = 'Novo Plano foi Cadastrado'

            new_plan = Plan.objects.get(name=plan_name)

            client_subscription.set_subscription_plan(new_plan)
            client_subscription.set_dashboard(with_dashboard)
            client_subscription.set_number_of_hired_services(
                number_of_services)
            client_subscription.set_queries_limit(number_of_queries)

            client_subscription.set_value(plan_value)

            sendEmail(email_template, email_title,
                      people_to_send_email, email_context)

        else:
            cnpj = converted_request_body.get('cnpj')
            chosen_period = converted_request_body.get('chosen_period')

            set_company_info_with_cnpj(client=client, cnpj=cnpj)

            with_extra_queries = int(converted_request_body.get(
                'with_extra_queries'))

            if with_extra_queries == 1:
                with_extra_queries = True
            else:
                with_extra_queries = False

            new_plan = Plan.objects.get(name=plan.capitalize())
            plan_value = new_plan.get_value()

            client_subscription.set_subscription_plan(new_plan)
            client_subscription.set_dashboard(with_dashboard)
            client_subscription.set_number_of_hired_services(
                new_plan.get_plan_qnt_automations())
            client_subscription.set_extra_queries(with_extra_queries)
            client_subscription.set_payment_period(chosen_period.upper())

            if with_extra_queries:
                regular_queries_limit = new_plan.get_plan_qnt_queries()
                extra_queries = new_plan.get_plan_qnt_extra_queries()
                number_of_queries = regular_queries_limit + extra_queries
                plan_value += new_plan.get_extra_price()
            else:
                number_of_queries = new_plan.get_plan_qnt_queries()

            client_subscription.set_queries_limit(number_of_queries)

            if chosen_period.upper() == 'YEARLY':
                plan_value = plan_value * 10
            client_subscription.set_value(plan_value)

            sendEmail('novoPlanoCadastrado', "Novo Plano foi Cadastrado", people_to_send_email, {
                'language': 'pt-BR', 'plan': plan, 'period': translate(chosen_period, 'pt-BR'), 'extra_queries': with_extra_queries, 'services': chosen_services, 'cnpj': cnpj, 'client': client, 'user': request.user})

        client_subscription.set_subscription_plan(new_plan)
        client_subscription.save()
        Subscription.resetSubscriptionByClient(client)
        AutomationsClients.resetAutomationsClientsByClient(client)

        if plan != 'business' or plan_value != 0:
            try:
                plan_name = plan.capitalize()
                if plan == 'business':
                    number_of_licenses = number_of_services
                    queries = number_of_queries if number_of_queries != 0 else translate(
                        "unlimited", language)
                else:
                    number_of_licenses = new_plan.get_plan_qnt_automations()
                    queries = new_plan.get_plan_qnt_queries()

                chosen_period = converted_request_body.get('chosen_period')

                if language == 'pt-BR':
                    today_date = datetime.now().strftime("%d/%m/%Y")
                else:
                    today_date = datetime.now().strftime("%m/%d/%Y")

                payment = PagarmeSubscriptions.objects.filter(
                    client=client).values('payment_type')[0].get('payment_type')

                if payment:
                    payment_display_name = translate(payment, language)
                else:
                    payment_display_name = ""

                payment_value = Subscription.getSubscriptionByClient(
                    client).get_value()

                sendEmail('yourPlanWasHired', f"{translate('congrats_subscription_to_the_following_plan', language)} {plan_name} {translate('confirmed', language)}", user.email, {
                    'language': language, 'plan_name': plan_name, 'number_of_licenses': number_of_licenses, 'queries': queries, 'today': today_date, 'payment_type': payment_display_name, 'period': translate(chosen_period, language), 'value': payment_value, 'user': request.user, })
            except Exception as e:
                pass

        return JsonResponse(data, status=status.HTTP_201_CREATED)

    except Exception as e:
        print('error', e, e.__traceback__.tb_lineno)
        return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@require_http_methods(["POST"])
def pay_subscription(request):
    response_data = {'status': 200}
    converted_request_body = json.loads(request.body)
    client = get_client_from_request(request)
    subscription = request.subscription
    try:
        client = get_client_from_request(request)
        test_pagarme = getPagarmeTest()

        plan_pagarme_name = converted_request_body.get('plan')
        try:
            if 'starter' in plan_pagarme_name:
                plan_obj = Plan.objects.get(name='Starter')
            elif 'advanced' in plan_pagarme_name:
                plan_obj = Plan.objects.get(name='Advanced')
            else:
                plan_obj = subscription.get_subscription_plan()
        except Exception as e:
            plan_obj = subscription.get_subscription_plan()

        chosen_period = converted_request_body.get('chosen_period')

        plan_days = '30'
        if 'year' in chosen_period:
            plan_days = '365'
        if test_pagarme:
            plan_days = '3'

        amount = converted_request_body.get('amount')
        if 'business' in plan_pagarme_name:
            subscription_value = str(subscription.get_value()).replace('.', '')
            # se o valor pago pelo cartão em amount for diferente do valor do plano, o usuário optou pelo pagamento anual do business
            if amount != int(subscription_value):
                subscription.set_value(amount)
            if 'Trial' in plan_obj.get_plan_name():
                new_plan = Plan.objects.get(name='Business')
                subscription.set_subscription_plan(new_plan)
            subscription.set_payment_period(chosen_period.upper())
            subscription.save()
            plan_pagarme_name = 'Business'
        else:
            plan_pagarme_name = plan_obj.get_plan_name()

        plan_payload = {
            # amount is sent as a number but divided by 100 on pagarme, for cents calculation
            "amount": amount,
            "days": plan_days,
            "name": plan_pagarme_name
        }
        plan_pagarme = getPagarmePlan(test_pagarme, plan_payload)
        if type(plan_pagarme) == dict:
            response_data = plan_pagarme
            return JsonResponse(response_data, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            customer = converted_request_body.get('customer')
            payment_method = converted_request_body.get('payment_method')
            payload_subscription = {
                'plan_id': plan_pagarme.plan_pagarme_id,
                "customer": {
                    "email": customer['email'],
                    "name": customer['name'],
                    "document_number": customer['document_number'],
                    "address": customer['address'],
                    "phone": customer['phone']
                },
                "payment_method": payment_method,
                "postback_url": f"{getHubUrl(False)}pagarme/feedback",
            }
            if payment_method == 'credit_card':
                card_hash = converted_request_body.get('card_hash')
                payload_subscription['card_hash'] = card_hash

            language = getLanguage(request)
            try:
                pagarme_subscription = PagarmeSubscriptions.objects.get(
                    client=client, is_test=test_pagarme)
                # new_future_infos = calculatePagarmeSubscriptionUpdate(request, pagarme_subscription, plan_days)
                if payment_method == 'boleto' and pagarme_subscription.get_payment_type() == 'boleto':
                    payload_subscription.pop('payment_method', None)
                subscription_pagarme = updatePagarmeSubscription(
                    test_pagarme, pagarme_subscription, payload_subscription, language)
            except ObjectDoesNotExist:
                subscription_pagarme = setPagarmeSubscription(
                    test_pagarme, client, payload_subscription, language)

            if type(subscription_pagarme) == dict:
                response_data = subscription_pagarme
            return JsonResponse(response_data, status=status.HTTP_201_CREATED)

    except Exception as e:
        return JsonResponse({'status': 401, 'msg': 'error', 'error': str(e)}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'POST'])
def pagarme_feedback(request):
    json_result = {'status': 400, 'msg': ':-p'}
    payload = ''
    signature = ''

    if request.body:
        payload = request.body.decode()
        payload = payload.encode('utf-8')

        header_signature = request.META.get('HTTP_X_HUB_SIGNATURE', None)
        if header_signature != None:
            signature = header_signature
        else:
            header_signature = request.META.get('X-Hub-Signature', None)
            if header_signature != None:
                signature = header_signature
    if payload != '':
        signature = re.sub('sha1=', '', signature)
        json_result['signature'] = signature

        test_pagarme = getPagarmeTest()

        api_key = getPagarmeAPIKey(test_pagarme)
        hashed = hmac.new(api_key.encode(), payload, sha1)
        hex_signature = binascii.b2a_hex(hashed.digest())
        generated_signature = hex_signature.decode()

        if generated_signature == signature:
            json_result['msg'] = 'proceeding...'
            try:
                if request.method == 'POST':
                    payload_json = request.POST.dict()
                    # checar as infos com o pagarme_subscription
                    if 'current_status' in payload_json and payload_json['current_status'] == 'canceled':
                        pagarme_subscription_id = payload_json['subscription[id]']
                        cancel_json = cancelPagarmeSubscription(
                            pagarme_subscription_id)
                        if cancel_json['status'] == 200:
                            json_result = cancel_json
                            print('subscription canceled')
                        else:
                            json_result = {'status': 401,
                                           'msg': cancel_json['msg']}
                    elif 'current_status' in payload_json and (payload_json['current_status'] == 'paid' or payload_json['current_status'] == 'unpaid'):
                        try:
                            period_dict = {'current_period_start': payload_json['subscription[current_period_start]'],
                                           'current_period_end': payload_json['subscription[current_period_end]']}
                            period_dict = getSubscriptionPeriodFromJson(
                                period_dict)
                            print('INFOS FROM PAYLOAD_JSON ------------------>')
                            print(payload_json['subscription[id]'], payload_json['subscription[current_transaction][payment_method]'],
                                  period_dict['start'], period_dict['end'], payload_json['current_status'])
                            print('INFOS FROM PAYLOAD_JSON ------------------>')

                            pagarme_subscription = PagarmeSubscriptions.objects.get(
                                subscription_pagarme_id=payload_json['subscription[id]'])
                            pagarme_subscription.set_payment_type(
                                payload_json['subscription[current_transaction][payment_method]'])
                            pagarme_subscription.set_current_period_start(
                                period_dict['start'])
                            pagarme_subscription.set_current_period_end(
                                period_dict['end'])

                            try:
                                pagarme_subscription.save()
                            except Exception as e:
                                json_result['error'] = 'Error saving pagarmesubscription'
                            finally:
                                json_result = {'status': 200,
                                               'msg': 'Payment done'}
                                json_result = Subscription.updateSubscriptionAfterPayment(json_result, pagarme_subscription.get_client(
                                ), period_dict['start'], period_dict['end'], payload_json['current_status'])
                        except ObjectDoesNotExist:
                            json_result = {'status': 402,
                                           'msg': 'Pagarmsubscription not found'}

            except Exception as e:
                # no method found or error on post
                print(str(e))

    print(json_result)
    return JsonResponse(json_result, status=status.HTTP_200_OK)


def chosen_plan_feedback(request):
    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse('login'))
    elif not isClientMainUser(request.user):
        return HttpResponseRedirect(reverse('onboarding'))

    language = getLanguage(request)

    client = get_client_from_request(request)

    plan = getUserPlan(request=request)
    all_hired_automations = AutomationsClients.objects.filter(client=client)
    allowed_automations = Automation.get_automations_with_ui(language, client)

    hired_services = {}

    for automation_plan in all_hired_automations:
        automation_name = automation_plan.automation.name
        automation_name_is_allowed = check_if_automation_name_is_in_query(
            automation_name=automation_name, query=allowed_automations)

        if automation_name_is_allowed:
            hired_services[automation_name] = {
                'display_name': get_automation_display_name(automation_plan.automation, language)}
            hired_services[automation_name]['quantity'] = automation_plan.qnt_automations

    if request.subscription.get_dashboard():
        hired_services['dashboard'] = {
            'display_name': 'Dashboard', 'quantity': 1}

    plan_name = plan.get_plan_name()

    if 'business trial' in plan_name.lower():
        plan_name = 'Business'

    context = {
        'language': language,
        'hidehole_navbar': 1,
        'hide_warnings': True,
        'plan': plan,
        'subscription': request.subscription,
        'hired_services': hired_services,
        'dashboard': request.subscription.get_dashboard(),
        'plan_name': plan_name,
    }

    return render(request, "free_trial_concluded_feedback.html", context)


def send_email_confirmation(request):
    language = getLanguage(request)
    user = request.user

    try:
        user_uid = urlsafe_base64_encode(force_bytes(user.pk))
        token_to_verify_email = account_activation_token.make_token(user)

        link_to_verify_email = f"{getHubUrl()}accounts/email-confirmation/{user_uid}/{token_to_verify_email}"

        sendEmail('confirmEmail', translate('confirm_your_email_address',
                                            language), request.user.email, {'language': language, 'link': link_to_verify_email})
        return JsonResponse({}, status=status.HTTP_200_OK)
    except Exception as e:
        print('erro', e, e.__traceback__.tb_lineno)
        return JsonResponse({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def email_confirmed_view(request):
    language = getLanguage(request)

    context = {
        'language': language,
        'hidehole_navbar': True,
        'hide_warnings': True,
    }

    return render(request, "email_confirmed.html", context)
