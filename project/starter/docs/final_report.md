# AI-Assisted Development Project Report

**Student Name:** `A***** P*****`  
**Project Title:** Flashcard Quizzer CLI  
**Date:** 2026-11-19 — approved report

## Executive Summary

The Flashcard Quizzer loads validated JSON decks, asks each card once, evaluates text answers, and reports accuracy and missed terms. Sequential, seeded random, and adaptive modes share an engine. Persistent error-balance history and optional JSON results extend the core quiz.

Development used ChatGPT/Codex through separately reviewed stages. The student questioned design choices and accepted stages based on explanations and reported evidence. Codex executed the recorded checks; acceptance does not imply independent Python inspection or physical terminal verification.

## Project Overview

### Problem Statement

Learners need repeatable practice and useful feedback without losing progress when deck files move. Invalid input and interrupted sessions should produce understandable outcomes while preserving completed answers.

### Solution Approach

Python 3.10 is the minimum target. Runtime dependencies are entirely standard-library modules; pip and venv isolate development tools. Frozen dataclasses represent cards and summaries, while Protocol defines a structural Strategy interface. As with TypeScript interfaces, annotations describe contracts without validating untrusted JSON.

### Final Features

- Core: validated decks, finite quizzes, feedback, and partial statistics.
- Addition 1: persistent adaptive learning changes future priority across sessions.
- Addition 2: seeded random sessions reproduce an order independently of history.
- Addition 3: optional JSON session export provides metadata, statistics, and missed cards.

## AI Collaboration Experience

### AI Tools Used

ChatGPT/Codex generated and refined implementation, tests, explanations, and documentation. No other assistant is claimed.

### Collaboration Workflow

Requests specified scope, behavior, evidence, and a stopping point. Follow-up questions challenged identity, duplicates, scoring, persistence, exports, and interruption behavior. Design proposals were distinguished from accepted decisions. Stage 7 presented reproduced defects before edits; approved corrections began with failing regressions. An item-by-item Codex checklist review was performed on November 19; it is not claimed as earlier human review.

### Most Valuable AI Interactions

These are documented examples rather than a student-ranked list.

#### Example 1: Durable identity and useful priority

**Context:** History initially depended on paths and cumulative mistakes.  
**AI Prompt:** Explain moves, edits, duplicates, and decreasing scores.  
**AI Response:** Proposed content identity and error balance.  
**Your Changes:** Student review rejected path dependence, front-only uniqueness, and optional context.  
**Outcome:** Normalized front/back JSON pairs are hashed; identical cards share history. Incorrect adds one, correct subtracts one with a zero floor.

#### Example 2: F1 interruption between phases

**Context:** A boundary interruption skipped pending persistence.  
**AI Prompt:** Reproduce, test first, and prevent repeated committed updates.  
**AI Response:** Added failing entry-point regressions and phase tracking.  
**Your Changes:** Student approval required uncertain writes not be blindly retried.  
**Outcome:** Pending work resumes with status 130; observed history attempts remain one.

#### Example 3: F2 failed terminal output

**Context:** Summary failure skipped writes and changed interruption status.  
**AI Prompt:** Preserve saving/export and statuses after expected output errors.  
**AI Response:** Added closed-pipe regressions and narrow terminal error handling.  
**Your Changes:** Review required independence and visible programming errors.  
**Outcome:** EOF/interruption retain 1/130. A further regression caught shutdown status 120; retiring the failed descriptor corrected it.

### Challenges with AI Collaboration

High coverage initially missed combined failure scenarios. An oversized-integer decoder exception also required a narrow fix. A test-bootstrap delimiter mistake was corrected before valid regression results were interpreted. These failures and corrections remain recorded.

## Software Engineering Practices

### Code Quality Measures

Black, isort, flake8, strict mypy, typed functions, docstrings, and structured errors support review. Final inspection found eight missing bootstrap docstrings, eight spacing errors, and F3: failed startup-warning output replaced interrupt status 130 with 1. Approved corrections followed failing regressions. File-level and extracted-bootstrap lint now pass without weakened rules; unexpected programming errors remain visible.

Independent review prompted portable nesting tests and C0/DEL/C1 display escaping; readable Unicode and domain data remain unchanged.

### Testing Strategy

Pytest covers validation, immutable snapshots, source preservation, scoring, temporary-file round trips, persistence failures, exports, conflicts, and actual-entry-point subprocesses. Random tests check membership without requiring a changed shuffle. Stage 7 used regression-first development; this is not a claim that all development followed test-driven development.

### Design Patterns Used

Strategy is listed in the supplied guide, section 1. It was chosen so ordering can change without rewriting grading or progress. QuizStrategy defines a structural Protocol; CLI composition selects an implementation, and the engine requests its permutation once. Persistence and terminal effects remain separate.

### Code Structure and Organization

