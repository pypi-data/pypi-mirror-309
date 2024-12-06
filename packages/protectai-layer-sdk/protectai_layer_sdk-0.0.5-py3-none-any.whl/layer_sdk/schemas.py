"""This module contains the schemas for the Layer SDK."""
import uuid
from enum import Enum
from typing import Any, Dict, List, Union, Optional
from datetime import datetime
from dataclasses import field, dataclass

from .exceptions import LayerSchemaValidationError


class SessionActionKind(Enum):
    """Enum for session action kinds.

    Attributes:
        EMBEDDINGS (str): Embeddings action
        MODERATION (str): Moderation action
        COMPLETION_PROMPT (str): Completion prompt action
        COMPLETION_OUTPUT (str): Completion output action
    """

    EMBEDDINGS = "embeddings"
    MODERATION = "moderation"
    COMPLETION_PROMPT = "completion_prompt"
    COMPLETION_OUTPUT = "completion_output"


@dataclass
class SessionActionError:
    """Error schema for session actions.

    Attributes:
        message (str): The error message. It is a required field
        code (int, optional): The error code
        details (Dict[str, Any], optional): The error details
    """

    message: str
    code: Optional[int] = None
    details: Optional[Dict[str, Any]] = None


@dataclass
class SessionActionScanner:
    """Scanner schema for session actions.

    Attributes:
        name (str): The scanner name
        data (Dict[str, Any]): The scanner data
    """

    name: str
    data: Dict[str, Any]


@dataclass
class SessionActionRequest:
    """Request schema for appending a new session action to an existing session.

    Attributes:
        kind (SessionActionKind): The action kind
        start_time (datetime): The action start time
        end_time (datetime): The action end time
        attributes (Dict[str, Any], optional): The action attributes
        data (Union[Dict, List], optional): The action data
        error (SessionActionError, optional): The action error
        scanners (List[Dict], optional): The action scanners
    """

    # The action kind. It is required field
    kind: SessionActionKind
    # The action start time. It is required field
    start_time: datetime
    # The action end time. It is required field
    end_time: datetime
    # The action attributes (i.e. metadata)
    attributes: Dict[str, Any] = field(default_factory=dict)
    # The action data (i.e. the result of the action)
    data: Optional[Dict] = None
    # The action error, if any
    error: Optional[SessionActionError] = None
    # The action scanners, if any
    scanners: Optional[List[SessionActionScanner]] = None


@dataclass
class SessionRequest:
    """Request schema for creating a new session.

    Attributes:
        application_id (Union[str, uuid.UUID]): The application ID
        session_id (Union[str, uuid.UUID], optional): The custom session ID
        attributes (Dict[str, str], optional): The session attributes
        actions (List[SessionActionRequest], optional): The session actions
    """

    # The application ID
    application_id: Union[str, uuid.UUID]
    # Custom session ID (UUID v5). If not provided, a new UUID will be generated
    session_id: Optional[Union[str, uuid.UUID]] = field(default=None)
    # The session attributes (i.e. metadata)
    attributes: Dict[str, str] = field(default_factory=dict)
    # The session actions, if any. When empty, the session will be created without any actions
    actions: Optional[List[SessionActionRequest]] = None

    def __post_init__(self):
        """Post initialization method to validate the schema."""
        if self.session_id is not None:
            if isinstance(self.session_id, uuid.UUID):
                session_id_uuid = self.session_id
            else:
                try:
                    session_id_uuid = uuid.UUID(self.session_id)
                except Exception as e:
                    raise LayerSchemaValidationError(e)

            if session_id_uuid.version != 5:
                raise LayerSchemaValidationError("Custom session ID must be a UUID v5")
