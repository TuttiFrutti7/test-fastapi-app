import pytest
from app import schemas


def test_get_all_posts(auth_client, test_posts):
    res = auth_client.get("/posts/")

    def validate(post):
        return schemas.PostVote(**post)
    posts_map = map(validate, res.json())
    posts_list = list(posts_map)

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200
    assert posts_list[0].Post.id == test_posts[0].id

def test_get_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostVote(**res.json())
    assert res.status_code == 200
    assert post.Post.id == test_posts[0].id

def test_get_invalid_post(client, test_posts):
    res = client.get(f"/posts/39")
    assert res.status_code == 404

@pytest.mark.parametrize('title, content, published',[
    ('life', 'life is a flat circle', True),
    ('time', 'does time ever stop', True),
    ('private', 'my private post', False)
])
def test_create_post(auth_client, test_user, title, content, published):
    res = auth_client.post("/posts/", json={'title': title, 'content': content, 'published': published})
    post = schemas.PostResponse(**res.json())
    assert res.status_code == 201
    assert post.title == title
    assert post.owner_id == test_user['id']

def test_create_post_default_published(auth_client, test_user):
    res = auth_client.post("/posts/", json={'title': 'cheese', 'content': 'cheese is great'})
    post = schemas.PostResponse(**res.json())
    assert res.status_code == 201
    assert post.published == True
    assert post.owner_id == test_user['id']

def test_create_post_unauth(client, test_user):
    res = client.post("/posts/", json={'title': 'cheese', 'content': 'cheese is great'})
    assert res.status_code == 401

def test_unauth_delet_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_delete_post(auth_client, test_user, test_posts):
    res = auth_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

def test_delete_post_non_exist(auth_client, test_user, test_posts):
    res = auth_client.delete(f"/posts/69")
    assert res.status_code == 404

def test_delete_post_not_owned(auth_client, test_user, test_posts):
    res = auth_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403

def test_update_post(auth_client, test_user, test_posts):
    data = {
        'title': 'updated title',
        'content': 'updated content',
        'id': test_posts[0].id
    }
    res = auth_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.PostResponse(**res.json())
    assert res.status_code == 201
    assert updated_post.id == data['id']
    assert updated_post.title == data['title']

def test_update_post_not_owned(auth_client, test_user, test_posts):
    data = {
        'title': 'updated title',
        'content': 'updated content',
        'id': test_posts[3].id
    }
    res = auth_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403

def test_unauth_update_post(client, test_user, test_posts):
    data = {
        'title': 'updated title',
        'content': 'updated content',
        'id': test_posts[0].id
    }
    res = client.put(f"/posts/{test_posts[0].id}", json=data)
    assert res.status_code == 401

def test_upadate_post_not_exist(auth_client, test_user, test_posts):
    data = {
        'title': 'updated title',
        'content': 'updated content',
        'id': test_posts[3].id
    }
    res = auth_client.put(f"/posts/69", json=data)
    assert res.status_code == 404