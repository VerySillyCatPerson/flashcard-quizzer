# Authoritative audit request and rubric

Supplied by the student on 2026-11-19. The text below is preserved verbatim; its mandatory rubric and 1,000-1,500-word limit govern the current audit. Optional suggestions are not submission requirements.

```text
Perform the final audit of the current repository against the authoritative rubric included below.

Inspect the actual files. Earlier stage summaries support the audit but do not replace repository evidence. Do not commit, push, publish, or submit.

AUDIT OUTPUT

For each mandatory requirement, report:
- PASS, PARTIAL, FAIL, or UNVERIFIED.
- Exact evidence: repository paths, relevant sections or test names, and saved verification results.
- Any gap, its consequence, and the smallest correction needed.

Distinguish mandatory requirements from optional suggestions. Do not add features, dependencies, patterns, external APIs, or performance work to pursue optional suggestions.

SPECIFIC CHECKS

1. AI collaboration and review

Verify that:
- AI generated application code.
- All AI-generated code was reviewed using the provided checklist. Inspect actual checklist coverage; passing tests alone do not establish review.
- ai_edit_log.md contains specific prompts, AI responses, review decisions, and modifications or rejections.
- At least five meaningful interactions are documented. Identify five concrete examples and explain the decision or correction each produced.
- Recorded defects and fixes have genuine evidence, including F1/F2 and their failing-before/passing-after regressions.
- The log distinguishes AI recommendations, student decisions, automated verification, and manual observations.
- No human review, personal reflection, or manual test result has been invented.

2. Application and features

Verify that:
- The application meaningfully extends the starter and has a clear purpose.
- At least three distinct features beyond basic CRUD are implemented. Inspect persistent adaptive learning, seeded random sessions, and optional JSON export against code, tests, and README.
- Those features work through the actual CLI entry point.
- AI assistance throughout development is documented.

Do not count one feature multiple times or treat supporting implementation details as separate features without justification.

3. Design pattern

Verify that:
- At least one implemented pattern appears in the provided design-pattern guide.
- Strategy is actually listed in that guide.
- Its use for interchangeable quiz modes serves a real purpose.
- The final report accurately explains its implementation and why it was chosen.

Do not add patterns merely to satisfy optional suggestions.

4. Code quality

Inspect:
- PEP 8 compliance and the configured formatting, linting, and typing checks.
- Readability, maintainability, validation, and error handling.
- Whether functions have appropriate docstrings; lint success alone does not prove this.
- Whether expected failures are handled narrowly and unexpected programming errors remain visible.
- Whether quality rules, assertions, or coverage exclusions were weakened to obtain passing results.

5. Testing and coverage

Verify that:
- pytest coverage exceeds 80% across all production modules, including main.py.
- Tests cover original implemented behavior and AI-generated additions.
- Edge cases and error conditions are covered.
- Test names describe the behavior being tested.
- Saved coverage evidence corresponds to the final application source.

Report statement coverage, branch coverage, and combined coverage separately, with covered/total counts and the measurement command.

Preserve these distinctions:
- Injected KeyboardInterrupt is not physical Ctrl+C verification.
- Hard-link checks do not establish actual symlink traversal.
- Grammar/static checks are not runtime compatibility tests.
- Clean Windows Python 3.10.11 and 3.13.17 runs were reported; inspect their actual saved evidence.

6. Documentation and report

Verify that:
- final_report.md uses the supplied official template.
- Its length is 1,000–1,500 words. State the counting method and whether headings, tables, and appendices are included.
- It explains AI use throughout development, decisions, lessons learned, limitations, and the design-pattern choice.
- Reflections and self-assessment ratings match what I actually supplied or accepted.
- README describes current features, dependencies, installation, and working usage examples.
- Relative documentation links resolve.
- No relevant placeholders or stale verification claims remain.

The rubric below resolves the previous report-length conflict:
- 1,000–1,500 words is authoritative.
- Preserve the original official template.
- Update current documentation so the full rubric and report-length decision are no longer described as unresolved.
- Preserve historical log entries and append a dated resolution instead of rewriting history.

Do not record final report wording as approved unless I explicitly approve it.

7. Submission contents and hygiene

Inspect the actual proposed submission inventory, not just .gitignore.

Verify that it contains:
- Required application source.
- Tests.
- Required sample decks.
- Setup and usage documentation.
- ai_edit_log.md.
- The final report.
- Coverage evidence.
- Code-quality verification evidence.

Verify that credentials, private keys, real learning history, virtual environments, caches, and personal session files are excluded. Preserve required synthetic fixtures and submission evidence.

Confirm that evidence referenced by the report and log remains accessible within the proposed submission.

CHANGE AND VERIFICATION BOUNDARIES

Reuse valid verification evidence where application code, tests, configuration, and dependencies are unchanged. Do not repeat the entire suite solely because documentation changed.

You may make necessary factual documentation corrections, repair broken links, resolve stale pending-rubric notes, and correct submission-inventory issues within the agreed scope.

If you discover a necessary application-code change:
- Present the confirmed defect, reproduction, consequence, and proposed fix.
- Stop before implementing that fix for my review.
- After approval, preserve regression evidence and rerun affected checks.

Do not manufacture retrospective checklist reviews. If an actual checklist review is missing, perform it now and record its real date and scope.

Record this request, changes, checks, results, and unresolved items in ai_edit_log.md. Preserve historical findings.

FINAL RESPONSE

Finish with:
1. A requirement-by-requirement audit.
2. Mandatory requirements passed and remaining gaps.
3. A concrete inventory of files/directories to submit.
4. Whether each unresolved item blocks an explicit rubric requirement, with reasons.
5. Any action still required from me, including report approval or manual observations.

Do not treat an unperformed optional verification as an automatic rubric failure. Explain its actual relevance.

Stop for my review. Do not commit, push, publish, or submit.

AUTHORITATIVE RUBRIC

AI COLLABORATION AND CODE REVIEW

AI Code Review — Submission Requirements:
- Use AI tools to generate code for your application.
- Review all AI-generated code using the provided checklist.
- Document your review process in ai_edit_log.md with specific examples.
- Show evidence of modifying or rejecting poor AI suggestions.

Code Quality Standards — Submission Requirements:
- All code follows PEP 8 style guidelines.
- Proper error handling and input validation.
- Code is readable and maintainable.
- Functions have appropriate docstrings.

APPLICATION DEVELOPMENT

Functional Application — Submission Requirements:
- Build a working application that extends the starter code.
- Implement at least 3 new features beyond basic CRUD operations.
- Application should have clear functionality and purpose.
- Use AI assistance throughout the development process.

Design Patterns — Submission Requirements:
- Implement at least 1 design pattern from the provided guide.
- Pattern should serve a real purpose, not be forced.
- Document why you chose the pattern in your final report.

TESTING AND QUALITY ASSURANCE

Unit Testing — Submission Requirements:
- Achieve >80% test coverage using pytest.
- Write tests for both original and AI-generated code.
- Include tests for edge cases and error conditions.
- Use clear test names that describe what is being tested.

AI-Generated Code Validation — Submission Requirements:
- Test all AI-generated code thoroughly.
- Document any issues found with AI code in ai_edit_log.md.
- Show evidence of fixing or rejecting problematic AI suggestions.

DOCUMENTATION AND COMMUNICATION

AI Interaction Log — Submission Requirements:
- Complete detailed ai_edit_log.md with specific examples of AI usage.
- Document prompts you used and AI responses you received.
- Explain your decision-making process for accepting/rejecting AI suggestions.
- Include at least 5 meaningful AI interactions.

Final Report — Submission Requirements:
- Complete the final report using the provided template.
- Explain how you used AI throughout your development process.
- Reflect on what you learned about working with AI tools.
- Report should be 1000–1500 words.

README Updates — Submission Requirements:
- Update README.md with new features and setup instructions.
- Provide clear usage examples.
- Document any dependencies or installation requirements.

SUGGESTIONS TO MAKE YOUR PROJECT STAND OUT — OPTIONAL

- Implement multiple design patterns that serve real purposes in your application.
- Create a comprehensive test suite with >90% coverage including edge cases.
- Add advanced features like configuration management, logging, or data export capabilities.
- Write detailed AI interaction analysis showing sophisticated understanding of AI strengths and weaknesses.
- Implement security best practices including input validation and error handling.
- Create professional documentation that would help other developers understand your AI collaboration process.
- Add performance optimizations and document your decision-making process.
- Include integration with external APIs or services using AI assistance.
- Develop custom utilities or helper functions that extend the starter code meaningfully.
- Create visual documentation like diagrams or flowcharts explaining your application architecture.

SUBMISSION CHECKLIST

- Complete codebase with all source files, tests, and documentation.
- Completed ai_edit_log.md with at least 5 detailed AI interaction examples.
- Final project report using the provided template (1000–1500 words).
- Updated README.md with current setup instructions and feature descriptions.
- Test coverage report demonstrating >80% coverage.
- Code quality verification: all linting tools should pass without errors.
```
