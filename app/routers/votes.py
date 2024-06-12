from .. import schemas, models, utils, oauth2
from ..database import get_db
from sqlalchemy.exc import IntegrityError
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

router = APIRouter(prefix="/vote", tags=["Votes"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def vote(
    vote: schemas.Vote,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    vote_query = db.query(models.Votes).filter(
        models.Votes.post_id == vote.post_id,
        models.Votes.user_id == current_user.id,
    )
    found_vote = vote_query.first()
    
    if vote.dir not in [0, 1]:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Vote direction must be 0 or 1",
        )

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You already voted this post",
            )
        
        new_vote = models.Votes(post_id= vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully voted"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="You have not voted this post",
            )
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully unvoted"}