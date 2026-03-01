from fastapi import APIRouter, HTTPException, Body
from beanie import PydanticObjectId
from typing import List

from models.station import Station
from schemas.station import StationCreate, StationResponse

from database.database import add_station, retrieve_stations, retrieve_station

router = APIRouter()

@router.post("/", response_model=StationResponse)
async def create_station(station_data: StationCreate = Body(...)):
    new_station = Station(**station_data.model_dump())
    create_station = await add_station(new_station)
    return create_station

@router.get("/", response_model=List[StationResponse])
async def get_all_stations():
    stations = await retrieve_stations()
    return stations

@router.get("/{id}", response_model=StationResponse)
async def get_station(id: PydanticObjectId):
    station = await retrieve_station(id)
    if not station:
        raise HTTPException(status_code=404, detail="Không tìm thấy trạm thi (Station)")
    return station