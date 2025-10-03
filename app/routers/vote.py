from fastapi import status, HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import Vote
from .. import models
from .auth2 import get_current_user

router = APIRouter(prefix="/vote", tags=["votes"])


@router.post("/{id}", status_code=status.HTTP_201_CREATED)
def vote(
    vote_dir: Vote,
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with the id: {id} was not found",
        )

    vote_query = db.query(models.Vote).filter(
        models.Vote.user_id == current_user.id, models.Vote.post_id == post.id
    )

    found_vote = vote_query.first()
    if vote_dir.dir:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with id {current_user.id} has already like the post with id: {id}",
            )
        new_vote = models.Vote(user_id=current_user.id, post_id=post.id)
        db.add(new_vote)
        db.commit()
        return {"Message": "Successfully liked the post"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist"
            )
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"Message": "successfully unliked the post"}
