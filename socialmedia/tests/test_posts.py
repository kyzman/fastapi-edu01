from typing import List
from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    def validate(post):
        return schemas.PostOut(**post)

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


