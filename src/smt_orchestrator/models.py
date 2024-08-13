from datetime import datetime
import pytz
from django.db import models
from django.conf import settings
from django_unixdatetimefield import UnixDateTimeField
from django.core.cache import cache

from types import SimpleNamespace

from subscriptions.models import Client

# Create your models here.


class Automation(models.Model):

    TYPES = (
        ('upload', 'Upload'),
        ('credential', 'Credential'),
        ('upload_and_credential', 'Upload and Credential'),
        ('credential_and_filter_notes', 'Credential and Filter Notes'),
    )

    GROUPS = (
        ('banking', 'Banking'),
        ('cadastral_status', 'Cadastral Status'),
        ('cars_and_transit', 'Cars/Transit'),
        ('consumption_accounts', 'Consumption Accounts'),
        ('criminal_record', 'Criminal Record'),
        ('debt_certificates', 'Debt Certificates'),
        ('international', 'International'),
        ('management', 'Management'),
        ('nfe_and_nfse', 'NF-e / NFS-e'),
        ('processes', 'Processes'),
        ('taxes', 'Taxes'),
    )

    name = models.CharField(max_length=150, unique=True)
    client = models.ForeignKey(
        Client, on_delete=models.DO_NOTHING, null=True, blank=True, db_index=True)
    display_name_pt_br = models.CharField(
        max_length=150, null=True, blank=True)
    display_name_en = models.CharField(
        max_length=150, null=True, blank=True)
    display_name_es = models.CharField(
        max_length=150, null=True, blank=True)
    type = models.CharField(max_length=150, choices=TYPES,
                            default="upload")
    group = models.CharField(
        max_length=150, choices=GROUPS, default="management")
    active = models.BooleanField(default=True)
    is_showcase = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name

    def get_name(self):
        return self.name

    def get_is_showcase(self):
        return self.is_showcase

    def get_automations_with_ui(language, client, column=None):
        if column:
            cache_key = f"automations_column_{column}_{str(client.id)}"
        else:
            cache_key = f"automations_{str(client.id)}"

        cached_value = cache.get(cache_key)

        if cached_value and not settings.IS_LOCALHOST:
            return cached_value

        automations = [
            {
                'name': 'afip-argentina',
                'display_name_pt_br': 'Consulta de Retenção de Segurança Social',
                'display_name_en': 'Social Security Withholding Consultation',
                'display_name_es': 'Consulta de Retenciones del Seguro Social',
                'type': 'upload_and_credential',
                'group': 'international',
            },
            {
                'name': 'agip-argentina',
                'display_name_pt_br': 'Registro de Regimes Gerais | AGIP',
                'display_name_en': 'Registration of General Regimes | AGIP',
                'display_name_es': 'Registro de Regímenes Generales | AGIP',
                'type': 'upload',
                'group': 'international',
            },
            {
                'name': 'aguas-rio',
                'display_name_pt_br': 'Emissão de Contas de Água | Águas do Rio',
                'display_name_en': 'Issuance of Water Bills | river waters',
                'display_name_es': 'Emisión de Facturas de Agua | aguas del rio',
                'type': 'upload',
                'group': 'consumption_accounts',
            },
            {
                'name': 'antecedentes-federal',
                'display_name_pt_br': 'Verificação de Antecedentes Criminais | Brasil',
                'display_name_en': 'Criminal Background Check | Brazil',
                'display_name_es': 'Verificación de antecedentes penales | Brasil',
                'type': 'upload',
                'group': 'criminal_record',
            },
            {
                'name': 'antecedentes-rj',
                'display_name_pt_br': 'Verificação de Antecedentes Criminais | RJ',
                'display_name_en': 'Criminal Background Check | RJ',
                'display_name_es': 'Verificación de antecedentes penales | RJ',
                'type': 'upload',
                'group': 'criminal_record',
            },
            {
                'name': 'antecedentes-sp',
                'display_name_pt_br': 'Verificação de Antecedentes Criminais | SP',
                'display_name_en': 'Criminal Background Check | SP',
                'display_name_es': 'Verificación de antecedentes penales | SP',
                'type': 'upload',
                'group': 'criminal_record',
            },
            {
                'name': 'anvisa',
                'display_name_pt_br': 'Consulta de Processos | ANVISA',
                'display_name_en': 'Process Consultation | ANVISA',
                'display_name_es': 'Consulta de Procesos | ANVISA',
                'type': 'upload',
                'group': 'processes',
            },
            {
                'name': 'arba-argentina',
                'display_name_pt_br': 'Consulta do Registo do Regime de Cobrança - Alíquota por Assunto | ARBA',
                'display_name_en': 'Consultation of the Registration of the Collection Scheme - Rate by Subject | ARBA',
                'display_name_es': 'Consulta del Registro del Régimen de Recaudación - Tarifa por Materia | ARBA',
                'type': 'upload_and_credential',
                'group': 'international',
            },
            {
                'name': 'carf',
                'display_name_pt_br': 'Consulta de Processos | CARF',
                'display_name_en': 'Process Consultation | CARF',
                'display_name_es': 'Consulta de Procesos | CARF',
                'type': 'upload',
                'group': 'processes',
            },
            {
                'name': 'cedae',
                'display_name_pt_br': 'Emissão de Contas de Água | CEDAE',
                'display_name_en': 'Issuance of Water Bills | CEDAE',
                'display_name_es': 'Emisión de Facturas de Agua | CEDAE',
                'type': 'upload',
                'group': 'consumption_accounts',
            },
            {
                'name': 'cemig',
                'display_name_pt_br': 'Emissão de Contas de Energia | CEMIG',
                'display_name_en': 'Issuance of Energy Bills | CEMIG',
                'display_name_es': 'Emisión de Facturas de Energía | CEMIG',
                'type': 'credential',
                'group': 'consumption_accounts',
            },
            {
                'name': 'cepom-rj',
                'display_name_pt_br': 'Verificação de Situação Cadastral no CEPOM | Rio de Janeiro',
                'display_name_en': 'Verification of Registration Status at CEPOM | Rio de Janeiro',
                'display_name_es': 'Verificación del Estado de Registro en CEPOM | Rio de Janeiro',
                'type': 'upload',
                'group': 'cadastral_status',
            },
            {
                'name': 'certidao-mte',
                'display_name_pt_br': 'Emissão Certidão de Débitos Trabalhistas | MTE-SIT',
                'display_name_en': 'Issuance of Labor Debt Certificate | MTE-SIT',
                'display_name_es': 'Emisión de Certificado de Deuda Laboral | MTE-SIT',
                'type': 'upload',
                'group': 'debt_certificates',
            },
            {
                'name': 'claro',
                'display_name_pt_br': 'Emissão de Contas de Telefone | Claro',
                'display_name_en': 'Issuance of Telephone Bills | Claro',
                'display_name_es': 'Emisión de Facturas Telefónicas | Claro',
                'type': 'credential',
                'group': 'consumption_accounts',
            },
            {
                'name': 'cnd',
                'display_name_pt_br': 'Emissão de CND | Receita Federal',
                'display_name_en': 'CND issuance | IRS',
                'display_name_es': 'Emisión de CND | Receta Federal',
                'type': 'upload',
                'group': 'debt_certificates',
            },
            {
                'name': 'cnd-bahia',
                'display_name_pt_br': 'Emissão de CND | BA',
                'display_name_en': 'CND issuance | BA',
                'display_name_es': 'Emisión de CND | BA',
                'type': 'upload',
                'group': 'debt_certificates',
            },
            {
                'name': 'cnd-bocaina',
                'display_name_pt_br': 'Emissão de CND | Bocaina',
                'display_name_en': 'CND issuance | Bocaina',
                'display_name_es': 'Emisión de CND | Bocaina',
                'type': 'upload',
                'group': 'debt_certificates',
            },
            {
                'name': 'cnd-ce',
                'display_name_pt_br': 'Emissão de CND | CE',
                'display_name_en': 'CND issuance | CE',
                'display_name_es': 'Emisión de CND | CE',
                'type': 'upload',
                'group': 'debt_certificates',
            },
            {
                'name': 'cnd-fgts',
                'display_name_pt_br': 'Emissão do Certificado de Regularidade | FGTS',
                'display_name_en': 'Issuance of the Certificate of Regularity | FGTS',
                'display_name_es': 'Emisión del Certificado de Regularidad | FGTS',
                'type': 'upload',
                'group': 'debt_certificates',
            },
            {
                'name': 'cnd-fortaleza',
                'display_name_pt_br': 'Emissão de CND | Fortaleza',
                'display_name_en': 'CND issuance | Fortaleza',
                'display_name_es': 'Emisión de CND | Fortaleza',
                'type': 'upload',
                'group': 'debt_certificates',
            },
            {
                'name': 'cnd-mg',
                'display_name_pt_br': 'Emissão de CND | MG',
                'display_name_en': 'CND issuance | MG',
                'display_name_es': 'Emisión de CND | MG',
                'type': 'upload',
                'group': 'debt_certificates',
            },
            {
                'name': 'cnd-pe',
                'display_name_pt_br': 'Emissão de CND | PE',
                'display_name_en': 'CND issuance | PE',
                'display_name_es': 'Emisión de CND | PE',
                'type': 'upload',
                'group': 'debt_certificates',
            },
            {
                'name': 'cnd-rj',
                'display_name_pt_br': 'Emissão de CND | RJ',
                'display_name_en': 'CND issuance | RJ',
                'display_name_es': 'Emisión de CND | RJ',
                'type': 'upload',
                'group': 'debt_certificates',
            },
            {
                'name': 'cnd-sp',
                'display_name_pt_br': 'Emissão de CND | SP',
                'display_name_en': 'CND issuance | SP',
                'display_name_es': 'Emisión de CND | SP',
                'type': 'upload',
                'group': 'debt_certificates',
            },
            {
                'name': 'comgas',
                'display_name_pt_br': 'Emissão de Contas de Gás | Comgás',
                'display_name_en': 'Issuance of Gas Bills | Comgás',
                'display_name_es': 'Emisión de Facturas de Gas | Comgás',
                'type': 'upload',
                'group': 'consumption_accounts',
            },
            {
                'name': 'comprot',
                'display_name_pt_br': 'Consulta de Processos | COMPROT',
                'display_name_en': 'Process Consultation | COMPROT',
                'display_name_es': 'Consulta de Procesos | COMPROT',
                'type': 'upload',
                'group': 'processes',
            },
            {
                'name': 'conciliacao-bancaria',
                'display_name_pt_br': 'Consulta Conciliação Bancária | Interna',
                'display_name_en': 'Bank Reconciliation Consultation | internal',
                'display_name_es': 'Consulta de Conciliación Bancaria | Interno',
                'type': 'credential',
                'group': 'banking',
                'is_showcase': True,
            },
            {
                'name': 'consulta-antt-rntrc',
                'display_name_pt_br': 'Consulta Pública de Transportadores | ANTT',
                'display_name_en': 'Public Consultation of Transporters | ANTT',
                'display_name_es': 'Consulta Pública de Transportistas | ANTT',
                'type': 'upload',
                'group': 'cars_and_transit',
            },
            {
                'name': 'copasa',
                'display_name_pt_br': 'Emissão de Contas de Água | Copasa',
                'display_name_en': 'Issuance of Water Bills | Copasa',
                'display_name_es': 'Emisión de Facturas de Agua | Copasa',
                'type': 'credential',
                'group': 'consumption_accounts',
            },
            {
                'name': 'coren-rj',
                'display_name_pt_br': 'Verificação de Situação Cadastral COREN | RJ',
                'display_name_en': 'Verification of Cadastral Status COREN | RJ',
                'display_name_es': 'Verificación del estado de registro COREN | RJ',
                'type': 'upload',
                'group': 'cadastral_status',
            },
            {
                'name': 'correios',
                'display_name_pt_br': 'Monitoramento de Entregas | Correios',
                'display_name_en': 'Delivery Monitoring | Correios',
                'display_name_es': 'Monitoreo de entrega | Correios',
                'type': 'upload',
                'group': 'management',
            },
            {
                'name': 'correios-cas',
                'display_name_pt_br': 'Emissão de Fatura Eletrônica | Correios',
                'display_name_en': 'Electronic Invoice Issue | Correios',
                'display_name_es': 'Emisión de Factura Electrónica | Correo',
                'type': 'credential',
                'group': 'management',
            },
            {
                'name': 'cpfl-paulista',
                'display_name_pt_br': 'Emissão de Contas de Energia | CPFL',
                'display_name_en': 'Issuance of Energy Bills | CPFL',
                'display_name_es': 'Emisión de Facturas de Energía | CPFL',
                'type': 'upload',
                'group': 'consumption_accounts',
            },
            {
                'name': 'cpom-sp',
                'display_name_pt_br': 'Verificação de Situação Cadastral no CPOM | São Paulo',
                'display_name_en': 'Verification of Cadastral Status on CPOM | Sao Paulo',
                'display_name_es': 'Verificación del estado de registro en CPOM | San Pablo',
                'type': 'upload',
                'group': 'cadastral_status',
            },
            {
                'name': 'cremerj',
                'display_name_pt_br': 'Verificação de Situação Cadastral | CREMERJ',
                'display_name_en': 'Verification of Cadastral Status | CREMERJ',
                'display_name_es': 'Verificación del estado de registro | CREMERJ',
                'type': 'upload',
                'group': 'cadastral_status',
            },
            {
                'name': 'dashboards-ecommerce',
                'display_name_pt_br': 'Dashboard | Controle de Estoque',
                'display_name_en': 'Dashboard | Inventory control',
                'display_name_es': 'Tablero | Control de inventario',
                'type': 'credential',
                'group': 'management',
                'is_showcase': True,
            },
            {
                'name': 'decretos-portarias',
                'display_name_pt_br': 'Consulta de Decretos e Portarias',
                'display_name_en': 'Consultation of Decrees and Ordinances',
                'display_name_es': 'Consulta de Decretos y Ordenanzas',
                'type': 'credential',
                'group': 'processes',
                'is_showcase': True,
            },
            {
                'name': 'der',
                'display_name_pt_br': 'Consulta de Infrações de Transito | DER SP',
                'display_name_en': 'Traffic Infractions Inquiry | DER SP',
                'display_name_es': 'Consulta de Infracciones de Tránsito | DER SP',
                'type': 'upload',
                'group': 'cars_and_transit',
            },
            {
                'name': 'divida-ativa-mg',
                'display_name_pt_br': 'Consulta e Regulamentação de Dívida Ativa | MG',
                'display_name_en': 'Consultation and Regulation of Active Debt | MG',
                'display_name_es': 'Consulta y Regulación de Deuda Activa | MG',
                'type': 'upload',
                'group': 'debt_certificates',
            },
            {
                'name': 'divida-ativa-rj',
                'display_name_pt_br': 'Consulta e Regulamentação de Dívida Ativa | RJ',
                'display_name_en': 'Consultation and Regulation of Active Debt | RJ',
                'display_name_es': 'Consulta y Regulación de Deuda Activa | RJ',
                'type': 'upload',
                'group': 'debt_certificates',
            },
            {
                'name': 'divida-ativa-sp',
                'display_name_pt_br': 'Consulta e Regulamentação de Dívida Ativa | SP',
                'display_name_en': 'Consultation and Regulation of Active Debt | SP',
                'display_name_es': 'Consulta y Regulación de Deuda Activa | SP',
                'type': 'upload',
                'group': 'debt_certificates',
            },
            {
                'name': 'edp-brasil',
                'display_name_pt_br': 'Emissão de Contas de Energia | EDP',
                'display_name_en': 'Issuance of Energy Bills | EDP',
                'display_name_es': 'Emisión de Facturas de Energía | EDP',
                'type': 'credential',
                'group': 'consumption_accounts',
            },
            {
                'name': 'elektro',
                'display_name_pt_br': 'Emissão de Contas de Energia | Elektro',
                'display_name_en': 'Issuance of Energy Bills | Elektro',
                'display_name_es': 'Emisión de Facturas de Energía | Elektro',
                'type': 'credential',
                'group': 'consumption_accounts',
            },
            {
                'name': 'embratel',
                'display_name_pt_br': 'Emissão de Contas de Internet | Embratel',
                'display_name_en': 'Issuance of Internet Accounts | Embratel',
                'display_name_es': 'Emisión de Cuentas Internet | Embratel',
                'type': 'credential',
                'group': 'consumption_accounts',
            },
            {
                'name': 'enel-sp',
                'display_name_pt_br': 'Emissão de Contas de Energia | Enel',
                'display_name_en': 'Issuance of Energy Bills | Enel',
                'display_name_es': 'Emisión de Facturas de Energía | Enel',
                'type': 'credential',
                'group': 'consumption_accounts',
            },
            {
                'name': 'energisa',
                'display_name_pt_br': 'Emissão de Contas de Energia | Energisa',
                'display_name_en': 'Issuance of Energy Bills | Energisa',
                'display_name_es': 'Emisión de Facturas de Energía | Energisa',
                'type': 'credential',
                'group': 'consumption_accounts',
            },
            {
                'name': 'extrato-bancario',
                'display_name_pt_br': 'Emissão de Extrato Bancário',
                'display_name_en': 'Issuance of Bank Statement',
                'display_name_es': 'Emisión de Extracto Bancario',
                'type': 'credential',
                'group': 'banking',
            },
            {
                'name': 'gnre-rj',
                'display_name_pt_br': 'Emissão de GNRE | Todos os estados (exceto ES e SP)',
                'display_name_en': 'Issue of GNRE | All states (except ES and SP)',
                'display_name_es': 'Emisión de GNRE | Todos los estados (excepto ES y SP)',
                'type': 'upload',
                'group': 'taxes',
            },
            {
                'name': 'gnre-sp',
                'display_name_pt_br': 'Emissão de GNRE | SP',
                'display_name_en': 'Issue of GNRE | SP',
                'display_name_es': 'Emisión de GNRE | SP',
                'type': 'upload',
                'group': 'taxes',
            },
            {
                'name': 'ibama',
                'display_name_pt_br': 'Emissão de CND | IBAMA',
                'display_name_en': 'CND issuance | IBAMA',
                'display_name_es': 'Emisión de CND | IBAMA',
                'type': 'upload',
                'group': 'debt_certificates',
            },
            {
                'name': 'icms-alagoas',
                'display_name_pt_br': 'Emissão de Guia de ICMS | AL',
                'display_name_en': 'Issuance of ICMS Guide | AL',
                'display_name_es': 'Emisión de Guía ICMS | AL',
                'type': 'upload',
                'group': 'taxes',
            },
            {
                'name': 'icms-ce',
                'display_name_pt_br': 'Emissão de Guia de ICMS | CE',
                'display_name_en': 'Issuance of ICMS Guide | CE',
                'display_name_es': 'Emisión de Guía ICMS | CE',
                'type': 'upload',
                'group': 'taxes',
            },
            {
                'name': 'icms-mg',
                'display_name_pt_br': 'Emissão de Guia de ICMS | MG',
                'display_name_en': 'Issuance of ICMS Guide | MG',
                'display_name_es': 'Emisión de Guía ICMS | MG',
                'type': 'upload',
                'group': 'taxes',
            },
            {
                'name': 'icms-pe',
                'display_name_pt_br': 'Emissão de Guia de ICMS | PE',
                'display_name_en': 'Issuance of ICMS Guide | PE',
                'display_name_es': 'Emisión de Guía ICMS | PE',
                'type': 'upload',
                'group': 'taxes',
            },
            {
                'name': 'icms-pr',
                'display_name_pt_br': 'Emissão de Guia de ICMS | PR',
                'display_name_en': 'Issuance of ICMS Guide | PR',
                'display_name_es': 'Emisión de Guía ICMS | PR',
                'type': 'upload',
                'group': 'taxes',
            },
            {
                'name': 'icms-pa',
                'display_name_pt_br': 'Emissão de Guia de ICMS | PA',
                'display_name_en': 'Issuance of ICMS Guide | PA',
                'display_name_es': 'Emisión de Guía ICMS | PA',
                'type': 'upload',
                'group': 'taxes',
            },
            {
                'name': 'icms-sc',
                'display_name_pt_br': 'Emissão de Guia de ICMS | SC',
                'display_name_en': 'Issuance of ICMS Guide | SC',
                'display_name_es': 'Emisión de Guía ICMS | SC',
                'type': 'upload',
                'group': 'taxes',
            },
            {
                'name': 'icms-sp',
                'display_name_pt_br': 'Emissão de Guia de ICMS | SP',
                'display_name_en': 'Issuance of ICMS Guide | SP',
                'display_name_es': 'Emisión de Guía ICMS | SP',
                'type': 'upload',
                'group': 'taxes',
            },
            {
                'name': 'icms-rj',
                'display_name_pt_br': 'Emissão de Guia de ICMS | RJ',
                'display_name_en': 'Issuance of ICMS Guide | RJ',
                'display_name_es': 'Emisión de Guía ICMS | RJ',
                'type': 'upload',
                'group': 'taxes',
            },
            {
                'name': 'icms-pi',
                'display_name_pt_br': 'Emissão de Guia de ICMS | PI',
                'display_name_en': 'Issuance of ICMS Guide | PI',
                'display_name_es': 'Emisión de Guía ICMS | PI',
                'type': 'upload',
                'group': 'taxes',
            },
            {
                'name': 'icms-df',
                'display_name_pt_br': 'Emissão de Guia de ICMS | Distrito Federal',
                'display_name_en': 'Issuance of ICMS Guide | Federal District',
                'display_name_es': 'Emisión de Guía ICMS | Distrito Federal',
                'type': 'upload',
                'group': 'taxes',
            },
            {
                'name': 'icms-to',
                'display_name_pt_br': 'Emissão de Guia de ICMS | TO',
                'display_name_en': 'Issuance of ICMS Guide | TO',
                'display_name_es': 'Emisión de Guía ICMS | TO',
                'type': 'upload',
                'group': 'taxes',
            },
            {
                'name': 'inidoneos',
                'display_name_pt_br': 'Emissão de Certidão de Inidôneos | TCU',
                'display_name_en': 'Issuance of Certificate of Inidôneos | TCU',
                'display_name_es': 'Emisión de Certificado de Inidóneos | TCU',
                'type': 'upload',
                'group': 'debt_certificates',
            },
            {
                'name': 'inidoneos-ceis',
                'display_name_pt_br': 'Emissão de Certidão de Inidôneos | CEIS',
                'display_name_en': 'Issuance of Certificate of Inidôneos | CEIS',
                'display_name_es': 'Emisión de Certificado de Inidóneos | CEIS',
                'type': 'upload',
                'group': 'debt_certificates',
            },
            {
                'name': 'integra-siafi',
                'display_name_pt_br': 'Administração Financeira do Tesouro Nacional | SIAFI',
                'display_name_en': 'National Treasury Financial Administration | SIAFI',
                'display_name_es': 'Administración Financiera del Tesoro Nacional | SIAFI',
                'type': 'credential',
                'group': 'management',
                'is_showcase': True,
            },
            {
                'name': 'ipva-rj',
                'display_name_pt_br': 'Emissão de Guia de IPVA | Detran RJ',
                'display_name_en': 'Issuance of IPVA Guide | detran RJ',
                'display_name_es': 'Emisión de Guía IPVA | detran RJ',
                'type': 'upload',
                'group': 'cars_and_transit',
            },
            {
                'name': 'ipva-sp',
                'display_name_pt_br': 'Emissão de Guia de IPVA | SP',
                'display_name_en': 'Issuance of IPVA Guide | SP',
                'display_name_es': 'Emisión de Guía IPVA | SP',
                'type': 'upload',
                'group': 'cars_and_transit',
            },
            {
                'name': 'iss-barcarena',
                'display_name_pt_br': 'Emissão de Guias ISS | Barcarena',
                'display_name_en': 'Issuance of ISS Guides | Barcarena',
                'display_name_es': 'Emisión de Guías ISS | Barcarena',
                'type': 'credential',
                'group': 'taxes',
            },
            {
                'name': 'iss-cabedelo',
                'display_name_pt_br': 'Emissão de Guias ISS | Cabedelo',
                'display_name_en': 'Issuance of ISS Guides | Cabedelo',
                'display_name_es': 'Emisión de Guías ISS | Cabedelo',
                'type': 'credential',
                'group': 'taxes',
            },
            {
                'name': 'iss-guaruja',
                'display_name_pt_br': 'Emissão de Guias ISS | Guarujá',
                'display_name_en': 'Issuance of ISS Guides | Guarujá',
                'display_name_es': 'Emisión de Guías ISS | Guarujá',
                'type': 'credential',
                'group': 'taxes',
            },
            {
                'name': 'iss-ipojuca',
                'display_name_pt_br': 'Emissão de Guias ISS | Ipojuca',
                'display_name_en': 'Issuance of ISS Guides | Ipojuca',
                'display_name_es': 'Emisión de Guías ISS | Ipojuca',
                'type': 'upload_and_credential',
                'group': 'taxes',
            },
            {
                'name': 'iss-ipojuca-wilson',
                'display_name_pt_br': 'Emissão de Guias ISS | Ipojuca',
                'display_name_en': 'Issuance of ISS Guides | Ipojuca',
                'display_name_es': 'Emisión de Guías ISS | Ipojuca',
                'type': 'credential',
                'group': 'taxes',
                'client': Client.objects.filter(name='Wilson Sons').first()
            },
            {
                'name': 'iss-maceio',
                'display_name_pt_br': 'Emissão de Guias ISS | Maceió',
                'display_name_en': 'Issuance of ISS Guides | Maceió',
                'display_name_es': 'Emisión de Guías ISS | Maceió',
                'type': 'credential',
                'group': 'taxes',
            },
            {
                'name': 'iss-niteroi',
                'display_name_pt_br': 'Emissão de Guias ISS | Niterói',
                'display_name_en': 'Issuance of ISS Guides | Niterói',
                'display_name_es': 'Emisión de Guías ISS | Niterói',
                'type': 'credential',
                'group': 'taxes',
            },
            {
                'name': 'iss-oriximina',
                'display_name_pt_br': 'Emissão de Guias ISS | Oriximiná',
                'display_name_en': 'Issuance of ISS Guides | Oriximiná',
                'display_name_es': 'Emisión de Guías ISS | Oriximiná',
                'type': 'credential',
                'group': 'taxes',
            },
            {
                'name': 'iss-rio-grande',
                'display_name_pt_br': 'Emissão de Guias ISS |  Rio Grande',
                'display_name_en': 'Issuance of ISS Guides |  Rio Grande',
                'display_name_es': 'Emisión de Guías ISS |  Rio Grande',
                'type': 'credential',
                'group': 'taxes',
            },
            {
                'name': 'iss-rj',
                'display_name_pt_br': 'Emissão de Guias ISS | Rio de Janeiro | Nota Carioca',
                'display_name_en': 'Issuance of ISS Guides |  Rio de Janeiro | Nota Carioca',
                'display_name_es': 'Emisión de Guías ISS |  Rio de Janeiro | Nota Carioca',
                'type': 'upload_and_credential',
                'group': 'taxes',
            },
            {
                'name': 'iss-rj-wilson',
                'display_name_pt_br': 'Emissão de Guias ISS | Rio de Janeiro',
                'display_name_en': 'Issuance of ISS Guides | Rio de Janeiro',
                'display_name_es': 'Emisión de Guías ISS | Rio de Janeiro',
                'type': 'credential',
                'group': 'taxes',
                'client': Client.objects.filter(name='Wilson Sons').first()
            },
            {
                'name': 'iss-salvador',
                'display_name_pt_br': 'Emissão de Guias ISS | Salvador',
                'display_name_en': 'Issuance of ISS Guides | Salvador',
                'display_name_es': 'Emisión de Guías ISS | Salvador',
                'type': 'credential',
                'group': 'taxes',
            },
            {
                'name': 'iss-santos',
                'display_name_pt_br': 'Emissão de Guias ISS | Santos',
                'display_name_en': 'Issuance of ISS Guides | Santos',
                'display_name_es': 'Emisión de Guías ISS | Santos',
                'type': 'credential',
                'group': 'taxes',
            },
            {
                'name': 'iss-santo-andre',
                'display_name_pt_br': 'Emissão de Guias ISS | Santo André',
                'display_name_en': 'Issuance of ISS Guides | Santo André',
                'display_name_es': 'Emisión de Guías ISS | Santo André',
                'type': 'credential',
                'group': 'taxes',
            },
            {
                'name': 'iss-sp',
                'display_name_pt_br': 'Emissão de Guias ISS | São Paulo',
                'display_name_en': 'Issuance of ISS Guides | Sao Paulo',
                'display_name_es': 'Emisión de Guías ISS | San Pablo',
                'type': 'upload_and_credential',
                'group': 'taxes',
            },
            {
                'name': 'itau',
                'display_name_pt_br': 'Emissão de Extrato Bancário | Itaú',
                'display_name_en': 'Issuance of Bank Statement | Itaú',
                'display_name_es': 'Emisión de Estado de Cuenta | Itaú',
                'type': 'credential',
                'group': 'banking',
                'is_showcase': True,
            },
            {
                'name': 'light',
                'display_name_pt_br': 'Emissão de Contas de Energia | Light',
                'display_name_en': 'Issuance of Energy Bills | Light',
                'display_name_es': 'Emisión de Facturas de Energía | Light',
                'type': 'credential',
                'group': 'consumption_accounts',
            },
            {
                'name': 'mpf',
                'display_name_pt_br': 'Consulta de Processos | MPF',
                'display_name_en': 'Process Consultation | MPF',
                'display_name_es': 'Consulta de Procesos | MPF',
                'type': 'upload',
                'group': 'processes',
            },
            {
                'name': 'naturgy',
                'display_name_pt_br': 'Emissão de Contas de Gás | Naturgy',
                'display_name_en': 'Issuance of Gas Bills | Naturgy',
                'display_name_es': 'Emisión de Facturas de Gas | Naturgy',
                'type': 'upload',
                'group': 'consumption_accounts',
            },
            {
                'name': 'nfe-receita-federal',
                'display_name_pt_br': 'Emissão de Notas Fiscais (NFS-e) | Receita Federal',
                'display_name_en': 'Issuance of Invoices (NFS-e) | IRS',
                'display_name_es': 'Emisión de Facturas (NFS-e) | Receta Federal',
                'type': 'credential',
                'group': 'nfe_and_nfse',
                'is_showcase': True,
            },
            {
                'name': 'nfse-londrina',
                'display_name_pt_br': 'Emissão de Notas Fiscais de Serviço (NFS-e) | Londrina',
                'display_name_en': 'Issue of Service Invoices (NFS-e) | Londrina',
                'display_name_es': 'Emisión de Facturas de Servicios (NFS-e) | Londrina',
                'type': 'upload_and_credential',
                'group': 'nfe_and_nfse',
            },
            {
                'name': 'nfse-maringa',
                'display_name_pt_br': 'Emissão de Notas Fiscais de Serviço (NFS-e) | Maringá',
                'display_name_en': 'Issue of Service Invoices (NFS-e) | Maringá',
                'display_name_es': 'Emisión de Facturas de Servicios (NFS-e)| Maringá',
                'type': 'credential_and_filter_notes',
                'group': 'nfe_and_nfse',
            },
            {
                'name': 'nibo',
                'display_name_pt_br': 'Emissão de Relatórios Contábeis | Nibo',
                'display_name_en': 'Issuance of Accounting Reports | Nibo',
                'display_name_es': 'Emisión de Informes Contables | Nibo',
                'type': 'credential',
                'group': 'nfe_and_nfse',
            },
            {
                'name': 'notas-servicos-rj',
                'display_name_pt_br': 'Emissão de Notas Fiscais de Serviço (NFS-e) | Rio de Janeiro',
                'display_name_en': 'Issue of Service Invoices (NFS-e) | Rio de Janeiro',
                'display_name_es': 'Emisión de Facturas de Servicios (NFS-e) | Rio de Janeiro',
                'type': 'credential_and_filter_notes',
                'group': 'nfe_and_nfse',
            },
            {
                'name': 'notas-servico-sp',
                'display_name_pt_br': 'Emissão de Notas Fiscais de Serviço (NFS-e) | São Paulo',
                'display_name_en': 'Issue of Service Invoices (NFS-e) | Sao Paulo',
                'display_name_es': 'Emisión de Facturas de Servicios (NFS-e) | San Pablo',
                'type': 'upload',
                'group': 'nfe_and_nfse',
            },
            {
                'name': 'omie',
                'display_name_pt_br': 'Lançamento de Contas a Pagar | OMIE',
                'display_name_en': 'Launching Accounts Payable | OMIE',
                'display_name_es': 'Lanzamiento de Cuentas por Pagar | OMIE',
                'type': 'credential',
                'group': 'management',
            },
            {
                'name': 'oi',
                'display_name_pt_br': 'Emissão de Contas de Telefone | Oi',
                'display_name_en': 'Issuance of Telephone Bills | Oi',
                'display_name_es': 'Emisión de Facturas Telefónicas | Oi',
                'type': 'credential',
                'group': 'consumption_accounts',
            },
            {
                'name': 'processamento-documentos',
                'display_name_pt_br': 'Processamento Visual de Documentos',
                'display_name_en': 'Visual Document Processing',
                'display_name_es': 'Procesamiento de documentos visuales',
                'type': 'credential',
                'group': 'management',
                'is_showcase': True,
            },
            {
                'name': 'receita-federal-cpf',
                'display_name_pt_br': 'Verificação de Situação Cadastral de CPFs | Receita Federal',
                'display_name_en': 'Verification of CPF Registration Status | IRS',
                'display_name_es': 'Verificación del estado de registro de CPF | Receta Federal',
                'type': 'upload',
                'group': 'cadastral_status',
            },
            {
                'name': 'receita-federal-cnpj',
                'display_name_pt_br': 'Verificação de Situação Cadastral de CNPJs | Receita Federal',
                'display_name_en': 'Verification of CNPJ Registration Status | IRS',
                'display_name_es': 'Verificación del estado de registro de CNPJ | Receta Federal',
                'type': 'upload',
                'group': 'cadastral_status',
            },
            {
                'name': 'sabesp',
                'display_name_pt_br': 'Emissão de Contas de Água | Sabesp',
                'display_name_en': 'Issuance of Water Bills | Sabesp',
                'display_name_es': 'Emisión de Facturas de Agua | Sabesp',
                'type': 'upload',
                'group': 'consumption_accounts',
            },
            {
                'name': 'santander',
                'display_name_pt_br': 'Emissão de Extrato Bancário | Santander',
                'display_name_en': 'Issuance of Bank Statement | Santander',
                'display_name_es': 'Emisión de Estado de Cuenta | Santander',
                'type': 'credential',
                'group': 'banking',
                'is_showcase': True,
            },
            {
                'name': 'sefaz-rj',
                'display_name_pt_br': 'Declaração e Emissão de ITD | Sefaz RJ',
                'display_name_en': 'ITD Declaration and Issuance | Sefaz RJ',
                'display_name_es': 'Declaración y Emisión de ITD | Sefaz RJ',
                'type': 'upload_and_credential',
                'group': 'taxes',
            },
            {
                'name': 'shopee',
                'display_name_pt_br': 'Pesquisa e Monitoramento de preços | SHOPEE',
                'display_name_en': 'Price Research and Monitoring | SHOPEE',
                'display_name_es': 'Investigación y seguimiento de precios | SHOPEE',
                'type': 'upload',
                'group': 'management',
            },
            {
                'name': 'simples-nacional',
                'display_name_pt_br': 'Verificação de Situação Cadastral | Simples Nacional',
                'display_name_en': 'Verification of Registration Status | Simples Nacional',
                'display_name_es': 'Verificación del estado de registro | Simples Nacional',
                'type': 'upload',
                'group': 'cadastral_status',
            },
            {
                'name': 'sintegra-sc',
                'display_name_pt_br': 'Verificação de Situação Cadastral | SINTEGRA-SC',
                'display_name_en': 'Verification of Registration Status | SINTEGRA-SC',
                'display_name_es': 'Verificación del estado de registro | SINTEGRA-SC',
                'type': 'credential',
                'group': 'cadastral_status',
                'is_showcase': True,
            },
            {
                'name': 'solicitacao-notas-fiscais',
                'display_name_pt_br': 'Solicitação de Envio de Notas Ficais | Fornecedores e Prestadores',
                'display_name_en': 'Request for Sending Invoices | Suppliers and Providers',
                'display_name_es': 'Solicitud de Envío de Facturas | Proveedores',
                'type': 'upload',
                'group': 'nfe_and_nfse',
            },
            {
                'name': 'stone',
                'display_name_pt_br': 'Extrato de vendas | Stone',
                'display_name_en': 'Sales Extract | Stone',
                'display_name_es': 'Extracto de ventas | Stone',
                'type': 'credential',
                'group': 'management',
                'is_showcase': True,
            },
            {
                'name': 'tj-rj',
                'display_name_pt_br': 'Consulta de Processos | TJRJ',
                'display_name_en': 'Process Consultation | TJRJ',
                'display_name_es': 'Consulta de Procesos | TJRJ',
                'type': 'upload',
                'group': 'processes',
            },
            {
                'name': 'tj-sp',
                'display_name_pt_br': 'Consulta de Processos | TJSP',
                'display_name_en': 'Process Consultation | TJSP',
                'display_name_es': 'Consulta de Procesos | TJSP',
                'type': 'upload',
                'group': 'processes',
            },
            {
                'name': 'trf2',
                'display_name_pt_br': 'Emissão de Certidão | TRF2',
                'display_name_en': 'Certificate Issuance | TRF2',
                'display_name_es': 'Emisión de Certificados | TRF2',
                'type': 'upload',
                'group': 'debt_certificates',
            },
            {
                'name': 'trf3',
                'display_name_pt_br': 'Emissão de Certidão | TRF3',
                'display_name_en': 'Certificate Issuance | TRF3',
                'display_name_es': 'Emisión de Certificados | TRF3',
                'type': 'upload',
                'group': 'debt_certificates',
            },
            {
                'name': 'vivo',
                'display_name_pt_br': 'Emissão de Contas de Telefone | Vivo',
                'display_name_en': 'Issuance of Telephone Bills | Vivo',
                'display_name_es': 'Emisión de Facturas Telefónicas | Vivo',
                'type': 'credential',
                'group': 'consumption_accounts',
            },
        ]

        automations_with_ui_ids = set()
        for automation in automations:
            automation_name = automation.get('name')
            automation_client = automation.get('client', None)
            automation_display_name_pt_br = automation.get(
                'display_name_pt_br', '')
            automation_display_name_en = automation.get('display_name_en', '')
            automation_display_name_es = automation.get('display_name_es', '')
            automation_type = automation.get('type')
            automation_group = automation.get('group')
            automation_is_active = automation.get('active', True)
            automation_is_showcase = automation.get('is_showcase', False)

            automation_obj, created = Automation.objects.update_or_create(name=automation_name, defaults={
                'client': automation_client,
                'display_name_pt_br': automation_display_name_pt_br,
                'display_name_en': automation_display_name_en,
                'display_name_es': automation_display_name_es,
                'type': automation_type,
                'group': automation_group,
                'active': automation_is_active,
                'is_showcase': automation_is_showcase,

            })

            if automation_client:
                if automation_client == client or client.name == 'Smarthis':
                    automations_with_ui_ids.add(automation_obj.id)
                    name_without_client = "-".join(
                        automation_name.split('-')[:-1])

                    if client.name != 'Smarthis':
                        try:
                            automations_with_ui_ids.remove(name_without_client)
                        except KeyError:
                            pass
            else:
                automations_with_ui_ids.add(automation_obj.id)

        if column:
            data = Automation.objects.filter(pk__in=automations_with_ui_ids).order_by(
                '-active', 'is_showcase', f"display_name_{language.replace('-', '_').lower()}").values(column)
        else:
            data = Automation.objects.filter(pk__in=automations_with_ui_ids).order_by(
                '-active', 'is_showcase', f"display_name_{language.replace('-', '_').lower()}")

        cache.set(cache_key, data, 10800)   # 3 hours
        return data


