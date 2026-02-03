
# PLEASE READ INFO.md

For details on set up, details, and replies to questions, see INFO.md

# Coding Test for tails.com


## Overview

We're excited to see how you approach building quality software! Think of this as creating an open source project you'd be proud to share on GitHub. 

**Time commitment:** Minimum 90 minutes (feel free to spend more time if you'd like)

**What we're looking for:** High-quality code with great architecture, clear decision-making, and thoughtful implementation.  We value understanding over speed, so avoid frameworks that do all the heavy lifting for you.

**Show us how you think** through clear naming, comments, tests, and architectural choices. 

## Instructions

### 1. Set Up Your Application

Create a Docker container with a Python-based application. We prefer FastAPI, but any framework works. 

### 2. Build Your Features

Choose the track that matches your role:

#### Backend Software Engineer Track

* Render stores from `stores.json` in alphabetical order
* Integrate with [Postcodes.io](https://postcodes.io) to fetch and display latitude/longitude for each store's postcode
* Build functionality to return stores within a given radius of a UK postcode, ordered north to south. This function should include unit tests.

#### Full Stack Software Engineer Track

**Backend:**
* Create an API that searches stores from `stores.json` (e.g., searching "hav" returns "Newhaven")
* Order results by matching postcode first, then city name (e.g., "br" shows "Orpington" (BR5 3RP) before "Bracknell")
* Include unit tests

**Frontend (using Vue or React preferred):**
* Build a search interface with a text field and results list
* Add type-ahead suggestions with 100ms debounce (minimum 2 characters)
* Display 3 results initially, lazy load more on scroll

### 3. Submit Your Work

* Zip your code (max 10MB) and upload via the "Show Questions" button in your email
* Include a text file with answers to:
  1. Which track did you complete? (backend or full-stack)
  2. What would you do differently with more time?
  3. What was the hardest part?  What are you most proud of?  Why?
  4. How could we improve this test?

---

Good luck!  We're looking forward to seeing your work.  🚀
