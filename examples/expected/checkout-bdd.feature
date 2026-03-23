@checkout
@story-123
Feature: Checkout
  As a registered shopper
  I want complete checkout with valid payment details
  So that buy items without manual support

@story-123
@checkout
  Scenario: Complete checkout with a valid card
    Given the shopper is signed in
    And the cart contains one in-stock item
    When the shopper enters valid shipping and card details
    And submits the order
    Then the order is accepted
    And a confirmation page is displayed
