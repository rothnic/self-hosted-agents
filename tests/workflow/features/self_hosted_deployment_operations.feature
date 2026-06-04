@deployment @self-hosted @operational
@actor:agent-operator @actor:project-maintainer @actor:reviewer
Feature: Self-hosted deployment operations
  Operators need a reproducible self-hosted deployment profile before the selected agent stack can be promoted.

  Scenario: Operator can inspect reproducible deployment profiles
    Given an agent operator opens the deployment operations driver for the selected stack
    And the driver can inspect repo-local profile, environment, service, and machine evidence
    When the operator requests the local, development-server, and production-like profiles
    Then each profile names the required services, ports, storage paths, secret names, and target machine assumptions
    And the operational observations identify missing prerequisites without exposing or requiring secret values

  Scenario: Maintainer receives correlated deployment smoke evidence
    Given a project maintainer starts the reference deployment profile through the deployment operations driver
    When the maintainer runs the representative selected-stack smoke workflow
    Then the maintainer receives repo-local evidence with run, trace, evaluation, durable, and health correlation
    And the operational observations show whether observability and durable execution are available in that profile

  Scenario: Deterministic validation remains credential-free
    Given the operator runs fixture validation without hosted service credentials
    When the deployment operations driver evaluates the selected-stack profile
    Then deterministic validation completes without requiring a cloud service, external model provider, or hosted token
    And the operational observations preserve unavailable service-backed evidence as explicit follow-up gaps

  Scenario: Reviewer can evaluate recovery readiness
    Given an operator records backup, restore, reset, health, log, trace, rollback, and recovery runbook evidence
    When an independent reviewer evaluates Goal 005 deployment evidence
    Then the reviewer can accept or reject completion from repo-local evidence without a human-review blocker
    And the operational observations link runbooks, rehearsal evidence, gaps, and required follow-up tickets
