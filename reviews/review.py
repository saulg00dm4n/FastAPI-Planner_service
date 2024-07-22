from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from models import User, Event, Review
from schemas import ReviewCreate, ReviewResponse
from db import get_session
from utils import verify_access_token
from typing import List

router = APIRouter(prefix='/reviews', tags=['reviews'],
                   responses={404: {"description": "Not found"}})


@router.post('/create_review/', response_model=ReviewResponse)
async def create_review(data: ReviewCreate, session: Session = Depends(get_session),
                        current_user: User = Depends(verify_access_token)):
    event = session.get(Event, data.event_id)
    if not event:
        raise HTTPException(status_code=404, detail='Event not found')

    if data.rating < 1 or data.rating > 5:  # оценка по 5-ти бальной шкале
        raise HTTPException(status_code=400, detail='Rating must be between 1 and 5')

    review = Review(event_id=data.event_id, user_id=current_user.id, rating=data.rating, comment=data.comment)
    session.add(review)
    session.commit()
    session.refresh(review)
    raise HTTPException(status_code=200)


@router.get('/review_list/', response_model=List[ReviewResponse])
async def get_reviews(event_id: int, session: Session = Depends(get_session),
                      current_user: User = Depends(verify_access_token)):
    reviews = session.exec(select(Review).where(Review.event_id == event_id)).all()
    if not reviews:
        raise HTTPException(status_code=404, detail='No reviews found for this event')
    return reviews


@router.delete('/delete_review/')
async def delete_review(review_id: int, session: Session = Depends(get_session),
                        current_user: User = Depends(verify_access_token)):
    review = session.get(Review, review_id)
    if not review:
        raise HTTPException(status_code=404, detail='Review not found')

    if review.user_id != current_user.id:
        raise HTTPException(status_code=403, detail='This review is not yours')

    session.delete(review)
    session.commit()
    raise HTTPException(status_code=200)
