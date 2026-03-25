from datetime import datetime
from pydantic import BaseModel, Field, model_validator, ValidationError
from enum import Enum


class Rank(Enum):
    cadet = "cadet"
    officer = "officer"
    lieutenant = "lieutenant"
    captain = "captain"
    commander = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list = Field(min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def validate(self):
        if not self.mission_id.startswith("M"):
            raise ValueError('Mission ID must start with "M"')

        commanders = [c for c in self.crew if c.rank == Rank.commander]
        captains = [c for c in self.crew if c.rank == Rank.captain]
        if commanders == [] and captains == []:
            raise ValueError("Must have at least one Commander or Captain")

        if self.duration_days > 365:
            expes = [exp for exp in self.crew if exp.years_experience >= 5]
            if len(expes) < len(self.crew) // 2:
                raise ValueError("Long missions (> 365 days) need "
                                 "50% experienced crew (5+ years)")

        for member in self.crew:
            if not member.is_active:
                raise ValueError("All crew members must be active")
        return self


def main():
    crew_members = [
        CrewMember(member_id="AC01", name="Sarah Connor", rank=Rank.commander,
                   age=35, specialization="Mission Command",
                   years_experience=10, is_active=True),
        CrewMember(member_id="AC02", name="John Smith", rank=Rank.lieutenant,
                   age=30, specialization="Navigation",
                   years_experience=4, is_active=True),
        CrewMember(member_id="AC03", name="Alice Johnson", rank=Rank.officer,
                   age=28, specialization="Engineering", years_experience=4,
                   is_active=True),
    ]
    space_mission = SpaceMission(
                                mission_id="M2024_MARS",
                                mission_name="Mars Colony Establishment",
                                destination="Mars",
                                launch_date=datetime(2026, 3, 21, 9, 41),
                                duration_days=900,
                                crew=crew_members,
                                budget_millions=2500.0
                            )

    print("Space Mission Crew Validation")
    print("=========================================")
    print("Valid mission created:")
    print(f"Mission: {space_mission.mission_name}")
    print(f"ID: {space_mission.mission_id}")
    print(f"Destination: {space_mission.destination}")
    print(f"Duration: {space_mission.duration_days} days")
    print(f"Budget: ${space_mission.budget_millions}M")
    print(f"Crew size: {len(space_mission.crew)}")
    for member in space_mission.crew:
        print(f"- {member.name} ({member.rank.value}) - "
              f"{member.specialization}")

    try:
        print("\n=========================================")
        crew_members = [
                    CrewMember(member_id="AC01", name="Sarah Connor",
                               rank=Rank.cadet,
                               age=35, specialization="Mission Command",
                               years_experience=10, is_active=True),
                    CrewMember(member_id="AC02", name="John Smith",
                               rank=Rank.lieutenant,
                               age=30, specialization="Navigation",
                               years_experience=4, is_active=True),
                    CrewMember(member_id="AC03", name="Alice Johnson",
                               rank=Rank.officer,
                               age=28, specialization="Engineering",
                               years_experience=6, is_active=True),
                ]
        mission = SpaceMission(
                                mission_id="M2024_MARS",
                                mission_name="Mars Colony Establishment",
                                destination="Mars",
                                launch_date=datetime(2026, 3, 21, 9, 41),
                                duration_days=900,
                                crew=crew_members,
                                budget_millions=2500.0
                            )
        print(f"Mission {mission.mission_id} Validated!")
    except ValidationError as e:
        print("Expected validation error:")
        for err in e.errors():
            print(err["msg"])


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"{e.__class__.__name__}: {e}")
