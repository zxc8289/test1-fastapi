from databases import Database
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# https://apis.data.go.kr/6260000/AttractionService/getAttractionKr?serviceKey=L4O6Jd5locofQV0Sa674EwMQ4GyHi380DNlzkWVMQLw8O2LvzNMvBKe1RxTj4jssgmQKPrDvinJFtSOIs9KmbA%3D%3D&pageNo=1&numOfRows=10&resultType=json


class ResponseDTO(BaseModel):
    code: int
    message: str
    data: object | None


class Cat(BaseModel):
    name: str
    id: int = 0


class RequestInsertRegionDTO(BaseModel):
    regionName: str


class RequestUpdateRegionDTO(BaseModel):
    regionName: str
    # regionId: int





app = FastAPI()


origins = [
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

database = Database("sqlite:///C:\code\sqlite\hr")


@app.get("/first/{id}")
async def root(id: int):
    return {"message": "Hello World", "id": id}


@app.get("/second")
async def second(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}


@app.post("/cat")
async def cat(cat: Cat):
    return cat


@app.get("/error")
async def error():
    dto = ResponseDTO(
        code=0,
        message="페이지가 없습니다.",
        data=None
    )
    return JSONResponse(status_code=404, content=jsonable_encoder(dto))


@app.get("/error1")
async def error1():
    raise HTTPException(status_code=404, detail={"message": "Item not found"})


@app.post("/files/")
async def check_file(
    uploadFile: UploadFile = File(), token: str = Form()
):
    return {
        "token": token,
        # "uploadFileSize": len(await upload_file.read()),
        "uploadFileName": uploadFile.filename,
        "uploadFileContentType": uploadFile.content_type,
    }


@app.get("/findall")
async def fetch_data():

    await database.connect()

    query = """SELECT * FROM EMPLOYEES  e WHERE SALARY >= 15000"""
    results = await database.fetch_all(query=query)

    await database.disconnect()

    return results


@app.post("/insert")
async def insert_data(requestInsertRegionDTO: RequestInsertRegionDTO):

    await database.connect()

    error = False

    try:
        query = f"""INSERT INTO REGIONS (region_name) values('{requestInsertRegionDTO.regionName}')"""
        results = await database.execute(query)
    except:
        error = True
    finally:
        await database.disconnect()

    if (error):
        return "에러발생"

    return results


@app.put("/update/{id}")
async def update_data(id: int,requestUpdateRegionDTO: RequestUpdateRegionDTO):
    
    await database.connect()
    error = False

    try:
        query = f"""UPDATE REGIONS set REGION_NAME = ('{requestUpdateRegionDTO.regionName}')  WHERE REGION_ID = ('{id}')"""
        results = await database.execute(query)
    except:
        error = True
    finally:
        await database.disconnect()

    if (error):
        return "에러발생"

    return results


@app.delete("/delete/{id}")
async def delete_data(id:int):
    
    await database.connect()
    error = False

    try:
        query = f"""DELETE FROM REGIONS WHERE REGION_ID = ('{id}')"""
        results = await database.execute(query)
    except:
        error = True
    finally:
        await database.disconnect()

    if (error):
        return "에러발생"

    return results
