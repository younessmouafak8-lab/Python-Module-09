from pydantic import BaseModel, Field, ValidationError
from datetime import datetime
from typing import Optional


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: Optional[str] = Field(max_length=200)


def main():
    try:
        space_station = SpaceStation(
                                    station_id="ISS001",
                                    name="International Space Station",
                                    crew_size=6,
                                    power_level=85.5,
                                    oxygen_level=92.3,
                                    last_maintenance="2024-01-15T10:30:00",
                                    notes="All Good"
                                )
        print("Space Station Data Validation")
        print("===============================================")
        print("Valid station created:")
        print(f"ID: {space_station.station_id}")
        print(f"Name: {space_station.name}")
        print(f"Crew: {space_station.crew_size} people")
        print(f"Power: {space_station.power_level}%")
        print(f"Oxygen: {space_station.oxygen_level}%")
        status = ("Operational" if space_station.is_operational
                  else "Not operational")
        print(f"Status: {status}")
    except ValidationError as e:
        print("Expected validation error:")
        for err in e.errors():
            print(err["msg"])

    print("\n===============================================")
    try:
        space_station = SpaceStation(
                            station_id="ISS001",
                            name="International Space Station",
                            crew_size=21,
                            power_level=85.5,
                            oxygen_level=92.3,
                            last_maintenance="2024-01-15T10:30:00",
                            notes="All Good"
                        )
    except ValidationError as e:
        print("Expected validation error:")
        for err in e.errors():
            print(err["msg"])


if __name__ == "__main__":
    main()
