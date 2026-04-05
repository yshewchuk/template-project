# Improve Loop

## Purpose

Conduct a retrospective on a completed milestone and implement process improvements based on observed outcomes.

## Trigger

A milestone is completed: all PRs are merged and all acceptance tests pass.

## Output

An Improvement PR containing:
- Updated persona definitions (if role boundaries were unclear)
- Updated loop workflows (if stage sequences were suboptimal)
- Updated planning schemas (if YAML structure caused confusion)
- Updated `OWNERS.yaml` (if ownership boundaries need adjustment)
- Updated guides and documentation
- Retrospective notes documenting findings and rationale

## Flow

The Improve loop has the same structure in Phase 1 and beyond, since the Scrum Master is a dedicated role from day one.

```
Milestone complete (all PRs merged, acceptance tests passing)
    |
    v
[Scrum Master] -- review all PRs, threads, and CI logs
               -- identify bottlenecks and failures
               -- propose and implement process improvements
    |
    v
[Product Manager] -- review against product workflow
    |
    v
[Tech Lead] -- review against technical workflow
               (Phase 1: also covers Architect + Security review)
    |
    v
Improvement PR -> merge
```

## Stage Sequence

### Phase 1

| # | Stage | Persona | Type |
|---|-------|---------|------|
| 1 | Retrospective & improvements | Scrum Master | contribute |
| 2 | Product workflow review | Product Manager (human) | review |
| 3 | Technical workflow review | Tech Lead | review |

### Full Team (Phase 2+)

| # | Stage | Persona | Type |
|---|-------|---------|------|
| 1 | Retrospective & improvements | Scrum Master | contribute |
| 2 | Product workflow review | Product Manager (human) | review |
| 3 | Architecture workflow review | Architect | review |
| 4 | Security workflow review | Security Engineer | review |
| 5 | Technical workflow review | Tech Lead | review |

## Scrum Master Checklist

When executing this loop:

### Data Collection
- [ ] Review all PR threads from the completed milestone
- [ ] Review CI/CD logs for recurring failures or slow feedback
- [ ] Review review iteration counts (how many rounds before approval?)
- [ ] Identify instances where humans had to manually intervene
- [ ] Note any ownership conflicts or ambiguities

### Analysis
- [ ] Categorize issues: process, tooling, documentation, or persona
- [ ] Identify root causes (not just symptoms)
- [ ] Prioritize by impact: which changes would most reduce human intervention?

### Improvements
- [ ] Update persona definitions if role boundaries were unclear
- [ ] Refine loop stage sequences if they were suboptimal
- [ ] Adjust planning schemas if YAML structure caused confusion
- [ ] Update `OWNERS.yaml` if ownership boundaries need adjustment
- [ ] Improve context extraction if agents had insufficient or excessive context
- [ ] Update `docs/guides/onboarding.md` with lessons learned
- [ ] Update root `README.md` if repository structure changed
- [ ] Update root `CLAUDE.md` if universal rules need refinement

### Documentation
- [ ] Write retrospective notes with evidence-backed findings
- [ ] Document each change's rationale
- [ ] Flag any changes that are experimental and should be re-evaluated next milestone

## Metrics to Track

| Metric | Source | What It Indicates |
|--------|--------|-------------------|
| Review iteration count | PR threads | Clarity of implementation guidance |
| PR size (lines) | Git diffs | Plan decomposition quality |
| Time between stages | PR timestamps | Workflow efficiency |
| CI failure rate | CI logs | Build/test reliability |
| Human intervention count | PR comments | Agent autonomy level |
| Context extraction usefulness | Agent feedback | Information architecture quality |

## Backwards Compatibility

Process changes must be backwards-compatible:
- Schema changes must not invalidate existing valid YAML without a documented migration
- Persona changes must preserve the ownership invariant
- Loop changes must not break existing GitHub Actions workflows without updating them

## Labels

- `stage/scrum-master` -- Scrum Master contributing improvements
- `stage/review-product-manager` -- PM reviewing
- `stage/review-tech-lead` -- Tech Lead reviewing
