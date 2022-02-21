""" tests """

from django.contrib.auth.hashers import make_password
from django.test import TestCase
from django.urls import reverse

from apps.web.models import Bookmarks, BookmarkTags, Profile


class BookmarkTestCase(TestCase):
    """Test bookmark management"""

    def setUp(self):
        self.user1 = Profile.objects.create(
            username="tester1",
            password=make_password("asdf"),
            email="tester1@dubell.io",
            timezone="UTC",
        )
        self.user2 = Profile.objects.create(
            username="tester2",
            password=make_password("asdf"),
            email="tester2@dubell.io",
            timezone="UTC",
        )
        self.delete_bookmark = reverse("web:delete_bookmark")
        self.mark_read = reverse("web:mark_bookmark_read")

    def test_delete_bookmark(self):
        """Delete bookmark"""
        obj = Bookmarks.objects.create(user=self.user1)

        data = {"bm_id": obj.bm_id}
        self.client.force_login(self.user1)
        response = self.client.post(self.delete_bookmark, data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Bookmarks.objects.filter(bm_id=obj.bm_id).exists())

    def test_delete_bookmark_does_not_exist(self):
        """Delete a bookmark that does not exist"""
        obj = Bookmarks.objects.create(user=self.user1)

        data = {"bm_id": "1234"}
        self.client.force_login(self.user1)
        response = self.client.post(self.delete_bookmark, data, follow=True)

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Bookmarks.objects.all())

    def test_delete_other_user_bookmark(self):
        """Delete an other user's bookmark, should fail"""
        obj = Bookmarks.objects.create(user=self.user1)

        data = {"bm_id": obj.bm_id}
        self.client.force_login(self.user2)
        response = self.client.post(self.delete_bookmark, data, follow=True)

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Bookmarks.objects.all())

    def test_toggle_bookmark_read_true(self):
        """Mark bookmark as read"""
        obj = Bookmarks.objects.create(user=self.user1)

        data = {"bm_id": obj.bm_id}
        self.client.force_login(self.user1)
        response = self.client.post(self.mark_read, data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Bookmarks.objects.get(pk=obj.pk).read)

    def test_toggle_bookmark_read_false(self):
        """Mark bookmark as unread"""
        obj = Bookmarks.objects.create(user=self.user1, read=True)

        data = {"bm_id": obj.bm_id}
        self.client.force_login(self.user1)
        response = self.client.post(self.mark_read, data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Bookmarks.objects.get(pk=obj.pk).read)

    def test_toggle_other_user_bookmark_read(self):
        """Mark an other user's bookmark as read, should fail"""
        obj = Bookmarks.objects.create(user=self.user1, read=True)

        data = {"bm_id": obj.bm_id}
        self.client.force_login(self.user2)
        response = self.client.post(self.mark_read, data, follow=True)

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Bookmarks.objects.get(pk=obj.pk).read)

    def test_toggle_bookmark_does_not_exist(self):
        """Mark an other user's bookmark as read, should fail"""
        obj = Bookmarks.objects.create(user=self.user1, read=True)

        data = {"bm_id": "1234"}
        self.client.force_login(self.user1)
        response = self.client.post(self.mark_read, data, follow=True)

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Bookmarks.objects.all())

    def test_add_bookmark_tag(self):
        """Add tags to bookmark"""
        obj = Bookmarks.objects.create(user=self.user1)

        self.client.force_login(self.user1)
        url = reverse("web:add_bookmark_tag", kwargs={"bookmark_id": obj.bm_id})
        response = self.client.post(url, {"tag": "test-tag"})

        self.assertEqual(response.status_code, 201)
        self.assertTrue(Bookmarks.objects.filter(tags__name="test-tag"))

    def test_add_bookmark_tag_other_user(self):
        """It should not be possible to add tags for a bookmark belonging to an other user"""
        obj = Bookmarks.objects.create(user=self.user1)

        self.client.force_login(self.user2)
        url = reverse("web:add_bookmark_tag", kwargs={"bookmark_id": obj.bm_id})
        response = self.client.post(url, {"tag": "error"})

        self.assertEqual(response.status_code, 404)
        self.assertFalse(Bookmarks.objects.filter(tags__name="error"))

    def test_remove_bookmark_tag(self):
        """Remove tags from bookmark"""
        obj = Bookmarks.objects.create(user=self.user1)
        tag = BookmarkTags.objects.create(name="test-remove-tag")
        obj.tags.add(tag)
        obj.save()

        self.client.force_login(self.user1)
        url = reverse("web:add_bookmark_tag", kwargs={"bookmark_id": obj.bm_id})
        response = self.client.delete(url, "tag=test-remove-tag")

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Bookmarks.objects.filter(tags__name="test-remove-tag"))

    def test_remove_bookmark_tag_other_user(self):
        """It should not be possible to remove tags from a bookmark belonging to an other user"""
        obj = Bookmarks.objects.create(user=self.user1)
        tag = BookmarkTags.objects.create(name="test-remove-tag")
        obj.tags.add(tag)
        obj.save()

        self.client.force_login(self.user2)
        url = reverse("web:add_bookmark_tag", kwargs={"bookmark_id": obj.bm_id})
        response = self.client.delete(url, "tag=test-remove-tag")

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Bookmarks.objects.filter(tags__name="test-remove-tag"))
