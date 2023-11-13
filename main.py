import enum

class TestClass(enum.Enum):
    PLACEHOLDER1 = "1"
    PLACEHOLDER2 = "2"
    PLACEHOLDER3 = "3"
    PLACEHOLDER4 = "4"

    @classmethod
    def get_values(cls, target):
        for member in cls:
            if member.name == target:
                return member.value
            else:
                pass
    

results = TestClass.get_values("PLACEHOLDER1")
print(results)