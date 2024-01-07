from typing import List
from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    def validate(post):
        return schemas.PostOut(**post)


    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


