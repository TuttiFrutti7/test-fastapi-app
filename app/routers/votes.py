from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import schemas, models, oauth2
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(votereq: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == votereq.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post {votereq.post_id} does not exist")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == votereq.post_id, models.Vote.user_id == current_user.id)
    no_vote = db.query(models.Vote).filter(models.Vote.post_id == votereq.post_id, models.Vote.user_id == current_user.id, models.Vote.direction == 0)
    pos_vote = db.query(models.Vote).filter(models.Vote.post_id == votereq.post_id, models.Vote.user_id == current_user.id, models.Vote.direction == 1)
    neg_vote = db.query(models.Vote).filter(models.Vote.post_id == votereq.post_id, models.Vote.user_id == current_user.id, models.Vote.direction == -1)
    found_vote = vote_query.first()

    if (votereq.dir==1):
        if pos_vote.first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=
                                f"user {current_user.id} has already voted on post {votereq.post_id}")
        if neg_vote.first():
            neg_vote.delete()
        new_vote = models.Vote(post_id=votereq.post_id, user_id=current_user.id, direction=votereq.dir)
        db.add(new_vote)
        db.commit()
        return {"message": "succesfully added vote"}
    elif (votereq.dir==-1):
        if neg_vote.first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=
                                f"user {current_user.id} has already voted on post {votereq.post_id}")
        if pos_vote.first():
            pos_vote.delete()
        new_vote = models.Vote(post_id=votereq.post_id, user_id=current_user.id, direction=votereq.dir)
        db.add(new_vote)
        db.commit()
        return {"message": "succesfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "succesfully deleted vote"}