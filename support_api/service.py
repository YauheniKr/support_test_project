from dataclasses import dataclass

from support_api.choices import Status
from support_api.models import Post


@dataclass
class PostStatusCheck:
    post: Post

    def __change_post_status__(self) -> None:
        if self.post.status == Status.CLOSE:
            raise ValueError('Couldn"t create comments. Post is Closed')
        if self.post.status == Status.OPEN:
            self.post.status = 'In progress'
            self.post.save()
