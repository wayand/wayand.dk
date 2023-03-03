from tests.base_test_case import BaseTestCase

class HomeCase(BaseTestCase):

    def test_home(self):
        response = self.app.test_client().get('/')
        assert response.status_code == 200
        assert b"<!DOCTYPE html>" in response.data
        assert b"Hi there !" in response.data
        assert b"I'm" in response.data
        assert b"wayand bahramzy" in response.data
        assert b"a Full-stack Web Developer" in response.data
    
    def test_about_me(self):
        response = self.app.test_client().get('/')
        assert response.status_code == 200
        assert b"<!DOCTYPE html>" in response.data
        assert b"about <span>me</span>" in response.data
    
    def test_portfolio(self):
        response = self.app.test_client().get('/')
        assert response.status_code == 200
        assert b"<!DOCTYPE html>" in response.data
        assert b"my <span>portfolio</span>" in response.data
    
    def test_contact(self):
        response = self.app.test_client().get('/')
        assert response.status_code == 200
        assert b"<!DOCTYPE html>" in response.data
        assert b"get <span>in touch</span>" in response.data
    
    def test_blog(self):
        response = self.app.test_client().get('/')
        assert response.status_code == 200
        assert b"<!DOCTYPE html>" in response.data
        assert b"latest <span>posts</span>" in response.data
