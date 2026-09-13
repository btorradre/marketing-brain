# Atelier batch treatment

September 6 follow-up: refined the shared PDP component in unpublished theme 151389143105. It renders beneath the subtitle, above price, with a quiet status dot and either “Atelier: orders open for batch …” or “Atelier: final orders for batch …”. An optional short paragraph supports a real order deadline or next-batch timing. Empty or whitespace-only batch identifiers produce no message.

Changed files: sections/main-product.liquid, snippets/commerce-styles.liquid, locales/en.default.json. All three passed Shopify Liquid/theme validation and exact remote readback. The component applies to all PDP templates using main-product.

The component remains disabled: the current Velantra batch number and whether it is actually at final orders have not been supplied. R40/ARFORTI’s 08 identifier was not copied into Velantra as a factual claim. An asynchronous question for actual batch number/status/date was sent. Once supplied, configure show_batch, batch_number, batch_status and optional batch_note on the relevant product templates using current remote versions.

The two batch-design-only screenshots are browser-local design fixtures marked with batch XX and a preview note. They are not screenshots of enabled customer-facing batch claims. Desktop 1440px and mobile 390px checks verify no overflow and correct typography; the actual draft has no visible batch claim yet.

Theme publication remains a manual Shopify-admin action under the connector’s previously reported safety restriction. No publication attempt or bypass was made in this follow-up. Film cleanup is still pending the internal editor entry point described in README.md.
