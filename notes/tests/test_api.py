from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from notes.models import Note, Category

class NoteAPITests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')
        
        self.category1 = Category.objects.create(name='Cat1', owner=self.user1)
        self.category2 = Category.objects.create(name='Cat2', owner=self.user2)
        
        self.note1 = Note.objects.create(title='Note1', content='Content1', category=self.category1, owner=self.user1)
        self.note2 = Note.objects.create(title='Note2', content='Content2', category=self.category2, owner=self.user2)

    def test_list_categories(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Cat1')

    def test_create_category(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('category-list')
        data = {'name': 'New Cat'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 3)
        self.assertEqual(Category.objects.get(id=response.data['id']).owner, self.user1)

    def test_list_notes(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('note-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Note1')

    def test_create_note(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('note-list')
        data = {'title': 'New Note', 'content': 'New Content', 'category': self.category1.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Note.objects.count(), 3)
        self.assertEqual(Note.objects.get(id=response.data['id']).owner, self.user1)

    def test_unauthenticated_access(self):
        url = reverse('note-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_swagger_ui(self):
        url = reverse('schema-swagger-ui')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

