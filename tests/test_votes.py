import pytest
from app import models

@pytest.fixture()
def test_vote(test_posts, session, test_user):
    new_vote = models.Vote(post_id=test_posts[3].id, user_id=test_user['id'], direction=1)
    session.add(new_vote)
    session.commit()

def test_post_vote(auth_client, test_posts):
    res = auth_client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 1})
    assert res.status_code == 201

def test_delete_post_vote(auth_client, test_posts, test_vote):
    res = auth_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 0})
    assert res.status_code == 201

def test_post_vote_twice(auth_client, test_posts, test_vote):
    res = auth_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 409

def test_delete_post_vote_non_exist(auth_client, test_posts):
    res = auth_client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 0})
    assert res.status_code == 404

def test_post_vote_non_exist(auth_client, test_posts):
    res = auth_client.post("/vote/", json={"post_id": 69, "dir": 1})
    assert res.status_code == 404

def test_post_vote_unauth(client, test_posts):
    res = client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 1})
    assert res.status_code == 401