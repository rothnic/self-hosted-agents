@operator-workbench @review @handoff @operational
@actor:project-owner @actor:operator @actor:reviewer @actor:scheduled-agent
Feature: Operator workbench review UX
  Operators need a repo-backed workbench contract for status, evidence, review decisions, and handoffs.

  Scenario: Project owner inspects decision status from repo evidence
    Given an operator opens the workbench driver from current goals, specs, Beads, claims, and validation evidence
    And the driver can inspect repo-local trace, eval, branch, PR, report, and review evidence when available
    When the operator requests decision status
    Then the project owner sees the active objective, current goal and spec, Beads work state, validation state, and next owner
    And the operational observations link source artifacts with explicit GitHub and self-hosted Langfuse fallback state

  Scenario: Independent reviewer records durable decisions
    Given presenter evidence exists for a ticket, increment, or goal
    When an independent reviewer accepts, rejects, defers, or asks a question through the workbench driver
    Then the operator sees reviewer id, verdict, evidence checked, findings, follow-up routing, and human-required status
    And the operational observations preserve human-required only for user-reserved, missing, or contradictory decisions

  Scenario: Scheduled agents receive concise handoffs
    Given a scheduled agent or local session needs to resume work from the workbench driver
    When the driver emits a handoff summary
    Then the next agent receives the next ticket or role, required files, validation commands, risks, and exact artifact handles
    And the operational observations prove no hosted/cloud credentials or prior chat context are required
