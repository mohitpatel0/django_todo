from django.test import TestCase
from django.contrib.auth.models import User
import unittest
from django.urls import reverse
from todo.models import TaskData

class TestUpdateTask(TestCase):
    def setUp(self):

        self.task_id = '112'
        self.task_name = 'helo jivan ma'
        self.task_details ='detali of jivan'
        self.task_end_date ='2021-09-21'
        self.task_end_time ='07:38:14'

        self.credentials = {
            'username': 'supermo',
            'password': 'mohit123'}
        User.objects.create_user(**self.credentials)


    # def test_updatetask_page_url(self):
    #     response = self.client.post('/login/', self.credentials, follow=True)
    #     # should be logged in now
    #     self.assertTrue(response.context['user'].is_active)

    #     response = self.client.get(reverse('task-create'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, template_name='TaskData_form.html')

    def test_update_task(self):
        # send login data
        response = self.client.post('/login/', self.credentials, follow=True)
        # should be logged in now
        self.assertTrue(response.context['user'].is_active)
        #addtask
        response = self.client.post(reverse('task-create'), data={
            'task_id': self.task_id,
            'task_name': self.task_name,
            'task_details': self.task_details,
            'task_end_date': self.task_end_date,
            'task_end_time':self.task_end_time,
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/home/', status_code=302, 
        target_status_code=200, fetch_redirect_response=True)

        #update task
        data = TaskData.objects.all()
        for d in data :
            pk =d.pk 

        response = self.client.post(f'/taskdetail/{pk}/update', data={
            'task_id': self.task_id,
            'task_name': self.task_name,
            'task_details': "detail updated ",
            'task_end_date': self.task_end_date,
            'task_end_time':self.task_end_time,
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/home/', status_code=302, 
        target_status_code=200, fetch_redirect_response=True)



        #model have 1 taskdata
        tasks = TaskData.objects.all()
        self.assertEqual(tasks.count(), 1)






