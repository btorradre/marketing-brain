> ## Documentation Index
> Fetch the complete documentation index at: https://docs.aftersell.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Introduction to Upcart's public API

> Learn how to get started with Upcart's API, add scripts, test changes, and customize your cart with ease.

The **Upcart Public API** lets you customize your cart, automate workflows, and integrate with third-party apps - whether you're a developer or just getting started.\
This guide will walk you through the basics and help you start building custom functionality inside your cart drawer.

👉 [View Full Upcart Public API Documentation](https://rokt.notion.site/upcart-public-api)

***

## Overview

The Public API is a collection of JavaScript functions and event listeners that let you:

* **React to cart changes** — detect when items are added, removed, or updated.
* **Trigger actions** — such as opening or closing the cart programmatically.
* **Build custom features** — inject your own logic or UI components directly inside the cart drawer.

It’s especially helpful when working in the **Custom HTML** section of the Upcart editor, where you can use these functions to create unique experiences for shoppers.

***

## What You Need to Get Started

Before using Upcart’s API, make sure you have:

* **Access to Upcart in your Shopify store**\
  Ensure Upcart is installed and active in your store.
* **A basic understanding of JavaScript**\
  Many customizations use pre-written snippets, but knowing basic JavaScript helps if you want to go beyond the basics.

***

## Adding Your First Upcart API Script

You can start using the API right from your Upcart editor:

1. Go to **Upcart Editor → Settings → Custom HTML → Scripts (before load)**

2. Paste in your script — for example:

```
<script>
  window.upcartSubscribeAddedToCart(function(event) {
    console.log("You just added " + event.item.title + " to your cart!");
  });
</script>
```

**Note:** Older examples using `window.upcartOnAddToCart` still work but are deprecated and log a console warning. Use `upcartSubscribeAddedToCart` for all new scripts.

3. Save your changes, then test it in your store:

* Open Dev Tools (`F12` or `Ctrl + Shift + J` on Windows, `Cmd + Option + J` on Mac)
* Add a product to your cart
* Check the Console tab for the message:\
  `"You just added [product title] to your cart!"`

🎉 If you see the message, your first API script is working!

***

## Start Customizing Your Cart

Now that you’re set up, you can use the API to do all sorts of cool things — like automatically opening the cart when items are added, updating custom widgets, or sending analytics events.

For full function references and examples, check out the **[Upcart Public API Documentation](https://rokt.notion.site/upcart-public-api)**.

***

## More Resources

* 🧩 **[API FAQ](/upcart/upcart_api_frequently_asked_questions)** — Troubleshooting tips and common questions
* ⚙️ **[Common Uses for Upcart API](/upcart/common_upcart_api_uses)** — Popular code examples and templates
* 💡 **[Customization Docs](/upcart/add_a_mandatory_terms_and_conditions_checkbox_to_your_cart)** — Pre-written scripts to help you get started fast
* 🛍️ **[Shopify’s Cart API Documentation](https://shopify.dev/docs/api/ajax/reference/cart)** — Learn how Shopify handles cart data behind the scenes
* 👩💻 Need advanced customizations? Consider hiring a [Shopify Expert](https://www.shopify.com/ca/partners/directory/services/development-and-troubleshooting/custom-apps-integrations) for more complex integrations.
