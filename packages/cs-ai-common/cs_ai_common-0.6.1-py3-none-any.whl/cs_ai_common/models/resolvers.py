from typing import List, Optional
from pydantic import BaseModel

class ResolverResponse(BaseModel): 
    Price: Optional[str] = None
    PriceCurrency: Optional[str] = None
    Mileage: Optional[str] = None
    ProductionYear: Optional[str] = None
    FuelType: Optional[str] = None
    Transmision: Optional[str] = None
    HorsePower: Optional[str] = None
    Capacity: Optional[str] = None
    AdvertisementLink: Optional[str] = None
    Thumbnails: Optional[List[str]] = None
    Source: Optional[str] = None
    SourceId: Optional[str] = None
    Location_Country: Optional[str] = None
    Location_City: Optional[str] = None
    Location_PostalCode: Optional[str] = None
    Make: Optional[str] = None
    Model: Optional[str] = None

class ResolverStatsModel(BaseModel):
    ResolverName: str
    TotalAds: int

class TaskStatisticsModel(BaseModel):
    Stats: List[ResolverStatsModel] = None