from sqlalchemy.orm.query import Query as QueryBase
from promise import Promise

class Query(QueryBase):
    def promise(self):
        promise = Promise()
        promise.resolve(self)
