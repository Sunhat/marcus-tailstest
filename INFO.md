
# How to run

```
cp .env.example .env
```
Then
```
./develop up
```

Runs on
```
http://localhost:6767
```

To run tests

```
./develop test
```

# Decisions - Set up

### Dockerfile

1. We copy requirements, install pip requirements, copy app, run as appuser, not root.

2. Dynamic APP_PORT, kinda useless feature I guess.

    a. Could add HOST_PORT and make that dynamic instead.
    Does mean you can run this outside Docker on a custom port if you setup venv

3. Hot reloading
    a. I read there's other ways to have hot reloading. Skipped and used --reload

### docker-compose.yml

1. Mount the app
2. Named marcus so it doesn't conflict with other code tests / other containers
3. PYTHONUNBUFFERED=1, so logs are apparently easier to read in Docker
4. No .env COPIED or added as volume attachment. --reload doesn't detect .env changes which is lame. And Docker is injecting .env as env vars anyway.


### No venv

Not necessary because we have Docker. Could be nice to have for personal preference? Apparently IDE hints are improved if we add this? NEEDING venv + Docker smells bad to me?... Maybe there's more to know

### Python

1. Python 3 latest
2. FastAPI because README said you like it
3. Pydantic Models

### AI Usage

AI was used in this project

- To help with Dockerfile construction (simple to do myself, but quicker with AI)
- To help get this code working, initially as functions, and without Pydantic Models
- I pushed AI down the path of helping ensure I have O(1), data validation, Pydantic, Configuration, helping refactor into classes
- AI suggested in-memory store, different namings, and different architecture (folders/files), much of which I rejected
- I chose to use "with PostcodesIO", thought it looked cool
- Used AI to write some of the remedial code. Had to debug tests it wrote and fix them myself.
- Used AI as a teacher for Python syntax and ecosystem.

### 3. Submit Your Work

1. Which track did you complete? (backend or full-stack)

Backend

2. What would you do differently with more time?

Merge search & list to offer one comprehensive call, that can order/sort, search

Consider better architecture
- JSON Reader is also Enricher...
- Do we store enriched results in memory instead of separate JSON?
- If store service would only have one method, does it need to be a class?
- is_within_radius as a separate testable method
- Improve Dockerfile for production-ready (separate FROMs, requirements-dev only locally, etc)
- Maybe a different folder structure?
- PostcodesIO has this __aenter__ stuff, which interfered with testing - need to understand when/how to use this better



3. What was the hardest part?  What are you most proud of?  Why?

Getting to grips with Python syntax, ecosystem, types, pydantic.

Instantiating classes/objects, "with" syntax, 

Proud? I think there's much to learn here, not really sure how good this is... 

Considered building this in Laravel for my own comparison, but out of time

4. How could we improve this test?


---

