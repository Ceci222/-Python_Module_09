from datetime import datetime
from pydantic import BaseModel, Field, ValidationError


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)  # greater or equal/ less or equal
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime = Field(...)  # obligatory but has no default
    is_operational: bool = True
    notes: str | None = Field(default=None, max_length=200)
    # Could be str or None, it's None by default

# By inheriting from BaseModel it validates data type,
# and can also validate field requirements
# raises a ValidationError that can be then printed
# This class also allows direct printing of the object: print(my_station)


def main() -> None:

    print("Space Station Data Validation\n"
          "========================================")

    try:

        valid_station = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=6,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime(2026, 3, 15, 10, 30),
            is_operational=True,
            notes=None
        )

        status = "Not operational"
        if valid_station.is_operational:
            status = "Operational"  # Otherwise it will print True/False

        print("Valid station created:")
        print(f"ID: {valid_station.station_id}")
        print(f"Name: {valid_station.name}")
        print(f"Crew: {valid_station.crew_size} people")
        print(f"Power: {valid_station.power_level}%")
        print(f"Oxygen: {valid_station.oxygen_level}%")
        print(f"Status: {status}")

    except ValidationError as e:
        print(e.errors()[0]["msg"])  # Prints the error message

    print()

    print("========================================\n"
          "Expected validation error:")

    try:
        invalid_station = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=25,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime(2026, 3, 15, 10, 30),
            is_operational=True,
            notes=None
        )

        status = "Not operational"
        if invalid_station.is_operational:
            status = "Operational"

        print(f"ID: {invalid_station.station_id}")
        print(f"Name: {invalid_station.name}")
        print(f"Crew: {invalid_station.crew_size} people")
        print(f"Power: {invalid_station.power_level}%")
        print(f"Oxygen: {invalid_station.oxygen_level}%")
        print(f"Status: {status}")
    except ValidationError as e:
        print(e.errors()[0]["msg"])


if __name__ == "__main__":
    main()
