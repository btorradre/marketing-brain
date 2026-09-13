> ## Documentation Index
> Fetch the complete documentation index at: https://docs.aftersell.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Common Upcart API uses

> Learn how to put Upcart's Public API to work with practical, copy-paste examples.

## How the API Pattern Works

Most Upcart API scripts follow the same simple pattern:

Listen for a cart event → Check a condition → Take an action

For example: "When the cart loads → check if it's empty → hide the sticky button."

💡 **New to APIs?** Start with [What is an API?](/upcart/what_is_an_api) before diving into the examples below.

***

## Where to Add Your Scripts

All scripts below go in:

**Cart Editor → Settings → Custom HTML → Scripts (before load)**

Wrap each snippet in `<script>...</script>` tags and save. To test, open your browser's Dev Tools console (`F12`) and look for any `console.log` messages.

***

## A note on legacy vs. modern callbacks

Upcart has two ways to listen for cart events:

| Style                | Example                          | Status                            |
| -------------------- | -------------------------------- | --------------------------------- |
| Modern (recommended) | `upcartSubscribeAddedToCart(fn)` | Current                           |
| Legacy (deprecated)  | `upcartOnAddToCart = fn`         | Still works, logs console warning |

All examples below use the modern API. Existing scripts using the old style will continue working.

***

## Example 1: Hide the Sticky Cart Button When the Cart is Empty

```html theme={"theme":{"light":"snazzy-light","dark":"github-dark"}}
<script>
  window.upcartSubscribeCartLoaded(function(event) {
    var stickyBtn = document.querySelector("#upCartStickyButton");
    if (stickyBtn) {
      var totalQty = event.cart.items.reduce(function(sum, item) {
        return sum + item.quantity;
      }, 0);
      stickyBtn.style.display = totalQty === 0 ? "none" : "block";
    }
  });
</script>
```

**How it works:** `upcartSubscribeCartLoaded` fires every time the cart is loaded. The callback receives an `event` with a `cart` object containing an `items` array. We sum the `quantity` of each item to determine if the cart is empty.

⚠️ **IMPORTANT:** `event.cart` does NOT have an `item_count` property. You must calculate the total by iterating `event.cart.items`.

***

## Example 2: Log When an Item is Added to the Cart

```html theme={"theme":{"light":"snazzy-light","dark":"github-dark"}}
<script>
  window.upcartSubscribeAddedToCart(function(event) {
    console.log("Added to cart:", event.item.title, "| Qty:", event.item.quantityAdded);
  });
</script>
```

**Properties available on `event.item`:**

| Property                   | Description                             |
| -------------------------- | --------------------------------------- |
| `event.item.title`         | Product title                           |
| `event.item.quantityAdded` | Number of units added in this action    |
| `event.item.quantity`      | Total quantity of this item now in cart |
| `event.item.variantId`     | Shopify variant ID                      |
| `event.item.handle`        | Product handle                          |
| `event.item.productId`     | Shopify product ID                      |
| `event.item.finalPrice`    | Final price after discounts             |
| `event.item.image`         | Product image URL                       |

***

## Example 3: Integrate with a Third-Party Analytics App (e.g. TripleWhale)

```html theme={"theme":{"light":"snazzy-light","dark":"github-dark"}}
<script>
  window.upcartSubscribeAddedToCart(function(event) {
    window.TriplePixel('AddToCart', {
      item: event.item.variantId,
      q: event.item.quantityAdded
    });
  });
</script>
```

> **Note:** Each third-party app is different. Check with your app's support team for the correct event format.

***

## Example 4: Open the Cart Automatically After a Product is Added

```html theme={"theme":{"light":"snazzy-light","dark":"github-dark"}}
<script>
  window.upcartSubscribeAddedToCart(function(event) {
    window.upcartOpenCart();
  });
</script>
```

> **Note:** If "Open cart drawer on add to cart" is already enabled in **Cart Editor → Settings → Cart settings**, you don't need this script.

***

## Quick Reference: Subscribe Functions (Modern API)

| Function                                               | When it fires                   | Callback receives                                                                                      |
| ------------------------------------------------------ | ------------------------------- | ------------------------------------------------------------------------------------------------------ |
| `upcartSubscribeCartLoaded(fn)`                        | Cart data loads                 | `{ cart }` - cart has `.items[]`, `.total`, `.currency`                                                |
| `upcartSubscribeAddedToCart(fn)`                       | Item added to cart              | `{ item }` - item has `.title`, `.variantId`, `.quantityAdded`, `.quantity`                            |
| `upcartSubscribeCartOpened(fn)`                        | Cart drawer opens               | `{}` (empty object)                                                                                    |
| `upcartSubscribeCartClosed(fn)`                        | Cart drawer closes              | `{}` (empty object)                                                                                    |
| `upcartSubscribeCartUpdated(fn)`                       | Cart contents change            | `{ cart }`                                                                                             |
| `upcartSubscribeItemRemoved(fn)`                       | Item removed                    | `{ item }`                                                                                             |
| `upcartSubscribeCheckoutClicked(fn)`                   | Checkout button clicked         | `{ event }` - browser MouseEvent                                                                       |
| `upcartSubscribeUpsellsAddedToCart(fn)`                | Upsell item added               | `{ variant }` - has `.id` and `.title`                                                                 |
| `upcartSubscribeUpsellsRendered(fn)`                   | Upsells render in cart          | `{ item, element }` - item is the product, element is the DOM node                                     |
| `upcartSubscribeNotesTextChanged(fn)`                  | Cart notes updated              | `{ newNotesText, oldNotesText }` - the new notes string and the previous one                           |
| `upcartSubscribeRewardsMilestonesCompletedChanged(fn)` | Reward milestone status changes | `{ numOfMilestonesCompleted, status }` - `status` is `"promotion"`, `"demotion"`, or `"initial-state"` |

***

## Direct Action Functions

| Function                           | What it does                                                   |
| ---------------------------------- | -------------------------------------------------------------- |
| `window.upcartOpenCart()`          | Opens the cart drawer                                          |
| `window.upcartCloseCart()`         | Closes the cart drawer                                         |
| `window.upcartRefreshCart()`       | Refreshes cart data                                            |
| `window.upcartGetCart()`           | Returns the current cart object                                |
| `window.upcartRegisterAddToCart()` | Registers add-to-cart for page builders (Replo, PageFly, etc.) |
| `window.upcartFormatMoney()`       | Formats a price using your store's money format                |

For the full API documentation, see the [Upcart Public API Documentation](https://rokt.notion.site/upcart-public-api).

***

## Troubleshooting

* **Script not running?** Double-check placement: it should be in *Scripts (before load)*, not after load.
* **Element not found?** Make sure the selector (e.g. `#upCartStickyButton`) matches the actual element ID in your cart.
* **Something broke?** Comment out your script by adding `//` to the start of each line, save, and refresh.
* **Still stuck?** See the [API FAQ](/upcart/upcart_api_frequently_asked_questions) for more troubleshooting steps.
