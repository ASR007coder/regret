# backend/database/model.py

from datetime import datetime

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    func,
    text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


# ==================================================
# BASE MODEL
# ==================================================

class Base(DeclarativeBase):
    pass


# ==================================================
# 1. USER TABLE
# ==================================================

class User(Base):

    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
        autoincrement=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    dob: Mapped[datetime | None] = mapped_column(
        Date,
        nullable=True
    )

    phone: Mapped[str | None] = mapped_column(
        String(15),
        unique=True,
        nullable=True
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
    default=False,
    server_default=text("0"),
    nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    # Relationships

    questions: Mapped[list["Question"]] = relationship(
        back_populates="user"
    )

    answers: Mapped[list["Answer"]] = relationship(
        back_populates="user"
    )

    likes: Mapped[list["Like"]] = relationship(
        back_populates="user"
    )

    comments: Mapped[list["Comment"]] = relationship(
        back_populates="user"
    )

    shares: Mapped[list["Share"]] = relationship(
        back_populates="user"
    )


# ==================================================
# 2. QUESTION TABLE
# ==================================================

class Question(Base):

    __tablename__ = "questions"

    ques_id: Mapped[int] = mapped_column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
        autoincrement=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id", ondelete="RESTRICT"),
        nullable=True,
        index=True
    )

    question: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    # Relationships

    user: Mapped["User"] = relationship(
        back_populates="questions"
    )

    answers: Mapped[list["Answer"]] = relationship(
        back_populates="question",
        cascade="all, delete-orphan"
    )

    likes: Mapped[list["Like"]] = relationship(
        back_populates="question",
        foreign_keys="Like.ques_id",
        cascade="all, delete-orphan"
    )

    comments: Mapped[list["Comment"]] = relationship(
        back_populates="question",
        foreign_keys="Comment.ques_id",
        cascade="all, delete-orphan"
    )

    shares: Mapped[list["Share"]] = relationship(
        back_populates="question",
        foreign_keys="Share.ques_id",
        cascade="all, delete-orphan"
    )


# ==================================================
# 3. ANSWER TABLE
# ==================================================

class Answer(Base):

    __tablename__ = "answers"

    ans_id: Mapped[int] = mapped_column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
        autoincrement=True
    )

    ques_id: Mapped[int] = mapped_column(
        ForeignKey("questions.ques_id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id", ondelete="RESTRICT"),
        nullable=True,
        index=True
    )

    answer: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    # Relationships

    question: Mapped["Question"] = relationship(
        back_populates="answers"
    )

    user: Mapped["User"] = relationship(
        back_populates="answers"
    )

    likes: Mapped[list["Like"]] = relationship(
        back_populates="answer",
        foreign_keys="Like.ans_id",
        cascade="all, delete-orphan"
    )

    comments: Mapped[list["Comment"]] = relationship(
        back_populates="answer",
        foreign_keys="Comment.ans_id",
        cascade="all, delete-orphan"
    )

    shares: Mapped[list["Share"]] = relationship(
        back_populates="answer",
        foreign_keys="Share.ans_id",
        cascade="all, delete-orphan"
    )


# ==================================================
# 4. LIKE TABLE
# ==================================================

class Like(Base):

    __tablename__ = "likes"

    like_id: Mapped[int] = mapped_column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
        autoincrement=True
    )

    ques_id: Mapped[int | None] = mapped_column(
        ForeignKey("questions.ques_id", ondelete="CASCADE"),
        nullable=True,
        index=True
    )

    ans_id: Mapped[int | None] = mapped_column(
        ForeignKey("answers.ans_id", ondelete="CASCADE"),
        nullable=True,
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="active",
        server_default="active",
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    # Constraints

    __table_args__ = (
        CheckConstraint(
            "(ques_id IS NOT NULL AND ans_id IS NULL) OR "
            "(ques_id IS NULL AND ans_id IS NOT NULL)",
            name="ck_like_single_target"
        ),

        CheckConstraint(
            "status IN ('active', 'inactive')",
            name="ck_like_status"
        ),

        Index(
            "uq_like_user_question",
            "user_id",
            "ques_id",
            unique=True,
            sqlite_where=text("ques_id IS NOT NULL")
        ),

        Index(
            "uq_like_user_answer",
            "user_id",
            "ans_id",
            unique=True,
            sqlite_where=text("ans_id IS NOT NULL")
        ),
    )

    # Relationships

    user: Mapped["User"] = relationship(
        back_populates="likes"
    )

    question: Mapped["Question | None"] = relationship(
        back_populates="likes",
        foreign_keys=[ques_id]
    )

    answer: Mapped["Answer | None"] = relationship(
        back_populates="likes",
        foreign_keys=[ans_id]
    )


# ==================================================
# 5. COMMENT TABLE
# ==================================================

class Comment(Base):

    __tablename__ = "comments"

    comment_id: Mapped[int] = mapped_column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
        autoincrement=True
    )

    ques_id: Mapped[int | None] = mapped_column(
        ForeignKey("questions.ques_id", ondelete="CASCADE"),
        nullable=True,
        index=True
    )

    ans_id: Mapped[int | None] = mapped_column(
        ForeignKey("answers.ans_id", ondelete="CASCADE"),
        nullable=True,
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    comment: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="active",
        server_default="active",
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    # Constraints

    __table_args__ = (
        CheckConstraint(
            "(ques_id IS NOT NULL AND ans_id IS NULL) OR "
            "(ques_id IS NULL AND ans_id IS NOT NULL)",
            name="ck_comment_single_target"
        ),

        CheckConstraint(
            "status IN ('active', 'hidden', 'deleted')",
            name="ck_comment_status"
        ),
    )

    # Relationships

    user: Mapped["User"] = relationship(
        back_populates="comments"
    )

    question: Mapped["Question | None"] = relationship(
        back_populates="comments",
        foreign_keys=[ques_id]
    )

    answer: Mapped["Answer | None"] = relationship(
        back_populates="comments",
        foreign_keys=[ans_id]
    )


# ==================================================
# 6. SHARE TABLE
# ==================================================

class Share(Base):

    __tablename__ = "shares"

    share_id: Mapped[int] = mapped_column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
        autoincrement=True
    )

    ques_id: Mapped[int | None] = mapped_column(
        ForeignKey("questions.ques_id", ondelete="CASCADE"),
        nullable=True,
        index=True
    )

    ans_id: Mapped[int | None] = mapped_column(
        ForeignKey("answers.ans_id", ondelete="CASCADE"),
        nullable=True,
        index=True
    )

    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.user_id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    # Constraints

    __table_args__ = (
        CheckConstraint(
            "(ques_id IS NOT NULL AND ans_id IS NULL) OR "
            "(ques_id IS NULL AND ans_id IS NOT NULL)",
            name="ck_share_single_target"
        ),
    )

    # Relationships

    user: Mapped["User | None"] = relationship(
        back_populates="shares"
    )

    question: Mapped["Question | None"] = relationship(
        back_populates="shares",
        foreign_keys=[ques_id]
    )

    answer: Mapped["Answer | None"] = relationship(
        back_populates="shares",
        foreign_keys=[ans_id]
    )