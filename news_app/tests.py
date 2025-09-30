from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Publisher, Article, Newsletter, Roles

User = get_user_model()


class UserModelTests(TestCase):
    def test_user_creation_and_role_group(self):
        user = User.objects.create_user(username="reader1", password="pass123", role=Roles.READER)
        self.assertEqual(user.role, Roles.READER)
        self.assertTrue(user.groups.filter(name="Reader").exists())

    def test_journalist_following(self):
        journalist = User.objects.create_user(username="journalist1", password="pass123", role=Roles.JOURNALIST)
        reader = User.objects.create_user(username="reader2", password="pass123", role=Roles.READER)
        reader.reader_subscriptions_journalists.add(journalist)
        self.assertIn(journalist, reader.reader_subscriptions_journalists.all())


class PublisherModelTests(TestCase):
    def test_publisher_creation(self):
        pub = Publisher.objects.create(name="Test News", description="A test publisher")
        self.assertEqual(str(pub), "Test News")


class ArticleModelTests(TestCase):
    def setUp(self):
        self.publisher = Publisher.objects.create(name="Daily Press")
        self.journalist = User.objects.create_user(username="journo", password="pass123", role=Roles.JOURNALIST)

    def test_article_creation(self):
        article = Article.objects.create(title="Breaking News", body="Content", publisher=self.publisher, journalist=self.journalist)
        self.assertEqual(str(article), "Breaking News")
        self.assertFalse(article.approved)


class NewsletterModelTests(TestCase):
    def setUp(self):
        self.publisher = Publisher.objects.create(name="Global News")
        self.journalist = User.objects.create_user(username="journo2", password="pass123", role=Roles.JOURNALIST)

    def test_newsletter_creation(self):
        newsletter = Newsletter.objects.create(subject="Weekly Update", body="Some text", publisher=self.publisher, journalist=self.journalist)
        self.assertEqual(str(newsletter), "Weekly Update")
        self.assertFalse(newsletter.approved)


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="pass123")

    def test_login_view(self):
        response = self.client.post(reverse("login"), {"username": "testuser", "password": "pass123"})
        self.assertEqual(response.status_code, 302)  # redirect on success

    def test_signup_view(self):
        response = self.client.post(reverse("signup"), {"username": "newuser", "password1": "pass12345", "password2": "pass12345"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())


class APITests(TestCase):
    def setUp(self):
        self.client = Client()
        self.publisher = Publisher.objects.create(name="API News")
        self.journalist = User.objects.create_user(username="apijourno", password="pass123", role=Roles.JOURNALIST)

    def test_article_api_create(self):
        self.client.force_login(self.journalist)
        response = self.client.post(reverse("article-list"), {
            "title": "API Article",
            "body": "API body",
            "publisher": self.publisher.id,
            "journalist": self.journalist.id
        })
        self.assertEqual(response.status_code, 201)

    def test_newsletter_api_create(self):
        self.client.force_login(self.journalist)
        response = self.client.post(reverse("newsletter-list"), {
            "subject": "API Newsletter",
            "body": "Body text",
            "publisher": self.publisher.id,
            "journalist": self.journalist.id
        })
        self.assertEqual(response.status_code, 201)
