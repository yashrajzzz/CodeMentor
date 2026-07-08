from pydantic import BaseModel, Field
from typing import List


class CodeExplanation(BaseModel):
    summary: str = Field(
        description="Short summary of what the code does."
    )

    line_by_line: List[str] = Field(
        description="Important line-by-line explanation."
    )

    analogy: str = Field(
        description="Simple real-world analogy."
    )

    bugs: List[str] = Field(
        description="Potential bugs or mistakes."
    )

    improvements: List[str] = Field(
        description="Concrete improvement suggestions."
    )

    documentation: List[str] = Field(
        description="Relevant documentation findings."
    )

    time_complexity: str

    space_complexity: str