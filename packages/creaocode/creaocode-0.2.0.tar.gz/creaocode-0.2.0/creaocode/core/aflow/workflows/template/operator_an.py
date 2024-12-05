# -*- coding: utf-8 -*-
# @Date    : 6/27/2024 19:46 PM
# @Author  : didi
# @Desc    : action nodes for operator
from typing import List
from pydantic import BaseModel, Field


class GenerateOp(BaseModel):
    response: str = Field(description="Your solution for this problem")

class CodeGenerateOp(BaseModel):
    code: str = Field(description="Your complete code solution for this problem")

class ScEnsembleOp(BaseModel):
    solution: str = Field(description="The most consistent solution.")

class SearchOp(BaseModel):
    response: str = Field(description="The search result")

class COTGenerateOp(BaseModel):
    thought: str = Field(description="The step by step thought process")
    answer: str = Field(description="The final answer")

class FormatOp(BaseModel):
    response: str = Field(description="The formatted response")

class ReviewOp(BaseModel):
    result: bool = Field(description="The result of the review")
    feedback: str = Field(description="The feedback of the review")

class ReviseOp(BaseModel):
    solution: str = Field(description="The revised solution")

class PlanOp(BaseModel):
    plan: List[str] = Field(description="The plan")
