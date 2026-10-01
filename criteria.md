# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:**
<!-- Why 4 of 5 and not 5 of 5? Something about your search, probably —
     "my search is a plain keyword match and some phrasings will miss" is a
     real answer. -->

---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:**
<!-- Why is 5 of 5 reasonable here when criterion 1 isn't? What's different
     about this path? -->

---

## 3. Something about state

Given a query that returns at least one listing, `session["selected_item"]` matches the `new_item` received by `suggest_outfit` in at least 4 of 5 runs.

**Why this target:**
This directly checks that the item found by `search_listings` is actually carried through the session state into the next tool. I chose 4 of 5 because the agent depends on the selected result from the search, and one miss would still reveal a state-handling problem without requiring a perfect target.



---

## 4. Something about the fit card

Given a successful run, at least 4 of 5 generated fit cards mention the selected item's title (or identifying item description), price, and platform.

**Why this target:**
The tool specification says the caption should mention the item, price, and platform once each, while allowing the model's wording to vary. I chose 4 of 5 because model-generated wording can vary between runs, so the criterion checks the required content instead of requiring identical text.


---

## 5. Your choice

For 5 queries that specify a maximum price, every returned listing has a price less than or equal to the requested maximum.

**Why this target:**
`max_price` is an explicit input to `search_listings`, so respecting the price ceiling is a behavior I can check directly from the returned listing data. I chose 5 of 5 because a price above the user's stated maximum would be an observable search error.



---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