main.py delegates execution. Models/loading define validated data; engine/strategies manage sessions; history owns score updates and persistence; paths validate file roles; terminal formats output; export builds result documents; CLI coordinates them.

## Technical Challenges and Solutions

### Challenge 1: Persistence without unnecessary infrastructure

**Problem:** Renaming decks should preserve progress, and learned cards should lose priority.  
**Solution:** Canonical normalized JSON pairs produce content hashes; stable sorting uses decreasing error balance.  
**AI Involvement:** Compared alternatives and tested serialization boundaries and cross-deck sharing.  
**Lessons Learned:** Content identity trades edit continuity for simple shared history; this is a documented design consequence.

### Challenge 2: Uncertain commits and failed displays

**Problem:** An interrupted replacement may already have committed, while printing can fail independently.  
**Solution:** Finalization marks attempts before invocation and continues pending phases. Only terminal write/flush errors are translated.  
**AI Involvement:** Preserved before/after evidence, including real replacement followed by interruption.  
**Lessons Learned:** An exception does not prove noncommit. Tests observe scores and attempt counts, while formatting RuntimeError remains visible.

## Code Quality Analysis

### Metrics

Production comprises 11 Python files, 1,167 physical lines including blanks/docstrings, 62 function definitions including methods, and 22 classes. Tests comprise 13 files and 2,764 physical lines. These are size measures, not authorship counts.

Post-review Windows CPython 3.10.11 and 3.13.17 runs each passed 343 tests with one skip, using the previously isolated environments against current source. Combined coverage is 98.21%; statements are 595/604, or 98.51%, and branches are 120/124, or 96.77%. All configured quality checks passed; Linux/Python 3.12 was not executed.

### Self-Assessment

Student-supplied Stage 8 ratings are unchanged. Factual reasons below reflect subsequent verification; original reasons remain in the interaction log.

- **Readability: 4/5.** Clear modules and typed models; finalization/stream handling need careful reading.
- **Maintainability: 4/5.** Engine, storage, and presentation are separated; interruption complexity is documented.
- **Test Quality: 4/5.** Strong behavioral and subprocess regressions; Windows Python 3.10.11 and 3.13.17 runtime checks passed. Physical Ctrl+C and actual symlinks remain unverified.
- **Documentation: 4/5.** Detailed instructions and evidence; clean reproduction and the authoritative rubric audit are complete. Final report wording is approved; the physical test result remains pending.

## Learning Outcomes

### Technical Skills Developed

I learned that Python annotations do not validate JSON at runtime, much like TypeScript types. Protocols resemble structural interfaces.

### AI Collaboration Skills

I challenged path-based history identity, cumulative scoring, unnecessary raw export answers, and automatic result replacement. Explanations and evidence helped me assess Python details I could not independently evaluate.

### Software Engineering Insights

I learned why high coverage does not guarantee correct behavior across failure scenarios. F1/F2 provided concrete examples of the distinction.

## Reflection

### What Worked Well

Pausing between stages gave me manageable decisions to review. The process let me question behavior before accepting it.

### What Could Be Improved

Repeated review rounds were lengthy. Next time, I would provide the full rubric earlier, agree storage/export behavior before implementation, and run manual terminal checks alongside automated tests earlier.

### Future Enhancements

The student supplied no future-feature wish list. Concurrent-session merging is an optional technical possibility requiring a separately agreed design. Current next actions are review and manual verification, not an agreed feature expansion.

## Conclusion

The project demonstrates reviewed AI-assisted implementation with measurable checks and documented limits. My next workflow would establish assessment criteria earlier and combine manual and automated verification sooner. The student accepted F3/bootstrap corrections based on reported regression evidence. Report wording is approved; physical Ctrl+C remains pending; submission is not authorized.

## Appendices

### Appendix A: AI Interaction Log

[The log](ai_edit_log.md) records nine detailed stage entries with grouped follow-ups, including identity/scoring, decoder validation, snapshots, save retries, export refinements, F1/F2, and clean reproduction. This is not a count of chat turns.

### Appendix B: Code Statistics

[The final audit](final_rubric_audit.md) links commands, metrics, checklist findings, and tested-source hashes. The 98.21% combined figure is (595+120)/(604+124); historical zero-statement coverage is not submission evidence.

### Appendix C: Additional Resources

The preserved [official template](report_template.md), [design-pattern guide](design_patterns.md), and supplied [authoritative rubric](authoritative_audit_request.md) provide context. Physical Ctrl+C and real symlink checks remain unverified; they are not explicit rubric requirements. Both runtime checks passed and F3/bootstrap corrections were accepted on reported evidence. Report wording is approved; the agreed manual result remains pending.

---

**Length rule:** The authoritative rubric requires 1,000–1,500 words. The preserved template's 2,000–3,000 footer is superseded, not an unresolved conflict. Due date and submission destination were not supplied.

