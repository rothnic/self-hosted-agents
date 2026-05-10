@comparison @actor:project-owner-engineer @operational
Feature: Comparable agent workflow
  Candidate apps need to prove the same agent workflow before platform choices are compared.

  Scenario: Project owner receives a decision-ready implementation slice
    Given a project owner acting as an engineer provides a product objective, constraints, and project context through the driver
    And the candidate app driver is registered for the shared comparison contract
    When the candidate app proposes the next implementation slice
    Then the project owner receives a concise recommendation with alternatives, explicit questions, and an acceptance check
    And the operational observations include durable run evidence that can be compared across candidate apps
