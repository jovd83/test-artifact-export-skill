### CHK-001

**Title:** Complete checkout with a valid card

**Description:** Validates the standard checkout path for a logged-in shopper.

**Traceability**
- STORY-123
- REQ-CHECKOUT-01

**Preconditions**
1. The shopper is signed in.
2. The cart contains one in-stock item.

**Steps**

| Step | Action | Expected Result |
|---|---|---|
| 1 | Open the checkout page. | The checkout summary and payment form are visible. |
| 2 | Enter valid shipping and card details and submit the order. | The order is accepted and a confirmation page is displayed. |

**Metadata**

- Execution Type: Manual
- Design Status: Approved
- Test Suite: Checkout
- Test Level: E2E
- Test Engineer: QA Team
- Notes: Use a non-expired Visa test card.
