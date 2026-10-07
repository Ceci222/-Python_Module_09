from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, ValidationError, model_validator


class ContactType(Enum):
    RADIO = "radio"  # enum → data type with name-value pair
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"
# ContactType.RADIO.value → "radio"
# ContactType.RADIO.name → "RADIO"
# enum determines what will be accepted in the ContactType field
# The attribute will only accept that value for each member (RADIO)
# Enum values can but mustn't be reassigned with _value_
# ContactType.RADIO._value_ = "sth else" → not good practice


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime = Field(...)
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType = Field(...)
    # The field is obligatory (...) and must be within the enum
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: str | None = Field(default=None, max_length=500)
    # optional, if string with some constraints defined in the field
    is_verified: bool = False

    @model_validator(mode="after")
    # model validator after determines once all attributes are ready
    # and after instantiation it will check with my rules
    # if sth's wrong it doesn't create the object and throws raises error
    def check_rules(self) -> "AlienContact":
        # since the verification is within the class py has not had access
        # to the entire class and objects are still conditional
        # that is why they go with "", had the validation been outside the
        # class, no "" would be necessary
        if not self.contact_id.startswith("AC"):
            raise ValueError("Contact ID must start with 'AC'")

        if self.contact_type is ContactType.PHYSICAL and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")

        if self.contact_type is ContactType.TELEPATHIC:
            if self.witness_count < 3:
                raise ValueError(
                    "Telepathic contact requires at least 3 witnesses"
                )

        if self.signal_strength > 7.0 and self.message_received is None:
            raise ValueError(
                "Strong signals should include received messages"
            )

        return self
# "self" doesn't exist in this class till everything's been validated
# by retruning "self" Pydantic gets it back & returns the valid object
# in valid_contact it saves "self" (the validated object)
# if a raise appears the excecution stops and nothing's stored in the variable


def main() -> None:

    print("Alien Contact Log Validation\n"
          "======================================")

    try:
        valid_contact = AlienContact(
            contact_id="AC_2024_001",
            timestamp=datetime(2024, 7, 12, 22, 15),
            location="Area 51, Nevada",
            contact_type=ContactType.RADIO,
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=5,
            message_received="Greetings from Zeta Reticuli",
            is_verified=True
        )

        print("Valid contact report:")
        print(f"ID: {valid_contact.contact_id}")
        print(f"Type: {valid_contact.contact_type.value}")
        print(f"Location: {valid_contact.location}")
        print(f"Signal: {valid_contact.signal_strength}/10")
        print(f"Duration: {valid_contact.duration_minutes} minutes")
        print(f"Witnesses: {valid_contact.witness_count}")
        print(f"Message: '{valid_contact.message_received}'")

    except ValidationError as e:
        print(e.errors()[0]["msg"])

    print()

    print("======================================\n"
          "Expected validation error:")

    try:
        invalid_contact = AlienContact(
            contact_id="AC_2024_002",
            timestamp=datetime(2024, 7, 13, 3, 40),
            location="Roswell, New Mexico",
            contact_type=ContactType.TELEPATHIC,
            signal_strength=5.0,
            duration_minutes=20,
            witness_count=1,
            message_received=None,
            is_verified=False
        )

        print(f"ID: {invalid_contact.contact_id}")
        print(f"Type: {invalid_contact.contact_type.value}")
        print(f"Location: {invalid_contact.location}")

    except ValidationError as e:
        print(e.errors()[0]["msg"].replace("Value error, ", ""))
        # print(e.errors()[0]["msg"])
        # prints from full list (e.errors) the msg of list element
        # needs .replace to remove default Value error added by Pydantic


if __name__ == "__main__":
    main()
