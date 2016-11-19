from utils.api.tests import APITestCase, APIClient


class AnnouncementAdminTest(APITestCase):
    def setUp(self):
        self.user = self.create_super_admin(login=True)
        self.url = self.reverse("announcement_admin_api")

    def test_announcement_list(self):
        response = self.client.get(self.url)
        self.assertSuccess(response)

    def create_announcement(self):
        return self.client.post(self.url, data={"title": "test", "content": "test"})

    def test_create_announcement(self):
        response = self.create_announcement()
        self.assertSuccess(response)

    def test_edit_announcement(self):
        data = {"id": self.create_announcement().data["data"]["id"], "title": "ahaha", "content": "test content",
                "visible": False}
        response = self.client.put(self.url, data=data)
        self.assertSuccess(response)
        resp_data = response.data["data"]
        self.assertEqual(resp_data["title"], "ahaha")
        self.assertEqual(resp_data["content"], "test content")
        self.assertEqual(resp_data["visible"], False)
