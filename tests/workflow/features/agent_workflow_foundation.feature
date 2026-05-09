@agent-workflow @actor:pm-steward @operational
Feature: Agent workflow foundation
  Agents need a portable process for turning objectives into reviewed, tested work.

  Scenario: PM steward plans from maintained project context
    Given an agent starts from a fresh checkout through the workflow driver
    And the repository has objectives, specs, tickets, behavior contracts, and run history
    When the PM steward performs a planning cycle
    Then the human reviewer sees the next safe action
    And the operational record contains the trigger, mode, context inputs, blockers, and checks

  Scenario: Implementation drivers prove the same e2e behavior
    Given a future implementation driver is registered for the behavior contract
    When the driver executes the actor-centered scenario
    Then the user-facing result matches the contract
    And the operational observations include persistence, telemetry, or artifact evidence required by the contract
