from typing import TypeVar, Callable
from typing_extensions import ParamSpec
from concurrent.futures import ThreadPoolExecutor

from sqlalchemy.orm.query import Query as QueryBase, _T
from promise import Promise


_P = ParamSpec("_P")
_R = TypeVar("_R")

executor = ThreadPoolExecutor(max_workers=None)


def promisified_query_result(
    resolve, reject, fn: Callable[_P, _R], *args: _P.args, **kwargs: _P.kwargs
):
    resp = executor.submit(fn, *args, **kwargs)
    try:
        resolve(resp).then(lambda x: x.result())
    except BaseException as e:
        reject(e)


class Query(QueryBase):
    def all(self) -> Promise[_T]:
        promise = Promise(
            lambda resolve, reject: promisified_query_result(
                resolve, reject, super(Query, self).all
            )
        )
        return promise
