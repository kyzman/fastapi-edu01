import pytest
from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


def test_unauthorized_get_all_posts(client):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_unauthorized_get_one_posts(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[1].id}")
    post = schemas.PostOut(**res.json())

    assert post.Post.id == test_posts[1].id
    assert post.Post.content == test_posts[1].content
    assert post.Post.title == test_posts[1].title
    assert res.status_code == 200


def test_one_post_not_exists(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/888")
    assert res.status_code == 404


@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "awesom new content", True),
    ("favorite pizza", "I live pepperoni", False),
    ("tallest skyscrapers", "wahoo", True),
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})
    new_post = schemas.Post(**res.json())

    assert res.status_code == 201
    assert new_post.title == title
    assert new_post.content == content
    assert new_post.published == published
    assert new_post.owner_id == test_user['id']


def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    res = authorized_client.post("/posts/", json={"title": "Arbitrary title", "content": "some content"})
    new_post = schemas.Post(**res.json())

    assert res.status_code == 201
    assert new_post.title == "Arbitrary title"
    assert new_post.content == "some content"
    assert new_post.published == True
    assert new_post.owner_id == test_user['id']


def test_unauthorized_create_post(client):
    res = client.post(f"/posts/", json={"title": "Dummy title", "content": "some dummy content"})
    assert res.status_code == 401


def test_unauthorized_delete_post(client, test_posts):
    res = client.delete(f"/posts/{test_posts[1].id}")
    assert res.status_code == 401


def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[1].id}")
    assert res.status_code == 204
    res = authorized_client.get("/posts")

    assert len(res.json()) == len(test_posts) - 1


def test_delete_post_not_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/8888")
    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403

