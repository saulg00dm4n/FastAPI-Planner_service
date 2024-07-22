# from fastapi import APIRouter, HTTPException, Response, Depends
# from sqlmodel import Session, select
# from datetime import datetime
#
# from db import get_session
# from models import Event, User, EventCost, Payment
# from schemas import GetEvent, AddEvent, PaymentCreate, EventUpdate
# from utils import verify_access_token, get_delta_time
#
# router = APIRouter(tags=['car_and_rent'],
#                    responses={404: {"description": "Not found"}})
#
#
# # @router.get('/get_car/')
# # def get_car_temp(data: GetCar, session: Session = Depends(get_session)):
# #     get_car(data)
# #     return get_car(data)
#
#
# @router.post('/rent_car/')
# def rent_car(title: str, session: Session = Depends(get_session), user: User = Depends(verify_access_token)):
#     if user.role == 'no_verify':
#         raise HTTPException(status_code=403, detail='You have not passed verification.')
#     if user.role == 'BAN':
#         raise HTTPException(status_code=403, detail='You are BANed!!!')
#     event = session.exec(select(Event).where(Event.title == title)).first()
#     if session.exec(select(Payment).where(Payment.user_id == user.id).where(Payment.status == 'waiting')).first():
#         raise HTTPException(status_code=402,
#                             detail="You have an unpaid trip. Pay for the trip for further use of the service")
#     if not event:
#         raise HTTPException(status_code=400, detail='Incorrect car number')
#     if session.exec(select(EventCost).where(EventCost.user_id == user.id).where(EventCost.data_rent_end == None)).first():
#         raise HTTPException(status_code=429, detail="You didn't complete the last trip. To continue, complete the trip")
#
#     event.no_active()
#     eventcost = EventCost(user_id=user.id, event_id=event.id)
#     session.add(event)
#     session.add(eventcost)
#     session.commit()
#     session.refresh(event)
#     raise HTTPException(status_code=200)
#
#
# @router.put('/end_rent_car/')
# def end_rent_car(data: PaymentCreate, user: User = Depends(verify_access_token), session: Session = Depends(get_session)):
#     rent = session.exec(select(EventCost).where(EventCost.user_id == user.id).where(EventCost.data_rent_end == None)).first()
#     if not rent:
#         raise HTTPException(status_code=400, detail="You don't have any trips started")
#     if user.role == 'BAN':
#         raise HTTPException(status_code=403, detail='You are BANed!!!')
#     car = session.exec(select(Event).where(Event.id == rent.car_id)).first()
#     rent.end()
#     car.active()
#     payment = Payment(rent_id=rent.id, user_id=user.id,
#                       prise=(car.price_order * get_delta_time(rent.data_rent_start, rent.data_rent_end)),
#                       card_number=data.card_number)
#     session.add(rent)
#     session.add(car)
#     session.add(payment)
#     session.commit()
#     session.refresh(rent)
#     session.refresh(car)
#     # здесь должна быть функция для обновления геолокации машины
#     raise HTTPException(status_code=200)
#
#
# @router.get('/my_rent')
# def get_my_rent(user: User = Depends(verify_access_token), session: Session = Depends(get_session)):
#     my_rents = session.exec(select(EventCost).where(EventCost.user_id == user.id)).all()
#     if not my_rents:
#         return "You don't have any trips"
#     return my_rents