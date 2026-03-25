from pydantic import BaseModel, Field, model_validator, ValidationError
from datetime import datetime
from enum import Enum
from typing import Optional


class ContactType(Enum):
    radio = "radio"
    visual = "visual"
    physical = "physical"
    telepathic = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str] = Field(max_length=100)
    is_verified: bool = True

    @model_validator(mode="after")
    def validation(self):
        if not self.contact_id.startswith("AC"):
            raise ValueError("contact_id must start with 'AC'")

        if self.contact_type == ContactType.physical:
            if not self.is_verified:
                raise ValueError("Physical contact reports must be verified")

        if self.contact_type == ContactType.telepathic:
            if self.witness_count < 3:
                raise ValueError("Telepathic contact requires at least "
                                 "3 witnesses")

        if self.signal_strength > 7.0:
            if not self.message_received:
                raise ValueError("Strong signals (> 7.0) should include "
                                 "received messages")

        return self


def main():
    print("Alien Contact Log Validation\n")
    print("======================================")
    valid_contact = AlienContact(
        contact_id="AC_2024_001",
        timestamp="2026-03-19T14:30:00",
        location="Area 51, Nevada",
        contact_type=ContactType.radio.value,
        signal_strength=8.5,
        duration_minutes=45,
        witness_count=5,
        message_received="'Greetings from Zeta Reticuli'"
    )
    print("Valid contact report:")
    print(f"ID: {valid_contact.contact_id}")
    print(f"Type: {valid_contact.contact_type}")
    print(f"Location: {valid_contact.location}")
    print(f"Signal: {valid_contact.signal_strength}/10")
    print(f"Duration: {valid_contact.duration_minutes} minutes")
    print(f"Witnesses: {valid_contact.witness_count}")
    print(f"Message: {valid_contact.message_received}\n")

    print("======================================")
    try:
        valid_contact = AlienContact(
                            contact_id="AC_2024_001",
                            timestamp="2026-03-19T14:30:00",
                            location="Area 51, Nevada",
                            contact_type=ContactType.telepathic.value,
                            signal_strength=8.5,
                            duration_minutes=45,
                            witness_count=2,
                            message_received="'Greetings from Zeta Reticuli'"
                        )
    except ValidationError as e:
        print("Expected validation error:")
        for err in e.errors():
            print(err["msg"])


main()
