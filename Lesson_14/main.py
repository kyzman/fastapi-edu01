from fastapi import FastAPI, Depends, HTTPException
from starlette.requests import Request

app = FastAPI()


async def get_async_session():
    print("Get session")
    session = "session"
    yield session
    print("Session release")


# yield function
@app.get("/items")
async def get_items(session=Depends(get_async_session)):
    print(session)
    return [{"id": 1, }]


def pagination_params(limit: int = 10, skip: int = 0):
    return {"limit": limit, "skip": skip}


# parameters
@app.get("/subjects")
async def get_subjects(pagination_params: dict = Depends(pagination_params)):
    return pagination_params


# class
class Paginator:
    def __init__(self, limit: int = 10, skip: int = 0):
        self.limit = limit
        self.skip = skip



# parameters
@app.get("/subclass")
async def get_subclass(pagination_params: Paginator = Depends(Paginator)):  # тут можно одно из упоминаний Paginator убрать без каких либо последствий после ":" или который в ()
    return pagination_params


# dependencies = [Depends(...)]
# class call
# request
class AuthGuard:
    def __init__(self, name):
        self.name = name

    def __call__(self, request: Request):
        if "super_cookie" not in request.cookies:
            raise HTTPException(status_code=403, detail="Forbidden!!!!!!!!")
        # проверяем в куках инфу о наличии прав у пользователя
        print("Approved!")
        return True


auth_guard_payments = AuthGuard("payments")


@app.get("/payments", dependencies=[Depends(auth_guard_payments)])
def get_payments():
    return "my payments...."



