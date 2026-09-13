# Existing navigation destinations — September 5, 2026

Read-only Shopify Admin and Chromium checks against unpublished theme **151337074753**. No collection, page, menu, theme or app settings changed; no contact or tracking forms submitted.

| Label | Existing destination | Resource / integration | Draft result |
| --- | --- | --- | --- |
| Accessories | `/collections/accessories` | Collection `gid://shopify/Collection/294984319041`; existing manual collection, five products | HTTP 200; horse charm, scarf, tote keychain, organizer and cherry charm render |
| Track your order | `/apps/parcel` | Existing Parcelwill/ParcelPanel app proxy; current main/footer menus already link directly here | HTTP 200; Order Number + Email/Phone and separate Tracking Number inputs render inside the draft theme |
| Contact | `/pages/contact` | Published Page `gid://shopify/Page/96252100673`; template suffix `contact` | HTTP 200; native required Name, Email and Message fields; POST `/contact#contact_form` |

`/pages/track-your-order` is also an existing published Page (`gid://shopify/Page/96362397761`, default page template). It renders an informational landing page whose “order tracking page” link points to `/apps/parcel`. The direct app proxy preserves the existing navigation destination and avoids this extra click. Neither destination requires a new template or app integration to render in this draft.

The app's existing support panel displays `+1 (704) 555-0197`, which appears to be placeholder content. This was observed, not changed. No actual order lookup was performed.

Five existing menus were read, with no further page available. None exactly matches **All bags, Accessories, Track your order, Contact** in that order. `main-menu` (`gid://shopify/Menu/204150997057`) has **Handbags, Accessories, Track Your Order, Contact, FAQs, About Us**. Its Handbags resource is collection `gid://shopify/Collection/294984253505`, `/collections/handbags`; root owns the final All bags destination decision.

Evidence:

- `navigation-destinations-source.json`: dated page IDs, publication/template fields and Accessories collection identity.
- `navigation-menus-source.json`: complete current menu destinations.
- `navigation-destination-qa.json`: HTTP status, rendered inputs/links, draft theme ID and screenshots. All four checked destinations had no horizontal overflow at 1440 px.
- `navigation-destination-accessories.png`, `navigation-destination-contact.png`, `navigation-destination-track-your-order.png`, `navigation-destination-parcel.png`.
