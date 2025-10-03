from fastapi import Depends, status, APIRouter, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional

from .. import models
from ..schemas import CreatePost, PostResponse, PostOut
from ..database import get_db
from .auth2 import get_current_user

router = APIRouter(prefix="/posts", tags=["posts_2"])


@router.get("/", response_model=list[PostOut])
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    # POST PARAMETERS
    # posts = (
    #     db.query(models.Post)
    #     .filter(models.Post.title.contains(search))
    #     .limit(limit)
    #     .offset(skip)
    #     .all()
    # )

    posts = (
        db.query(models.Post, func.count(models.Vote.post_id).label("likes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )

    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(
    post: CreatePost,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    # cursor.execute(
    #     "INSERT INTO posts (title, content, published) values(%s, %s, %s) RETURNING *",
    #     (post.title, post.content, post.published),
    # )
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(owner_id=current_user.id, **post.__dict__)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=PostResponse)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    # cursor.execute("SELECT * FROM posts WHERE id = %s", [id])

    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was Not Found",
        )
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", [id])
    # post = cursor.fetchone()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found",
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="U are not Authorized for such activity",
        )

    post_query.delete(synchronize_session=False)
    db.commit()
    return post


@router.put("/{id}", response_model=PostResponse)
def update_post(
    id: int,
    post: CreatePost,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    # cursor.execute(
    #     "UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
    #     [post.title, post.content, post.published, id],
    # )
    # post = cursor.fetchone()

    query_post = db.query(models.Post).filter(models.Post.id == id)

    if not query_post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found",
        )

    if query_post.first().owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="U are not Authorized for such activity",
        )
    query_post.update(post.__dict__)
    db.commit()
    return query_post.first()
