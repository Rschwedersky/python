from django.test import TestCase

from dashboard.templatetags.dashboard_tags import generateJobsFromJson

from subscriptions.models import Client
from uipath_logs.models import Context, Job, Areas, Processos

from datetime import datetime
import os
import json


class JobTestCase(TestCase):
    def setUp(self):
        """ Populates DB before testing """
        name = 'client_test'
        client_test = Client.objects.create(name=name)
        Context.objects.create(customer=client_test, context='')

        # create_test_job_logs(name)

        new_areas = get_all_test_area_name()
        new_processes = [
            {'process': 'Process Test 1', 'releasename': 'BANCO_DOC_PROD02'},
            {'process': 'Process Test 2', 'releasename': 'BANCO_DOC_PROD03'},
            {'process': 'Process Test', 'releasename': 'BANCO_DOC_PROD01'},
        ]
        count = 0
        for new_area in new_areas:
            area_test = Areas.objects.create(
                area=new_area, customer=client_test)
            Processos.objects.create(process=new_processes[count]['process'], ReleaseName=new_processes[count]['releasename'], duration_time=30.0,
                                     area=area_test, salary_collaborator=1200.0, hours_collaborator=8, howmany_collaborators=2, project_cost=30000.0, client=client_test)
            count += 1

    def test_average_occupation_limit_60(self):
        date_from = datetime.strptime('2020-01-01', '%Y-%m-%d').date()
        date_to = datetime.today().date()
        client_test = Client.objects.get(name='client_test')
        json = Job.get_json_from_db(date_from, date_to, client_test)
        error = {}
        for date, item in json['dates'].items():
            for process_key, process in item['processes'].items():
                for track_day, infos in process['averageoccupation_byday'].items():
                    if (infos['total_occupation_byhour'] / 60) / infos['qnt'] > 60:
                        print(
                            date, track_day, (infos['total_occupation_byhour'] / 60), infos['qnt'])
                        error[process_key] = (
                            infos['total_occupation_byhour'] / 60) / infos['qnt']

        self.assertEqual(error, {})

    def test_creation_returned_json_correct_dates(self):
        date_from = datetime.strptime('2020-01-01', '%Y-%m-%d').date()
        date_to = datetime.today().date()
        final_json = Job.setJsonReturn(date_from, date_to)
        date_keys = list(final_json['dates'].keys())

        self.assertEqual(date_keys[0], date_from.strftime('%Y_%m_%d'))
        self.assertEqual(date_keys[len(date_keys) - 1],
                         date_to.strftime('%Y_%m_%d'))

        # check if objects inside test are correct
        self.assertEqual(final_json['dates'][date_keys[0]], {'processes': {}, 'robots': {
        }, 'areas': {}, 'status': {}, 'date': date_from.strftime('%Y-%m-%d')})

    def test_all_listed_columns(self):
        date_from = datetime.strptime('2020-01-01', '%Y-%m-%d').date()
        date_to = datetime.today().date()
        client_test = Client.objects.get(name='client_test')

        all_processes = Job.listAllColumnsTypes(
            date_from, date_to, 'processes', 'ReleaseName', client_test)
        error_process = False
        processes = []
        for p in all_processes:
            if p in processes:
                print(p)
                error_process = True
            else:
                processes.append(p)
        self.assertEqual(error_process, False)

        all_status = Job.listAllColumnsTypes(
            date_from, date_to, 'status', 'State', client_test)
        error_status = False
        status = []
        for single_status in all_status:
            if single_status in status:
                print(single_status)
                error_status = True
            else:
                status.append(single_status)
        self.assertEqual(error_status, False)

        all_robots = Job.listAllColumnsTypes(
            date_from, date_to, 'robots', 'HostMachineName', client_test)
        error_robots = False
        robots = []
        for single_robot in all_robots:
            if single_robot in robots:
                print(single_robot)
                error_robots = True
            else:
                robots.append(single_robot)
        self.assertEqual(error_robots, False)

    def test_all_areas_get(self):
        name_test = 'Area Test'
        area_test = Areas.objects.get(area=name_test)
        self.assertEqual(area_test.get_area_name(), name_test)

        client_test = Client.objects.get(name='client_test')
        self.assertEqual(area_test.get_customer(), client_test)

    def test_all_areas_listed_columns(self):
        # get listed columns for determined client and check if data is sorted correctly
        client_test = Client.objects.get(name='client_test')
        alltypes = Areas.listAllColumnsTypes(client_test)
        not_sorted_list = alltypes['areas']
        alltypes['areas'].sort()
        self.assertEqual(json.dumps(not_sorted_list),
                         json.dumps(alltypes['areas']))

    def test_all_get_processes(self):
        processes_infos = get_process_infos()

        self.assertEqual(
            processes_infos['process'].get_process(), processes_infos['name_process'])
        self.assertEqual(
            processes_infos['process'].get_ReleaseName(), 'BANCO_DOC_PROD01')
        self.assertEqual(processes_infos['process'].get_duration_time(), 30.0)
        area_test = Areas.objects.get(
            area='Area Test', customer=processes_infos['client_test'])
        self.assertEqual(processes_infos['process'].get_area(), area_test)
        self.assertEqual(
            processes_infos['process'].get_salary_collaborator(), 1200.0)
        self.assertEqual(
            processes_infos['process'].get_hours_collaborator(), 8)
        self.assertEqual(
            processes_infos['process'].get_howmany_collaborators(), 2)
        self.assertEqual(
            processes_infos['process'].get_project_cost(), 30000.0)
        self.assertEqual(
            processes_infos['process'].get_client(), processes_infos['client_test'])

    def test_all_set_processes(self):
        processes_infos = get_process_infos()
        test_infos = [
            {
                'is_empty': False,
                'new_process': 'Process Set Test',
                'new_releasename': 'BANCO_DOC_PROD04',
                'new_duration_time': 40.0,
                'new_client_area': Areas.objects.get(area='RH Test'),
                'new_salary_collaborator': 1100.0,
                'new_hours_collaborator': 6,
                'new_howmany_collaborators': 3,
                'new_project_cost': 32000.0,
                'new_client_test': Client.objects.create(name='Client Tested'),
            },
            {
                'is_empty': True,
                'new_process': '',
                'new_releasename': '',
                'new_duration_time': 0,
                'new_client_area': [],
                'new_salary_collaborator': 0,
                'new_hours_collaborator': 0,
                'new_howmany_collaborators': 0,
                'new_project_cost': 0,
                'new_client_test': [],
            }
        ]

        count = 0
        for test_group in test_infos:
            processes_infos['process'].set_process(test_group['new_process'])
            processes_infos['process'].set_ReleaseName(
                test_group['new_releasename'])
            processes_infos['process'].set_duration_time(
                test_group['new_duration_time'])
            processes_infos['process'].set_area(test_group['new_client_area'])
            processes_infos['process'].set_salary_collaborator(
                test_group['new_salary_collaborator'])
            processes_infos['process'].set_hours_collaborator(
                test_group['new_hours_collaborator'])
            processes_infos['process'].set_howmany_collaborators(
                test_group['new_howmany_collaborators'])
            processes_infos['process'].set_project_cost(
                test_group['new_project_cost'])
            processes_infos['process'].set_client(
                test_group['new_client_test'])

            processes_infos['process'].save()

            if test_group['is_empty']:
                self.assertEqual(processes_infos['process'].get_process(
                ), test_infos[count - 1]['new_process'])
                self.assertEqual(processes_infos['process'].get_ReleaseName(
                ), test_infos[count - 1]['new_releasename'])
                self.assertEqual(processes_infos['process'].get_duration_time(
                ), test_infos[count - 1]['new_duration_time'])
                self.assertEqual(processes_infos['process'].get_area(
                ), test_infos[count - 1]['new_client_area'])
                self.assertEqual(processes_infos['process'].get_salary_collaborator(
                ), test_infos[count - 1]['new_salary_collaborator'])
                self.assertEqual(processes_infos['process'].get_hours_collaborator(
                ), test_infos[count - 1]['new_hours_collaborator'])
                self.assertEqual(processes_infos['process'].get_howmany_collaborators(
                ), test_infos[count - 1]['new_howmany_collaborators'])
                self.assertEqual(processes_infos['process'].get_project_cost(
                ), test_infos[count - 1]['new_project_cost'])
                self.assertEqual(processes_infos['process'].get_client(
                ), test_infos[count - 1]['new_client_test'])
            else:
                self.assertEqual(
                    processes_infos['process'].get_process(), test_group['new_process'])
                self.assertEqual(
                    processes_infos['process'].get_ReleaseName(), test_group['new_releasename'])
                self.assertEqual(processes_infos['process'].get_duration_time(
                ), test_group['new_duration_time'])
                self.assertEqual(
                    processes_infos['process'].get_area(), test_group['new_client_area'])
                self.assertEqual(processes_infos['process'].get_salary_collaborator(
                ), test_group['new_salary_collaborator'])
                self.assertEqual(processes_infos['process'].get_hours_collaborator(
                ), test_group['new_hours_collaborator'])
                self.assertEqual(processes_infos['process'].get_howmany_collaborators(
                ), test_group['new_howmany_collaborators'])
                self.assertEqual(
                    processes_infos['process'].get_project_cost(), test_group['new_project_cost'])
                self.assertEqual(
                    processes_infos['process'].get_client(), test_group['new_client_test'])

            count += 1

    def test_all_processes_listed_columns(self):
        client_test = Client.objects.get(name='client_test')
        alltypes = Processos.listAllColumnsTypes(client_test)
        not_sorted_list = alltypes['dict']
        sorted_list = sorted(alltypes['dict'])
        sort_array = []
        comparing_array = []

        # creating array to compare if has diference on sort of model and
        for releasename in sorted_list:
            sort_array.append(alltypes['dict'][releasename])
        for key, sort in not_sorted_list.items():
            comparing_array.append(sort)

        self.assertEqual(json.dumps(comparing_array), json.dumps(sort_array))

    def test_get_processes_field(self):
        processes_infos = get_process_infos()
        all_fields = processes_infos['process'].get_fields()
        self.assertEqual(len(all_fields) > 0, True)

    def test_set_default_clients_from_area(self):
        all_test_areas = get_all_test_area_name()
        area_test = Areas.objects.get(area=all_test_areas[0])
        process_empty_area = Processos.objects.create(process=None, ReleaseName='BANCO_DOC_PROD_00', duration_time=None, area=area_test,
                                                      salary_collaborator=None, hours_collaborator=None, howmany_collaborators=None, project_cost=None, client=None)
        Processos.set_default_clients()
        self.assertEqual(process_empty_area.area.customer, area_test.customer)


def create_test_job_logs(name='client_test'):
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(
        module_dir + '/test_files', 'uipath_logs_job.json')
    with open(file_path, 'r') as f:
        jobs_json = json.load(f)
        for key, j in jobs_json.items():
            generateJobsFromJson(j, name)


def get_all_test_area_name():
    return ['RH Test', 'Financeiro Test', 'Area Test']


def get_process_infos():
    name_process = 'Process Test'
    client_test = Client.objects.get(name='client_test')
    process = Processos.objects.get(process=name_process, client=client_test)
    return {'name_process': name_process, 'client_test': client_test, 'process': process}
