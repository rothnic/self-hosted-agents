@fixture @actor:pm-steward @operational
Feature: Sample workflow contract
  Scenario: Fixture contract exposes actor and operational expectations
    Given a fixture driver starts the workflow
    When the PM steward inspects the fixture
    Then the human reviewer sees the blocked decision
    And the operational report records the blocked reason
