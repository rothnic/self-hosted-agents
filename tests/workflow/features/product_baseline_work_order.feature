@product-baseline @work-order @operational
@actor:project-owner @actor:implementer @actor:reviewer @actor:operator
Feature: Product baseline work order
  The selected product baseline turns repo-local intent into one review-gated implementation work order.

  Scenario: Project owner receives an executable work order
    Given a project owner provides an approved roadmap goal, spec, or ready ticket through the product baseline driver
    And the product baseline driver can inspect repo-local objective, spec, Beads, and evidence state
    When the implementer requests the next product work order
    Then the implementer receives one behavior scope with explicit out-of-scope boundaries
    And the work order names the acceptance command `uv run awf workflow-fixture-test`
    And the operational observations include trace, evaluation, durable state, review gate, and evidence paths

  Scenario: Reviewer acceptance controls completion
    Given an implementer has produced work-order evidence through the product baseline driver
    When no independent reviewer acceptance artifact exists
    Then the work order remains waiting for review and is not considered complete
    And the operational observations identify the required reviewer, evidence paths, and next resumable state

  Scenario: Fixture validation does not require hosted services
    Given the operator runs the product baseline driver without hosted observability credentials
    When deterministic fixture validation evaluates the work order
    Then the operator receives passing or failing repo-local evidence without a cloud service dependency
    And the operational observations preserve any self-hosted observability gaps as explicit follow-up evidence
