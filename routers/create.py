from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from typing import List

from models import User, Event, Invitation, InvitationEnum, StatusEnum, Budget
from db import get_session
from schemas import AddEvent, EventUpdate, GetEvent, GetEventWithGuests, StatusEnum, BudgetCreate
from utils import verify_access_token

router = APIRouter(prefix='/events', tags=['events'],
                   responses={404: {"description": "Not found"}})


@router.post('/add_event/')
async def add_event(data: AddEvent, session: Session = Depends(get_session),
                    current_user: User = Depends(verify_access_token)):
    event = Event(title=data.title,
                  description=data.description,
                  date=data.date,
                  time=data.time,
                  location=data.location,
                  host_id=current_user.id,
                  status=data.status)
    session.add(event)
    session.commit()
    raise HTTPException(status_code=200)


@router.put('/event_update/')
async def update_event_data(data: EventUpdate,
                            session: Session = Depends(get_session),
                            user: User = Depends(verify_access_token)):
    event = session.get(Event, data.id)
    if not event:
        raise HTTPException(status_code=404, detail='Event not found')

    event.description = data.description
    event.date = data.date
    event.time = data.time
    event.location = data.location
    event.status = data.status
    session.commit()
    session.refresh(event)
    raise HTTPException(status_code=200)


@router.delete('/del_event/{event_id}')
def del_event(event_id: int, session: Session = Depends(get_session),
              current_user: User = Depends(verify_access_token)):
    event = session.exec(select(Event).where(Event.id == event_id)).first()
    if not event:
        raise HTTPException(status_code=404, detail='Event not found')

    invitations = session.exec(select(Invitation).where(Invitation.event_id == event_id)).all()
    for invitation in invitations:
        session.delete(invitation)

    session.delete(event)
    session.commit()
    raise HTTPException(status_code=200)


@router.get('/event_status/{event_id}')
def stat_event(event_id: int, session: Session = Depends(get_session),
               current_user: User = Depends(verify_access_token)):
    event = session.exec(select(Event).where(Event.id == event_id)).first()
    if not event:
        raise HTTPException(status_code=404, detail='An event not found')
    if event.status == 'planned':
        raise HTTPException(status_code=400, detail='The event is planned')
    if event.status == 'ended':
        raise HTTPException(status_code=400, detail='The event is completed')
    if event.status == 'active':
        raise HTTPException(status_code=400, detail='An event in progress')
    event.service()
    session.add(event)
    session.commit()
    session.refresh(event)
    raise HTTPException(status_code=200)


@router.post('/invite_guest/{event_id}/{guest_id}')
def invite_guest(event_id: int, guest_id: int, session: Session = Depends(get_session),
                 current_user: User = Depends(verify_access_token)):
    event = session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail='Event not found')

    if event.host_id != current_user.id:
        raise HTTPException(status_code=403, detail='Only the creator can invite guests')

    guest = session.get(User, guest_id)
    if not guest:
        raise HTTPException(status_code=404, detail='User not found')

    invitation = Invitation(event_id=event_id, user_id=guest_id, status=InvitationEnum.confirm)
    session.add(invitation)
    session.commit()
    raise HTTPException(status_code=200)


@router.delete('/remove_guest/{event_id}/{guest_id}')
def remove_guest(event_id: int, guest_id: int, session: Session = Depends(get_session),
                 current_user: User = Depends(verify_access_token)):
    invitation = session.exec(
        select(Invitation).where(Invitation.event_id == event_id, Invitation.user_id == guest_id)).first()
    if not invitation:
        raise HTTPException(status_code=404, detail='Invitation not found')

    session.delete(invitation)
    session.commit()
    raise HTTPException(status_code=200)


@router.get('/notify_events/', response_model=List[GetEvent])
def notify_events(session: Session = Depends(get_session),
                  current_user: User = Depends(verify_access_token)):
    hosted_events = session.exec(select(Event).where(Event.host_id == current_user.id)).all()

    invited_events = session.exec(
        select(Event).join(Invitation).where(Invitation.user_id == current_user.id)).all()

    user_events = hosted_events + invited_events

    return user_events


@router.get('/share_event/{event_id}', response_model=GetEvent)
def share_event(event_id: int, session: Session = Depends(get_session), current_user: User = Depends(verify_access_token)):
    event = session.exec(select(Event).where(Event.id == event_id)).first()
    if not event:
        raise HTTPException(status_code=404, detail='Event not found')

    return GetEvent.from_orm(event)


@router.post('/add_budget/{event_id}')
async def add_budget(event_id: int, data: BudgetCreate, session: Session = Depends(get_session),
                     current_user: User = Depends(verify_access_token)):
    event = session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail='Event not found')

    budget = Budget(event_id=event_id, description=data.description, amount=data.amount)
    session.add(budget)
    session.commit()
    raise HTTPException(status_code=200)


@router.get('/event_budget/{event_id}', response_model=List[Budget])
def get_budgets(event_id: int, session: Session = Depends(get_session),
                current_user: User = Depends(verify_access_token)):
    budgets = session.exec(select(Budget).where(Budget.event_id == event_id)).all()
    return budgets


@router.get('/event_info/{event_id}', response_model=GetEventWithGuests)
def get_event_with_guests(event_id: int, session: Session = Depends(get_session),
                          current_user: User = Depends(verify_access_token)):
    event = session.exec(select(Event).where(Event.id == event_id)).first()

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    invitations = session.exec(select(Invitation).where(Invitation.event_id == event_id)).all()
    if not invitations:
        raise HTTPException(status_code=404, detail='No invitations found for this event')

    guest_ids = [invitation.user_id for invitation in invitations]
    guests = session.exec(select(User).where(User.id.in_(guest_ids))).all()

    return GetEventWithGuests(event=event, guests=guests)


@router.get('/upcoming_events/', response_model=List[GetEvent])
def get_events_planned(session: Session = Depends(get_session),
                       current_user: User = Depends(verify_access_token)):
    events = session.exec(select(Event).where(Event.status == StatusEnum.planned)).all()
    return events


@router.get('/events_archive/', response_model=List[GetEvent])
def get_events_ended(session: Session = Depends(get_session),
                     current_user: User = Depends(verify_access_token)):
    events = session.exec(select(Event).where(Event.status == StatusEnum.ended)).all()
    return events