@automation @increment @operational
@actor:pm-steward @actor:orchestrator @actor:worker @actor:integrator
Feature: Automated increment orchestration
  Scheduled agents need to turn approved objectives into phase-level progress without manual command handoffs.

  Scenario: Agent receives one verification result and next action
    Given a scheduled workflow driver starts from objectives, specs, Beads tickets, claims, and git state
    When the automation loop verifies the current role profile
    Then the agent receives one pass or fail summary with failed checks and the next safe action
    And the operational record includes git status, review gate state, Beads readiness, and validation evidence

  Scenario: Orchestrator reroutes around blocked work
    Given an increment has unblocked ready work and a separate blocked ticket
    When the orchestrator driver selects the next worker action
    Then it assigns only unclaimed unblocked work to a focused worker branch
    And the operational record keeps blocked work visible for the PM review loop instead of idling the increment

  Scenario: Integrator stops at a human increment gate
    Given all child tickets for a spec phase are complete and verified
    When the integrator driver evaluates the feature branch
    Then it prepares the increment for human review rather than merging to main
    And the operational record links the phase evidence, learnings, and review status
