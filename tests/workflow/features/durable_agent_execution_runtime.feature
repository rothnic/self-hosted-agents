@durable-runtime @agent-workflow @operational
@actor:worker @actor:reviewer @actor:operator
Feature: Durable agent execution runtime
  Long-running agent work needs durable execution evidence before a candidate stack can be promoted.

  Scenario: Durable worker recovers from failure without duplicate side effects
    Given a worker driver starts a Pydantic AI candidate run through the durable runtime
    And the durable run reaches a recorded side-effect boundary
    When the driver injects a transient failure or process restart
    Then the durable run retries or resumes with the same durable run identity
    And the operational observations link retry count, trace id, eval id, and one side-effect record

  Scenario: Durable workflow waits for independent reviewer acceptance
    Given a worker driver reaches a review wait during durable execution
    When no independent reviewer acceptance artifact exists
    Then the durable run records a waiting state and performs no post-wait side effects
    And the operational observations link the wait state, Beads ticket, and required evidence path

  Scenario: Durable workflow resumes after reviewer acceptance
    Given an independent reviewer acceptance artifact is recorded for the waiting durable run
    When the worker driver resumes the durable runtime
    Then the run continues with the same durable run identity
    And the operational observations link the reviewer, acceptance artifact, trace id, eval id, and Beads evidence
