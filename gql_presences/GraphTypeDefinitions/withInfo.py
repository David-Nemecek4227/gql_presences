from contextlib import asynccontextmanager

@asynccontextmanager
async def withInfo(info):
    asyncSessionMaker = info.context["asyncSessionMaker"]
    async with asyncSessionMaker() as session:
        try:
            yield session
        finally:
            pass


def AsyncSessionFromInfo(info):
    print(
        "obsolete function used AsyncSessionFromInfo, use withInfo context manager instead"
    )
    return info.context["session"]