class FutureAutomation(models.Model):
    name = models.CharField(max_length=150, unique=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    def get_name(self):
        return self.name


class InterestedInServiceUnderMaintenance(models.Model):
    automation = models.ForeignKey(Automation, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self) -> str:
        return self.automation.name


class Schedule(models.Model):
    class Meta:
        unique_together = [['user', 'automation', 'name']]

    SCHEDULE_STATES = (
        (1, 'IDDLE'),
        (2, 'RUNNING'),
        (3, 'FAULTED'),
    )

    APPOINTMENTS_RECURRENCE = (
        (0, 'WITHOUT-REPEAT'),
        (30, 'MONTHLY'),
        (7, 'WEEKLY'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    client = models.ForeignKey('subscriptions.Client',
                               on_delete=models.CASCADE, default=1)
    automation = models.ForeignKey(Automation, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    input_path = models.CharField(max_length=500, null=True, blank=True)
    attachments_path = models.CharField(max_length=500, null=True, blank=True)
    file_format = models.CharField(max_length=10, null=True, blank=True)
    state = models.PositiveSmallIntegerField(
        choices=SCHEDULE_STATES, default=1, blank=False)
    link_results = models.URLField(max_length=200, null=True, blank=True)
    email_to_send_results = models.TextField()
    cron_expression = models.CharField(max_length=30, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    execution_date = UnixDateTimeField(null=True, blank=True)
    # keeping recurrence to translate after
    recurrence = models.PositiveSmallIntegerField(
        choices=APPOINTMENTS_RECURRENCE, default=0, blank=True, null=True)
    output_files_in_pdf = models.BooleanField(
        null=True, blank=True, default=False)

    def __str__(self) -> str:
        return self.name

    def get_user(self):
        return self.user

    def get_client(self):
        return self.client

    def get_automation(self):
        return self.automation

    def set_updated_at(self, time):
        if isinstance(time, datetime):
            self.updated_at = time

    def get_cron_expression(self):
        return self.cron_expression

    def set_cron_expression(self, new_value):
        self.cron_expression = new_value

    def get_execution_date(self, format):
        response = self.execution_date
        if format:
            response = response.strftime(format)
        return response

    def set_execution_date(self, time):
        if isinstance(time, datetime):
            if time.tzinfo is None:
                brasa_timezone = pytz.timezone('America/Sao_Paulo')
                time = brasa_timezone.localize(time)
            self.execution_date = time
        elif time == None:
            self.execution_date = None

    def updateAllScheduleClients():
        def make_necessary_imports():
            from subscriptions.models import Profile
            dict = {
                'Profile': Profile}
            # Getting dot notation
            transformed_dict = SimpleNamespace(**dict)
            return transformed_dict

        all_schedules = Schedule.objects.all()
        imports = make_necessary_imports()
        for schedule in all_schedules:
            if schedule.client.id == 1:
                try:
                    profile = imports.Profile.objects.get(user=schedule.user)
                    schedule.client = profile.client
                    schedule.save()
                except Exception as e:
                    print(str(e))


class ScheduleExtraInfos(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    extra_info = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self) -> str:
        return self.schedule.name


class Task(models.Model):
    TASK_STATES = (
        (1, 'IDDLE'),
        (2, 'READY'),
        (3, 'PROCESSING'),
        (4, 'FAULTED'),
        (5, 'CANCELED'),
        (6, 'FINISHED'),
        (7, 'RESULTS SENT')
    )

    # preserve all registered tasks if an schedule is deleted
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    state = models.PositiveSmallIntegerField(
        choices=TASK_STATES, default=1, blank=False)
    number_of_rows = models.IntegerField(default=0, null=False, blank=False)
    number_of_successfull_rows = models.IntegerField(
        default=0, null=False, blank=False)
    source = models.CharField(
        max_length=300, null=False, blank=False, default='FRONT')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    scheduled_for = models.DateTimeField(null=True, default=None)

    def __str__(self) -> str:
        return f'{self.schedule.name} | {self.state}'

    def get_schedule(self):
        return self.schedule

    def get_created_at(self):
        return self.created_at

    def get_updated_at(self):
        return self.updated_at


class CaptchaUsage(models.Model):
    origin = models.CharField(max_length=300, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.CharField(max_length=300, null=True, blank=True)
    saldo = models.DecimalField(
        decimal_places=5, max_digits=10, null=True, blank=True)
    custo = models.DecimalField(
        decimal_places=5, max_digits=10, null=True, blank=True)
    engine = models.CharField(
        max_length=300, null=True, blank=True, default='Not provided')
    from_email = models.CharField(max_length=100, null=True, blank=True)


class ICMSVivara(models.Model):
    status = models.CharField(max_length=255, null=True)
    num_capta = models.CharField(max_length=255, null=True)
    store = models.CharField(max_length=255, null=True)
    company = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    uf = models.CharField(max_length=255, null=True)
    cep = models.CharField(max_length=255, null=True)
    cnpj = models.CharField(max_length=255, null=True)
    insc_estadual = models.CharField(max_length=255, null=True)
    insc_municipal = models.CharField(max_length=255, null=True)
    responsible = models.CharField(max_length=255, null=True)
    receipt_code_icms = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'smt_orchestrator_icms_vivara'


class ICMSVivaraConfig(models.Model):
    uf = models.CharField(max_length=255, null=True, unique=True)
    qualification = models.CharField(max_length=255, null=True)
    expiration = models.CharField(max_length=255, null=True)
    icms_rule = models.CharField(max_length=255, null=True)
    receita_code = models.CharField(max_length=255, null=True)
    tipo_debito = models.CharField(max_length=255, null=True)
    codigo_operacao = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'smt_orchestrator_icms_vivara_config'


class ICMSVivaraRJ(models.Model):
    cnpj = models.CharField(max_length=255, null=True)
    qualification = models.CharField(max_length=255, null=True)
    reference_period = models.DateField(null=True)
    informed_icms = models.DecimalField(
        decimal_places=2, max_digits=16, null=True)
    informed_fecp = models.DecimalField(
        decimal_places=2, max_digits=16, null=True)

    class Meta:
        db_table = 'smt_orchestrator_icms_vivara_rj'
