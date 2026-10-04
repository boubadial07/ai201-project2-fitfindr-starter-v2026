# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

FitFindr is a thrift-shopping assistant that helps a user find a clothing item,
style it with their existing wardrobe, and create a short fit-card caption.

The user enters a natural-language request such as:

`vintage graphic tee under $30`

FitFindr:
1. Parses the request into a description, size, and maximum price.
2. Searches the thrift listings for matching items.
3. Selects the best matching listing.
4. Suggests one or two outfits using the user's wardrobe.
5. Creates a short social-media-style fit card.

If no listings match the request, the agent stops after the search and tells the
user what they can change instead of continuing to the outfit and fit-card steps.

## Tool Inventory

### `search_listings`

**What it does:** Searches the thrift listings for items matching the user's
description and optional filters.

**Inputs:**
- `description: str` — keywords describing the item.
- `size: str | None` — optional requested size.
- `max_price: float | None` — optional maximum price, inclusive.

**Returns:** A list of matching listing dictionaries, ranked by keyword
overlap and limited by `config.SEARCH_RESULT_LIMIT`.

**When nothing matches:** Returns an empty list `[]`.

For size matching, the search accepts an exact size or a size component such as
`M` in `S/M`, rather than using a naive substring test.

### `suggest_outfit`

**What it does:** Uses the model to suggest one or two outfits for the selected
thrift item.

**Inputs:**
- `new_item: dict` — the selected listing.
- `wardrobe: dict` — the user's wardrobe, containing an `items` list.

**Returns:** A non-empty string containing outfit suggestions.

**When the wardrobe is empty:** Returns general styling advice for the new item
instead of failing or returning an empty string.

### `create_fit_card`

**What it does:** Uses the model to create a short social-media-style caption
for the selected item and outfit.

**Inputs:**
- `outfit: str` — the outfit suggestion.
- `new_item: dict` — the selected listing.

**Returns:** A two-to-four sentence fit-card caption mentioning the item, price,
and platform.

**When there is no outfit:** Returns a descriptive message instead of calling
the model.

## Planning Loop

The planning loop is implemented in `agent.py`.

The flow is:

`user query → parse query → search_listings → branch → suggest_outfit → create_fit_card`

The query parser uses regular expressions to extract:
- the maximum price from values such as `$30`
- the size from phrases such as `size M`

The remaining text becomes the item description.

After `search_listings()` runs, the agent checks the returned list.

**If results are found:**
1. The first result is stored in `session["selected_item"]`.
2. That same selected item is passed to `suggest_outfit()`.
3. The outfit suggestion is stored in session state.
4. `create_fit_card()` receives the outfit and the same selected item.
5. The completed session is returned.

**If no results are found:**
- `session["error"]` is set with a message explaining what the user can
  change.
- The session is returned immediately.
- `suggest_outfit()` and `create_fit_card()` are not called.

The loop also calls `trace.check_iterations()` to enforce the configured
maximum iteration count.

## Sample Run

### Successful search

Command:

```text
python app.py ask 'vintage graphic tee under $30'

Output:

```text
Found: Y2K Baby Tee — Butterfly Print — $18.0 on depop

Outfit:
Two outfit ideas were generated using pieces from the user's wardrobe,
including baggy dark-wash jeans, a black cropped zip hoodie, chunky white
sneakers, and a black crossbody bag.

Fit card:
The generated caption described the Y2K Butterfly Baby Tee as an $18.00
Depop find and suggested styling it with baggy denim or wide-leg trousers.

search_listings
Command:
python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"

The test returned matching listings under the $30 price ceiling, including
the Y2K Baby Tee, Graphic Tee, and other listings containing graphic-tee
keywords.

suggest_outfit

Command:
python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"

The test returned a complete outfit suggestion for the Vintage Levi's 501 Jeans,
using pieces from the example wardrobe.

The empty-wardrobe test also returned general styling advice instead of an
empty response.

create_fit_card

Command:
python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"

The test returned a short social-media-style caption mentioning the Levi's 501s,
the $38.00 price, and Depop.

The empty-outfit test returned:
No outfit suggestion was provided, so a fit card could not be created.

---


## How I Used AI

I used AI as a development assistant while building FitFindr. I used it to help
interpret the project requirements, reason about the planning-loop structure,
review implementation ideas, and debug test results.

I still tested the tools and agent locally using the provided commands and
checked the returned results against the project requirements and my acceptance
criteria.

### Moment 1

- **What I asked for:** Help implementing and testing the three required tools
  one at a time while following their required inputs, outputs, and empty cases.
- **What came back:** Implementation suggestions for `search_listings`,
  `suggest_outfit`, and `create_fit_card`, along with commands for testing both
  normal and edge-case behavior.
- **What I changed:** I implemented the three functions in `tools.py` and
  tested each one locally, including size/price filtering, an empty wardrobe,
  and an empty outfit.

### Moment 2

- **What I asked for:** Help wiring the planning loop so the selected listing
  would move through the session state and the agent would stop when no
  listings were found.
- **What came back:** A planning-loop structure using query parsing, session
  state, a no-results branch, and the three tools in sequence.
- **What I changed:** I implemented the loop in `agent.py`, tested successful
  searches and the no-results case, and verified that the no-results path
  stopped before the outfit and fit-card tools were called.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```

```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```

```

**Empty search**

```

```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
