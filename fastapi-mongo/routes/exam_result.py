from fastapi import APIRouter, Body
from typing import List

from models.exam_result import ExamResult
from schemas.exam_result import ExamResultCreate, ExamResultResponse

router = APIRouter()

