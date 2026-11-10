# REGRET
### An Anonymous Question & Answer Platform

REGRET is a platform designed to give people a space to ask questions, share personal thoughts, and express experiences without the pressure of revealing their identity.

It allows people to publish questions anonymously and lets others respond to those questions through anonymous answers. The goal is to create an environment where people can openly express themselves, share perspectives, and learn from the experiences of others.

---

## 1. The Idea Behind REGRET

People often have questions, thoughts, experiences, or regrets that they hesitate to share publicly because of social pressure, fear of judgment, or privacy concerns.

REGRET aims to make sharing easier by providing an anonymous question-and-answer environment.

For example:

- Someone wants to ask: "What is one decision you wish you could change?"
- Another person wants to know: "How did you overcome your biggest failure?"
- Someone may want to share a personal experience without disclosing their identity.

REGRET provides a platform where these conversations can happen without requiring people to publicly associate their identity with their contributions.

## 2. Core Concept

The platform is built around two primary entities:

**Question:** A user submits a question to the platform. The question can be associated with a registered account or submitted anonymously.

**Answer:** Other users can respond to an existing question. Each answer belongs to a specific question and can also be submitted anonymously.

The relationship is:

```text
                  REGRET PLATFORM
                         |
                         |
                    QUESTION
                         |
              ---------------------
              |         |         |
           Answer 1  Answer 2  Answer 3
              |         |         |
           Anonymous Anonymous Anonymous
```

A question can have multiple answers, but every answer must belong to an existing question.

## 3. Key Features

### Core Features

- **Anonymous Question Creation:** Users can submit questions without associating them with a registered account.
- **Anonymous Answers:** People can answer questions without revealing their identity.
- **Question-Based Discussions:** Every answer is connected to a particular question.
- **Public Question Discovery:** Users can explore questions shared on the platform.
- **Question and Answer Viewing:** Users can read questions and their associated answers.

### Planned Platform Features

The platform's data model also considers additional capabilities:

- User registration and authentication.
- User profiles.
- Likes on questions and answers.
- Comments and discussions.
- Sharing questions and answers.

These features can be introduced as the platform evolves.

## 4. How REGRET Works

The intended user journey is straightforward:

1. A person visits REGRET.
2. They explore existing questions or submit a new question.
3. Other people discover that question.
4. Interested people submit answers.
5. The platform stores each answer against its corresponding question.
6. People can read the responses and learn from different perspectives.

### Example Interaction

**Question:**

"What is one thing you regret not doing when you were younger?"

**Possible Answers:**

- "I regret not spending enough time with my family."
- "I wish I had taken more risks in my career."
- "I regret not learning new skills earlier."

The purpose is to encourage honest expression and meaningful interaction.

## 5. System Architecture

REGRET follows a backend-driven architecture. The client communicates with the backend through REST APIs, while the backend handles validation, application logic, and database operations.

### High-Level Architecture

```text
                 USER
                  |
                  |
          Web / Mobile Client
                  |
                  |
              HTTP Request
                  |
                  v
          +----------------+
          |   FastAPI      |
          |   API Layer    |
          +----------------+
                  |
                  v
          +----------------+
          |    Routers     |
          |                |
          | Question APIs  |
          | Answer APIs    |
          +----------------+
                  |
                  v
          +----------------+
          |    Schemas     |
          |                |
          | Validation     |
          | Request/Output |
          +----------------+
                  |
                  v
          +----------------+
          |   SQLAlchemy   |
          |   ORM Layer    |
          +----------------+
                  |
                  v
          +----------------+
          |    Database    |
          |                |
          |    SQLite      |
          +----------------+
```

### Architecture Components

| Component | Responsibility |
|---|---|
| Client | Provides the interface through which users interact with REGRET |
| FastAPI | Receives HTTP requests and returns API responses |
| Routers | Handle specific application endpoints |
| Pydantic Schemas | Validate incoming data and define response structures |
| SQLAlchemy ORM | Converts application operations into database queries |
| Database Models | Define the structure and relationships of stored data |
| Database | Persistently stores platform information |

The architecture separates API handling, validation, database operations, and data storage to keep the backend organized and maintainable.

## 6. Database Architecture

The initial relational database design consists of six main entities.

### Entity Overview

| Entity | Purpose |
|---|---|
| Users | Stores registered user information |
| Questions | Stores questions submitted to the platform |
| Answers | Stores responses to questions |
| Likes | Records likes on questions and answers |
| Comments | Stores comments associated with questions or answers |
| Shares | Records sharing activity |

### Entity Relationships

```text
                  USERS
                    |
          ---------------------
          |         |         |
       Questions  Answers   Likes
          |         |         |
          |         |         |
          +---- QUESTIONS    |
                   |          |
                   |          |
                 ANSWERS      |
                   |          |
          ---------------------
          |                   |
       COMMENTS             SHARES
```

The primary relationships are:

- A user can create multiple questions.
- A user can submit multiple answers.
- A question can contain multiple answers.
- An answer belongs to exactly one question.
- Likes can reference either a question or an answer.
- Comments can reference either a question or an answer.
- Shares can reference either a question or an answer.
- User association is optional for anonymous questions and answers.

The database uses foreign keys to maintain relationships between records.

## 7. Technology Stack

| Technology | Role |
|---|---|
| Python | Backend programming language |
| FastAPI | REST API framework |
| SQLAlchemy | Database ORM |
| SQLite | Initial relational database |
| Pydantic | Data validation and serialization |
| Uvicorn | ASGI application server |
| python-dotenv | Environment configuration |

The initial backend is developed using Python and FastAPI. SQLite is used as the development database, with the database layer structured around SQLAlchemy.

## 8. API Architecture

REGRET exposes REST endpoints to allow clients to interact with the platform.

### Question APIs

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/question` | Create a question |
| GET | `/questions/` | Retrieve questions |
| GET | `/questions/{ques_id}` | Retrieve a specific question |

### Answer APIs

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/question/{ques_id}/answer` | Submit an answer to a question |

### System API

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health/` | Check API availability |

API documentation is available through FastAPI's Swagger UI
## 10. Privacy and Anonymity

Anonymity is an important part of REGRET's design.

The initial system supports contributions without requiring a registered user ID. The database allows the user association for questions and answers to be empty.

This means:

- A question can exist without a registered user association.
- An answer can exist without a registered user association.
- Answers remain linked to their respective questions.

**Privacy consideration:** Anonymous contributions should not expose account identity through public API responses. Anonymity at the application level does not automatically guarantee complete network or infrastructure-level anonymity.

## 11. Future Scope

REGRET can evolve into a broader social discussion platform.

Potential future improvements include:

- Secure user authentication and account management.
- User profiles and contribution history.
- Like and comment systems.
- Question and answer sharing.
- Search and filtering.
- Content moderation and reporting.
- Frontend web application.
- Mobile-friendly experience.
- Deployment and production database infrastructure.

These additions will build upon the core question-and-answer architecture.

## 12. Project Vision

REGRET aims to create a place where people can ask what they hesitate to ask, share what they hesitate to share, and learn from experiences beyond their own.

**Ask freely. Answer honestly. Stay anonymous.**

---

*REGRET – An Anonymous Question & Answer Platform.*