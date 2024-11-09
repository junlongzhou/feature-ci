from enum import IntEnum, Enum

MAXIMUM_LEN_OF_GIT_BRANCH = 250

FCI_ID_PREFIX = 'FCI'

FCI_ID_MAXIMUM_LEN = 22

class Status(IntEnum):
    PAUSE = -2
    ABANDONED = -1
    INACTIVE = 0
    DRAFT = 1
    WIP = 2
    ACTIVE = 9
    MERGED = 10

class TemplateKind(Enum):
    COMPONENT = 'component'
    FEATURE = 'feature'

    @classmethod
    def to_choices(cls):
        return [(name, member.value) for name, member in cls.__members__.items()]

class Action(Enum):
    APPROVE = 'approve'
    ABANDON = 'abandon'

    @classmethod
    def to_choices(cls):
        return [(name, member.value) for name, member in cls.__members__.items()]

class Widget(Enum):
    TEXT = 'text'
    SELECT = 'select'
    SELECT_MULTIPLE = 'select_multiple'
    BUTTON = 'button'

    @classmethod
    def values(cls):
        return [member.value for _, member in cls.__members__.items()]
