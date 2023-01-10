from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from models import Inmueble

router = APIRouter()


@router.post("/", response_description="Create a new inmueble", status_code=status.HTTP_201_CREATED, response_model=Inmueble)
def create_inmueble(request: Request, inmueble: Inmueble = Body(...)):
    inmueble = jsonable_encoder(inmueble)
    if inmueble.get('_id'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID field cannot be set manually")
    new_inmueble = request.app.database['inmuebles'].insert_one(inmueble)
    created_inmueble = request.app.database['inmuebles'].find_one(
        {'_id': new_inmueble.inserted_id}
    )
    return created_inmueble

@router.get("/", response_description="Get all inmuebles", response_model=List[Inmueble])
def get_all_inmuebles(request: Request):
    inmuebles = list(request.app.database['inmuebles'].find())
    return inmuebles

@router.get("/{id}", response_description="Get an inmueble by id", response_model=Inmueble)
def get_inmueble(id: str, request: Request):
    if (inmueble := request.app.database["inmuebles"].find_one({'_id': id})) is not None:
        return inmueble
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inmueble with ID {} does not exist".format(id))

# They will already have the full object when they get here, so it's OK to just put the full object
@router.put("/{id}", response_description="Edit an inmueble by ID", response_model=Inmueble)
def edit_inmueble(id: str,request: Request, inmueble: Inmueble = Body(...)):
    inmueble = jsonable_encoder(inmueble)
    if inmueble['_id'] != id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID field cannot be edited")
    edit_result = request.app.database['inmuebles'].update_one({'_id': id}, {'$set': inmueble})
    if edit_result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inmueble with ID {} does not exist".format(id))
    if (inmueble := request.app.database['inmuebles'].find_one({'_id': id})) is not None:
        return inmueble
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inmueble with ID {} does not exist".format(id))

@router.delete("/{id}", response_description="Delete an inmueble by id")
def delete_inmueble(id: str, request: Request, response: Response):
    if request.app.database['inmuebles'].delete_one({"_id": id}).deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inmueble with ID {} does not exist".format(id))
