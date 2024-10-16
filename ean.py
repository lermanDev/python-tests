import pydantic


class EANFormatError(Exception):
    """Custom error that is raised when an EAN code doesn't have the right format."""

    def __init__(self, value: str, message: str) -> None:
        self.value = value
        self.message = message
        super().__init__(message)


class BaseEAN(pydantic.BaseModel):
    """Base class for EAN"""

    value: str

    @classmethod
    def validate_digits(cls, value: str, expected_length: int):
        """Shared validation to check if the code consists of digits and has the correct length."""
        if len(value) != expected_length or not value.isdigit():
            raise EANFormatError(
                value=value,
                message=f"EAN code should be exactly {expected_length} digits."
            )
        return value


class EAN8(BaseEAN):
    """Class for EAN-8"""
    
    @pydantic.validator("value")
    def validate_ean8(cls, value: str) -> str:
        """Specific validation for EAN-8."""
        return cls.validate_digits(value=value, expected_length=8)


class EAN13(BaseEAN):
    """Class for EAN-13"""
    
    @pydantic.validator("value")
    def validate_ean13(cls, value: str) -> str:
        """Specific validation for EAN-13."""
        return cls.validate_digits(value=value, expected_length=13)
    
    def extract_variable_weight_data(self):
        prefix = self.value[0:2]
        merca_code = self.value[2:7]
        price_cents = self.value[7:12]

        return (prefix, merca_code, price_cents)
    
    def extract_merca_code(self):
        return self.ean[7:12]


def main() -> None:
    """Main function to create and validate EAN-8 and EAN-13 codes."""

    ean8 = EAN8(value="12345678")
    ean13 = EAN13(value="9780201379624")

    print(f"Valid EAN-8: {ean8.value}")
    print(f"Valid EAN-13: {ean13.value} variable data: {ean13.extract_variable_weight_data()}")

    try:
        invalid_ean8 = EAN8(value="1234567")  # This will raise an error (too short)
    except EANFormatError as e:
        print(f"Error: {e}")

    try:
        invalid_ean13 = EAN13(value="97802013796XX")  # This will raise an error (invalid characters)
    except EANFormatError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
