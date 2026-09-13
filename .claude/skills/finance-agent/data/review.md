# Review queue — 424 transactions in 234 vendor groups

Generated 2026-09-02T00:05:56 · threshold 0.8

Rule with: `python3 review.py --set-merchant "<regex>" <category> --learn --name "<rule>"`

## Policy questions — answer ONCE, settles every row tagged with it

| policy | txns | $ | currently booked as | settle with |
|---|---:|---:|---|---|
| personal_looking | 206 | $10,801 | other_opex | `python3 review.py --policy personal_looking <category>` |
| unknown_transfer | 3 | $8,350 | other_opex | `python3 review.py --policy unknown_transfer <category>` |
| people_payments | 10 | $2,982 | contractors_agency | `python3 review.py --policy people_payments <category>` |
| whop_memberships | 10 | $1,596 | marketing_software | `python3 review.py --policy whop_memberships <category>` |

personal_looking → `owner_draw` (excluded from profit) or `other_opex` (keep as company cost). people_payments → `contractors_agency` or `owner_draw`. unknown_transfer → rule each wire by id.

## Coinbase  ·  1 txn · $5,500.00  ·  proposed **other_opex** (0.90)
_Brooks to rule: contractor payment vs personal — see memory_
- `13edded6616eb322` 2026-06-29 $5,500.00 CHECKING ...6666 — Coinbase

## Venmo  ·  5 txn · $2,717.00  ·  proposed **contractors_agency** (0.90)
_per Brooks: Venmo/Wise to individuals = contractors unless clearly personal_
- `597d5062d9f5d44e` 2026-05-11 $534.00 BUSINESS CHECKING ...0189 — Venmo Transfer
- `9ae5c370c196fb1c` 2026-05-11 $266.00 BUSINESS CHECKING ...0189 — Venmo Transfer
- `9d343b3b0f15dfd9` 2026-05-20 $65.00 BUSINESS CHECKING ...0189 — Venmo Transfer
- `9badf6bf74095633` 2026-05-22 $150.00 BUSINESS CHECKING ...0189 — Venmo
- `7aebcb1af70f5b3d` 2026-06-17 $1,702.00 BUSINESS CHECKING ...0189 — Venmo

## WT 260518-032837 JPMORGAN CHASE BANK /BNF=Dhanra  ·  1 txn · $1,850.00  ·  proposed **other_opex** (0.90)
_Dhanraj Gala wire ruled NOT a contractor (2026-07-05); rule each new wire_
- `c4dd221c7fd462f5` 2026-05-18 $1,850.00 CHECKING ...6666 — WT 260518-032837 JPMORGAN CHASE BANK /BNF=Dhanraj Gala SRF# OW00006966891964 TRN#260518032

## GOOGLE *YouTube TV 1600 AMPHITHEATRE PKWY 650-25  ·  22 txn · $1,360.86  ·  proposed **other_opex** (0.90)
_looks personal — confirm business purpose or owner_draw_
- `b7a35b2051cb5371` 2025-05-29 $59.99 Apple Card — GOOGLE *YouTube TV 1600 AMPHITHEATRE PKWY 650-253-0000 94043 CA USA
- `f9c4a771369143e7` 2025-06-29 $82.99 Apple Card — GOOGLE *YouTube TV 1600 AMPHITHEATRE PKWY 650-253-0000 94043 CA USA
- `390e2ff571b7e0b6` 2025-07-29 $82.99 Apple Card — GOOGLE *YouTube TV 1600 AMPHITHEATRE PKWY 650-253-0000 94043 CA USA
- `d2141c1bcba7bf46` 2025-08-29 $82.99 Apple Card — GOOGLE *YouTube TV 1600 AMPHITHEATRE PKWY 650-253-0000 94043 CA USA
- `8547ce4796db1059` 2025-09-05 $27.75 Apple Card — GOOGLE *YouTube TV 1600 AMPHITHEATRE PKWY 650-253-0000 94043 CA USA
- `91bac7e9bd0a27c6` 2025-09-29 $82.99 Apple Card — GOOGLE *YouTube TV 1600 AMPHITHEATRE PKWY 650-253-0000 94043 CA USA
- … 16 more

## MULTISERVICELLC 3725 Vitruvian Way Addison  ·  1 txn · $1,000.00  ·  proposed **other_opex** (0.90)
_$1,000 Square payment 2026 — purpose unknown_
- `4dfa83fe223b2567` 2026-04-18 $1,000.00 Apple Card — SQ *MULTISERVICELLC 3725 Vitruvian Way Addison 75001 TX USA

## NON-WF ATM WITHDRAWAL AUTHORIZED ON 06/15 JAPANP  ·  3 txn · $976.28  ·  proposed **other_opex** (0.90)
_cash — purpose unknown_
- `983013bb55c1c400` 2026-06-15 $314.21 CHECKING ...6666 — NON-WF ATM WITHDRAWAL AUTHORIZED ON 06/15 JAPANPOST BANK(406010) OSAKA JPN 586166583016393
- `7f0ed62187d98202` 2026-06-22 $331.66 CHECKING ...6666 — NON-WF ATM WITHDRAWAL AUTHORIZED ON 06/20 WOORI CARD SEOUL KOR 466171538786250 ATM ID 2041
- `6ed996c75b6e13f2` 2026-06-22 $330.41 CHECKING ...6666 — NON-WF ATM WITHDRAWAL AUTHORIZED ON 06/22 SHINHAN CARD SEOUL KOR 586173571244586 ATM ID 08

## Equinox  ·  3 txn · $715.00  ·  proposed **other_opex** (0.90)
_likely personal — Brooks to confirm_
- `2751b6dcb3ccf351` 2026-05-18 $75.00 Business Platinum Card® — Equinox
- `fa0db75ff979981e` 2026-05-23 $320.00 Business Platinum Card® — Equinox
- `6bc13b99b3d29f6b` 2026-06-23 $320.00 Business Platinum Card® — Equinox

## WHOP*ECOMMERCE BUILDER312 W 2nd St Unit #A2299 C  ·  3 txn · $618.61  ·  proposed **marketing_software** (0.90)
_Whop hosts AdRevival + other memberships — check the memo_
- `a30c15bde0db3607` 2025-08-07 $210.27 Apple Card — WHOP*ECOMMERCE BUILDER312 W 2nd St Unit #A2299 CASPER 82601 WY USA
- `70f650af8b49e4c9` 2025-08-07 $196.16 Apple Card — WHOP*ECOMMERCE BUILDER312 W 2nd St Unit #A2299 CASPER 82601 WY USA
- `3f781d49863ecf2b` 2025-09-06 $212.18 Apple Card — WHOP*ECOMMERCE BUILDER312 W 2nd St Unit #A2299 CASPER 82601 WY USA

## PlayStation Network 2207 Bridgepointe Pkwy San M  ·  17 txn · $500.15  ·  proposed **other_opex** (0.90)
_looks personal — confirm business purpose or owner_draw_
- `308ee93f17c4e549` 2024-12-20 $29.74 Apple Card — PlayStation Network 2207 Bridgepointe Pkwy San Mateo 94404 CA USA
- `8e3b196cb7831d2b` 2025-01-02 $19.11 Apple Card — PlayStation Network 2207 Bridgepointe Pkwy San Mateo 94404 CA USA
- `91f49decf107d9ce` 2025-02-02 $19.11 Apple Card — PlayStation Network 2207 Bridgepointe Pkwy San Mateo 94404 CA USA
- `7178492ab7019bbf` 2025-03-07 $19.11 Apple Card — PlayStation Network 2207 Bridgepointe Pkwy San Mateo 94404 CA USA
- `7c1a0d2fcaa702d8` 2025-05-07 $17.99 Apple Card — PlayStation Network 2207 Bridgepointe Pkwy San Mateo 94404 CA USA
- `25f7d158cd7c6ece` 2025-06-07 $17.99 Apple Card — PlayStation Network 2207 Bridgepointe Pkwy San Mateo 94404 CA USA
- … 11 more

## Manhao Spa  ·  2 txn · $464.77  ·  proposed **other_opex** (0.90)
_likely personal — Brooks to confirm_
- `fbc60f3957c0f009` 2026-06-26 $393.44 Business Platinum Card® — Manhao Spa
- `fc5305dc261f2199` 2026-06-26 $71.33 Business Platinum Card® — Manhao Spa

## COACH 2006 100 Huntington Avenue G011A Boston  ·  1 txn · $414.43  ·  proposed **other_opex** (0.90)
_apparel — likely personal / owner_draw unless wardrobe for shoots_
- `8a3abb0d0a952da1` 2025-02-10 $414.43 Apple Card — COACH 2006 100 Huntington Avenue G011A Boston 02116 MA USA

## Brooks Brothetsim Sha Tsui Hk  ·  1 txn · $361.65  ·  proposed **other_opex** (0.90)
_apparel — likely personal / owner_draw unless wardrobe for shoots_
- `051b2ca3d7213f16` 2026-06-26 $361.65 Business Platinum Card® — Brooks Brothetsim Sha Tsui Hk ; Brooks Brothers

## Zara  ·  2 txn · $325.03  ·  proposed **other_opex** (0.90)
_apparel — likely personal / owner_draw unless wardrobe for shoots_
- `4e046119934c4be1` 2026-06-16 $223.19 Business Platinum Card® — Zara
- `a008085cbce76448` 2026-06-29 $101.84 Business Platinum Card® — Zara

## Whop  ·  2 txn · $312.50  ·  proposed **marketing_software** (0.90)
_Whop hosts AdRevival + other memberships — check the memo_
- `07c1eb56faa0b5b4` 2026-06-12 $262.50 Business Platinum Card® — Whop
- `d8c6fa8f5d1d3d12` 2026-06-16 $50.00 Business Platinum Card® — Whop

## Allsaints Regent 240 Regent St. London W1B 3BR G  ·  2 txn · $286.20  ·  proposed **other_opex** (0.90)
_apparel — likely personal / owner_draw unless wardrobe for shoots_
- `8ba6f235437d5651` 2025-06-17 $206.02 Apple Card — Allsaints Regent 240 Regent St. London W1B 3BR GBRGBR
- `bfbceff7b2cbf81c` 2025-07-12 $80.18 Apple Card — Allsaints Regent 240 Regent St. London W1B 3BR GBRGBR

## RayBan Opticians Coven15 JAMES ST London WC2E8BU  ·  1 txn · $274.68  ·  proposed **other_opex** (0.90)
_apparel — likely personal / owner_draw unless wardrobe for shoots_
- `19a67f86e85efc51` 2025-07-26 $274.68 Apple Card — RayBan Opticians Coven15 JAMES ST London WC2E8BU GB GBR

## H SAMUEL 250 OXFORD STREET OXFORD CIRCUSW1C1DJ G  ·  1 txn · $273.92  ·  proposed **other_opex** (0.90)
_apparel — likely personal / owner_draw unless wardrobe for shoots_
- `b4acc74832936145` 2025-06-12 $273.92 Apple Card — H SAMUEL 250 OXFORD STREET OXFORD CIRCUSW1C1DJ GBR

## HELP.HBOMAX.COM Warner Media 30 Hudson Yards NEW  ·  12 txn · $265.88  ·  proposed **other_opex** (0.90)
_looks personal — confirm business purpose or owner_draw_
- `481580e6282e9954` 2025-07-18 $20.99 Apple Card — HELP.HBOMAX.COM Warner Media 30 Hudson Yards NEW YORK 10001 NY USA
- `063c79f0c05ee3ea` 2025-08-18 $20.99 Apple Card — HELP.HBOMAX.COM Warner Media 30 Hudson Yards NEW YORK 10001 NY USA
- `26df0a4e71f6aefd` 2025-09-18 $20.99 Apple Card — HELP.HBOMAX.COM Warner Media 30 Hudson Yards NEW YORK 10001 NY USA
- `fb89685f3dfe96e3` 2025-10-18 $20.99 Apple Card — HELP.HBOMAX.COM Warner Media 30 Hudson Yards NEW YORK 10001 NY USA
- `67eba755484f944c` 2025-11-17 $20.99 Apple Card — HELP.HBOMAX.COM Warner Media 30 Hudson Yards NEW YORK 10001 NY USA
- `ffab680a9a8b58bc` 2025-12-18 $22.99 Apple Card — HELP.HBOMAX.COM Warner Media 30 Hudson Yards NEW YORK 10001 NY USA
- … 6 more

## PMUSA 953016 SOUTHERN 1100 SPRING ST NW ATLANTA  ·  48 txn · $264.40  ·  proposed **other_opex** (0.90)
_Philip Morris USA — tobacco/vending, personal_
- `3395bfa3cb6ce600` 2025-09-25 $6.45 Apple Card — PMUSA 953016 SOUTHERN 1100 SPRING ST NW ATLANTA 30309 GA USA
- `60ea3f10c9c0f852` 2025-11-03 $6.45 Apple Card — PMUSA 953016 SOUTHERN 1100 SPRING ST NW ATLANTA 30309 GA USA
- `c323b1e9a106841e` 2025-11-04 $6.45 Apple Card — PMUSA 953016 SOUTHERN 1100 SPRING ST NW ATLANTA 30309 GA USA
- `d551e9c20fe4608f` 2025-11-05 $6.45 Apple Card — PMUSA 953016 SOUTHERN 1100 SPRING ST NW ATLANTA 30309 GA USA
- `d551e9c20fe4608f` 2025-11-05 $6.45 Apple Card — PMUSA 953016 SOUTHERN 1100 SPRING ST NW ATLANTA 30309 GA USA
- `a24ddf736d0f2371` 2025-12-11 $6.45 Apple Card — PMUSA 953016 SOUTHERN 1100 SPRING ST NW ATLANTA 30309 GA USA
- … 42 more

## LULULEMON NORTH PARK 8687 N Central Expy Space C  ·  1 txn · $264.13  ·  proposed **other_opex** (0.90)
_apparel — likely personal / owner_draw unless wardrobe for shoots_
- `606a7ba6d040ac60` 2026-04-25 $264.13 Apple Card — LULULEMON NORTH PARK 8687 N Central Expy Space C DALLAS 75225 TX USA

## RAY-BAN E512 20 HUDSON YARDS #215B NEW YORK CITY  ·  1 txn · $259.12  ·  proposed **other_opex** (0.90)
_apparel — likely personal / owner_draw unless wardrobe for shoots_
- `f917e4303d835dad` 2025-03-29 $259.12 Apple Card — RAY-BAN E512 20 HUDSON YARDS #215B NEW YORK CITY10001 NY USA

## ZARA USA 3753 212-214 NEWBURY STREET BOSTON  ·  1 txn · $243.51  ·  proposed **other_opex** (0.90)
_apparel — likely personal / owner_draw unless wardrobe for shoots_
- `e2a65f87f39179aa` 2025-02-17 $243.51 Apple Card — ZARA USA 3753 212-214 NEWBURY STREET BOSTON 02116 MA USA

## NETFLIX.COM 121 Albright Way LOS GATOS  ·  9 txn · $228.91  ·  proposed **other_opex** (0.90)
_looks personal — confirm business purpose or owner_draw_
- `a49ce4ec2f0775c8` 2025-05-12 $24.99 Apple Card — NETFLIX.COM 121 Albright Way LOS GATOS 95032 CA USA
- `937868187f0116c7` 2025-06-12 $24.99 Apple Card — NETFLIX.COM 121 Albright Way LOS GATOS 95032 CA USA
- `f7a8b9d2c5c11098` 2025-08-12 $24.99 Apple Card — NETFLIX.COM 121 Albright Way LOS GATOS 95032 CA USA
- `e38f9b10a42bacdb` 2025-11-12 $24.99 Apple Card — NETFLIX.COM 121 Albright Way LOS GATOS 95032 CA USA
- `c321dc79f15436dd` 2025-12-12 $24.99 Apple Card — NETFLIX.COM 121 Albright Way LOS GATOS 95032 CA USA
- `53b40adefed2945a` 2026-02-12 $24.99 Apple Card — NETFLIX.COM 121 Albright Way LOS GATOS 95032 CA USA
- … 3 more

## Ralph Lauren Tsim Sha Tsui Hk  ·  1 txn · $228.30  ·  proposed **other_opex** (0.90)
_apparel — likely personal / owner_draw unless wardrobe for shoots_
- `7ada8eb995fc4424` 2026-06-29 $228.30 Business Platinum Card® — Ralph Lauren Tsim Sha Tsui Hk ; Ralph Lauren

## TICKPICK 225 W 34TH ST 1708 8455384567  ·  1 txn · $226.00  ·  proposed **meals_entertainment** (0.90)
_matched rule 'entertainment venues'_
- `8cd08a2e09d00f73` 2025-03-28 $226.00 Apple Card — TICKPICK 225 W 34TH ST 1708 8455384567 10122 NY USA

## SP REPRESENT CLO US 461 North Robertson Boulevar  ·  1 txn · $221.56  ·  proposed **other_opex** (0.90)
_apparel — likely personal / owner_draw unless wardrobe for shoots_
- `fdf8424d5701472d` 2025-02-02 $221.56 Apple Card — SP REPRESENT CLO US 461 North Robertson Boulevard WEST HOLLYWOO90048 CA USA

## Wise  ·  4 txn · $220.00  ·  proposed **contractors_agency** (0.90)
_per Brooks: Venmo/Wise to individuals = contractors unless clearly personal_
- `13d3614b65fbce87` 2026-05-11 $60.00 BUSINESS CHECKING ...0189 — Wise Transfer
- `6d42f82943aa0d41` 2026-05-20 $60.00 CHECKING ...6666 — Wise Transfer
- `41a361da0c34f631` 2026-05-20 $40.00 CHECKING ...6666 — Wise Transfer
- `339ee01525155aa7` 2026-06-01 $60.00 CHECKING ...6666 — Wise Transfer

## DERAMO CHIROPRACTIC 1200 QUAIL STREET ST 165 NEW  ·  2 txn · $216.30  ·  proposed **other_opex** (0.90)
_likely personal — Brooks to confirm_
- `3a9ee146fa471709` 2025-05-07 $108.15 Apple Card — DERAMO CHIROPRACTIC 1200 QUAIL STREET ST 165 NEW PORT 92660 CA USA
- `7361b09e0d8c00f6` 2026-05-20 $108.15 Apple Card — DERAMO CHIROPRACTIC 1200 QUAIL STREET ST 165 NEW PORT 92660 CA USA

## WHOP.COM/PAY/M0JEYK 300 Kent Ave STE 401 BROOKLY  ·  1 txn · $214.01  ·  proposed **marketing_software** (0.90)
_Whop hosts AdRevival + other memberships — check the memo_
- `9cabcd8af4d83a04` 2025-07-08 $214.01 Apple Card — WHOP.COM/PAY/M0JEYK 300 Kent Ave STE 401 BROOKLYN 11249 NY USA

## WHOP.COM/PAY/ZESYDI 300 Kent Ave STE 401 BROOKLY  ·  1 txn · $199.64  ·  proposed **marketing_software** (0.90)
_Whop hosts AdRevival + other memberships — check the memo_
- `b533886dad9a2357` 2025-07-08 $199.64 Apple Card — WHOP.COM/PAY/ZESYDI 300 Kent Ave STE 401 BROOKLYN 11249 NY USA

## Margiela Sf  ·  1 txn · $183.18  ·  proposed **other_opex** (0.90)
_apparel — likely personal / owner_draw unless wardrobe for shoots_
- `c1d5435561950ad8` 2026-07-02 $183.18 Business Platinum Card® — Margiela Sf ; Maison Margiela

## SCRIBD *660331675 460 BRYANT ST 9999999999  ·  15 txn · $179.85  ·  proposed **other_opex** (0.90)
_looks personal — confirm business purpose or owner_draw_
- `f533c1ae1c00b709` 2025-03-27 $11.99 Apple Card — SCRIBD *660331675 460 BRYANT ST 9999999999 94107 CA USA
- `628ef0a5d9298781` 2025-05-27 $11.99 Apple Card — SCRIBD *660331675 460 BRYANT ST 9999999999 94107 CA USA
- `082a7a3b6c8c1378` 2025-06-27 $11.99 Apple Card — SCRIBD *660331675 460 BRYANT ST 9999999999 94107 CA USA
- `ed5cfb4130bae9e2` 2025-07-27 $11.99 Apple Card — SCRIBD *660331675 460 BRYANT ST 9999999999 94107 CA USA
- `20b78157d28b7780` 2025-08-27 $11.99 Apple Card — SCRIBD *660331675 460 BRYANT ST 9999999999 94107 CA USA
- `7a0481d695fec8bf` 2025-09-27 $11.99 Apple Card — SCRIBD *660331675 460 BRYANT ST 9999999999 94107 CA USA
- … 9 more

## Frlkorea Seoul  ·  1 txn · $169.81  ·  proposed **other_opex** (0.90)
_apparel — likely personal / owner_draw unless wardrobe for shoots_
- `6072503900905514` 2026-06-21 $169.81 Business Platinum Card® — Frlkorea Seoul ; Uniqlo Korea

## Zerro Air  ·  3 txn · $139.22  ·  proposed **other_opex** (0.30)
_Plaid business_category 'miscellaneous'_
- `a42f0de557965e84` 2026-06-16 $38.08 Business Platinum Card® — Zerro Air ; Zerro
- `3e0af4d2aad67d30` 2026-06-17 $85.53 Business Platinum Card® — Zerro Air ; Zerro
- `ff43ff5bb43f7824` 2026-06-17 $15.61 Business Platinum Card® — Zerro Air ; Zerro

## Goonamloseu Busan  ·  1 txn · $137.93  ·  proposed **other_opex** (0.20)
_Plaid business_category 'uncategorized / needs review'_
- `b2060d1cb366f3f2` 2026-06-22 $137.93 Business Platinum Card® — Goonamloseu Busan

## Ocean Park Tiaberdeen Hk  ·  1 txn · $137.22  ·  proposed **meals_entertainment** (0.90)
_matched rule 'entertainment venues'_
- `d1d1200d0a914880` 2026-06-30 $137.22 Business Platinum Card® — Ocean Park Tiaberdeen Hk ; Ocean Park Hong Kong

## MACYS DALLAS 8687 N CENTRAL EXPY DALLAS  ·  1 txn · $134.14  ·  proposed **other_opex** (0.90)
_apparel — likely personal / owner_draw unless wardrobe for shoots_
- `b3c087bd8532d87e` 2026-04-25 $134.14 Apple Card — MACYS DALLAS 8687 N CENTRAL EXPY DALLAS 75225 TX USA

## RAVEN BARBERS 35 Grafton Way London W1T5DB GBR  ·  2 txn · $121.57  ·  proposed **other_opex** (0.90)
_likely personal — Brooks to confirm_
- `136afd820d291949` 2025-06-26 $58.53 Apple Card — SQ *RAVEN BARBERS 35 Grafton Way London W1T5DB GBR
- `72d3495af53db2d3` 2025-07-16 $63.04 Apple Card — SQ *RAVEN BARBERS 35 Grafton Way London W1T5DB GBR

## WHOP.COM/PAY/5TFOXR 10 Grand St.Ste. 1300 BROOKL  ·  1 txn · $106.16  ·  proposed **marketing_software** (0.90)
_Whop hosts AdRevival + other memberships — check the memo_
- `06380e610e25669f` 2025-02-19 $106.16 Apple Card — WHOP.COM/PAY/5TFOXR 10 Grand St.Ste. 1300 BROOKLYN 11249 NY USA

## Apple  ·  1 txn · $99.99  ·  proposed **other_opex** (0.30)
_Plaid business_category 'miscellaneous'_
- `7530a862e334fcd8` 2026-05-11 $99.99 CHECKING ...6666 — Apple

## ZARA OXFORD ST FAR EASOXFORD STREET 61 LONDON W1  ·  1 txn · $98.17  ·  proposed **other_opex** (0.90)
_apparel — likely personal / owner_draw unless wardrobe for shoots_
- `277187ba85415bc0` 2025-06-05 $98.17 Apple Card — ZARA OXFORD ST FAR EASOXFORD STREET 61 LONDON W1D 2EH GBRGBR

## CENTRE DE LOISIR 8 AVENUE FOCH PARIS IDFFRA  ·  3 txn · $97.58  ·  proposed **meals_entertainment** (0.90)
_matched rule 'entertainment venues'_
- `ab820a7924454c93` 2025-06-15 $46.46 Apple Card — CENTRE DE LOISIR 8 AVENUE FOCH PARIS 75016 IDFFRA
- `2dd98291e97c5f63` 2025-06-15 $25.56 Apple Card — CENTRE DE LOISIR 8 AVENUE FOCH PARIS 75016 IDFFRA
- `2dd98291e97c5f63` 2025-06-15 $25.56 Apple Card — CENTRE DE LOISIR 8 AVENUE FOCH PARIS 75016 IDFFRA

## Prime Video Channels 440 Terry Ave N SEATTLE  ·  5 txn · $91.95  ·  proposed **other_opex** (0.90)
_looks personal — confirm business purpose or owner_draw_
- `509e56f88c4863b0` 2026-02-13 $18.39 Apple Card — Prime Video Channels 440 Terry Ave N SEATTLE 98109 WA USA
- `a40a5c79c3af9896` 2026-03-13 $18.39 Apple Card — Prime Video Channels 440 Terry Ave N SEATTLE 98109 WA USA
- `21a782acfd830ba1` 2026-04-13 $18.39 Apple Card — Prime Video Channels 440 Terry Ave N SEATTLE 98109 WA USA
- `4549bcb65113c477` 2026-05-13 $18.39 Apple Card — Prime Video Channels 440 Terry Ave N SEATTLE 98109 WA USA
- `9c2a5dfe7baf34fe` 2026-06-13 $18.39 Apple Card — Prime Video Channels 440 Terry Ave N SEATTLE 98109 WA USA

## Greenville Ave  ·  1 txn · $88.29  ·  proposed **other_opex** (0.20)
_Plaid business_category 'uncategorized / needs review'_
- `08d622bb23d13865` 2026-05-09 $88.29 Business Platinum Card® — 4747 Greenville Ave

## Tiqets INC 417 South St Tiqets Office , PA  ·  1 txn · $78.00  ·  proposed **meals_entertainment** (0.90)
_matched rule 'entertainment venues'_
- `0b02eec0f9c0017f` 2025-02-15 $78.00 Apple Card — Tiqets INC 417 South St Tiqets Office #8, 19147 PA 19147 PA USA

## Fourvenues Calle Pintor soler Blasco 16, entresu  ·  1 txn · $76.18  ·  proposed **meals_entertainment** (0.90)
_matched rule 'entertainment venues'_
- `71a9366270bd4408` 2025-06-27 $76.18 Apple Card — Fourvenues Calle Pintor soler Blasco 16, entresuelo derechaCastellon de 12003 ESPESP

## NETFLIX, INC. 100 Winchester Circle CA  ·  3 txn · $74.97  ·  proposed **other_opex** (0.90)
_looks personal — confirm business purpose or owner_draw_
- `9e837afc8d0d2455` 2025-10-12 $24.99 Apple Card — NETFLIX, INC. 100 Winchester Circle CA 95032 CA USA
- `4ec6e7ca53dc1227` 2026-01-12 $24.99 Apple Card — NETFLIX, INC. 100 Winchester Circle CA 95032 CA USA
- `dd38cb57b57581ce` 2026-03-12 $24.99 Apple Card — NETFLIX, INC. 100 Winchester Circle CA 95032 CA USA

## WHOP.COM/PAY/ASZY4N 10 Grand St. Ste. 1300 BROOK  ·  1 txn · $73.74  ·  proposed **marketing_software** (0.90)
_Whop hosts AdRevival + other memberships — check the memo_
- `8a266489bf966efc` 2025-05-20 $73.74 Apple Card — WHOP.COM/PAY/ASZY4N 10 Grand St. Ste. 1300 BROOKLYN 11249 NY USA

## KLUB CENTRAL TRG GAJE BULATA 5 Split HR HRV  ·  1 txn · $73.34  ·  proposed **meals_entertainment** (0.90)
_matched rule 'entertainment venues'_
- `b380b52b7d25e9de` 2025-06-06 $73.34 Apple Card — KLUB CENTRAL TRG GAJE BULATA 5 Split 21000 HR HRV

## PLAYSTATION 2207 Bridgepointe Pkwy San Mateo  ·  4 txn · $71.96  ·  proposed **other_opex** (0.90)
_looks personal — confirm business purpose or owner_draw_
- `1d95cceb131fb33d` 2026-03-07 $17.99 Apple Card — PLAYSTATION 2207 Bridgepointe Pkwy San Mateo 94404 CA USA
- `42cf918af312e9d2` 2026-04-07 $17.99 Apple Card — PLAYSTATION 2207 Bridgepointe Pkwy San Mateo 94404 CA USA
- `99a96dc202c68a47` 2026-05-07 $17.99 Apple Card — PLAYSTATION 2207 Bridgepointe Pkwy San Mateo 94404 CA USA
- `4adc2ffd86ad787f` 2026-06-07 $17.99 Apple Card — PLAYSTATION 2207 Bridgepointe Pkwy San Mateo 94404 CA USA

## WHOP.COM/PAY/WWWGLN 10 Grand St. Ste. 1300 BROOK  ·  1 txn · $71.60  ·  proposed **marketing_software** (0.90)
_Whop hosts AdRevival + other memberships — check the memo_
- `7edc98aa2a8ecb66` 2025-03-21 $71.60 Apple Card — WHOP.COM/PAY/WWWGLN 10 Grand St. Ste. 1300 BROOKLYN 11249 NY USA

## Giraffe Japan Air  ·  3 txn · $71.17  ·  proposed **meals_entertainment** (0.90)
_matched rule 'entertainment venues'_
- `7d2aacf38e03d61a` 2026-06-17 $49.94 Business Platinum Card® — Giraffe Japan Air ; Giraffe Japan
- `2270f81fcdeb5e3f` 2026-06-17 $11.24 Business Platinum Card® — Giraffe Japan Air ; Giraffe Japan
- `0ad8a4db94259084` 2026-06-17 $9.99 Business Platinum Card® — Giraffe Japan Air ; Giraffe Japan

## Aqua Luna Shaukeiwan  ·  1 txn · $65.94  ·  proposed **meals_entertainment** (0.90)
_matched rule 'entertainment venues'_
- `38314412b3ba3ecc` 2026-06-28 $65.94 Business Platinum Card® — Aqua Luna Shaukeiwan ; Aqua Luna

## Ngong Ping  ·  1 txn · $65.81  ·  proposed **meals_entertainment** (0.90)
_matched rule 'entertainment venues'_
- `9070d1155e63757d` 2026-06-27 $65.81 Business Platinum Card® — Ngong Ping 360

## PBZ7ZARASPLIT MARMONTOVA 7 SPLIT 17 HRV  ·  1 txn · $64.17  ·  proposed **other_opex** (0.90)
_apparel — likely personal / owner_draw unless wardrobe for shoots_
- `6cd6e7413608fce3` 2025-06-07 $64.17 Apple Card — PBZ7ZARASPLIT MARMONTOVA 7 SPLIT 21000 17 HRV

## HELP.MAX.COM Warner Media 30 Hudson Yards NEW YO  ·  3 txn · $62.97  ·  proposed **other_opex** (0.90)
_looks personal — confirm business purpose or owner_draw_
- `056801d3e95f5143` 2025-03-18 $20.99 Apple Card — HELP.MAX.COM Warner Media 30 Hudson Yards NEW YORK 10001 NY USA
- `23d3593d674d5ebb` 2025-05-18 $20.99 Apple Card — HELP.MAX.COM Warner Media 30 Hudson Yards NEW YORK 10001 NY USA
- `7957bc98a351498c` 2025-06-18 $20.99 Apple Card — HELP.MAX.COM Warner Media 30 Hudson Yards NEW YORK 10001 NY USA

## Virtus Barber and Co  ·  1 txn · $54.00  ·  proposed **other_opex** (0.90)
_likely personal — Brooks to confirm_
- `32399438252f8a6f` 2026-05-05 $54.00 Business Platinum Card® — Virtus Barber and Co ; Virtus Barber & Co

## NETFLIX.COM 121 Albright Way NETFLIX.COM  ·  2 txn · $49.98  ·  proposed **other_opex** (0.90)
_looks personal — confirm business purpose or owner_draw_
- `1ba9e235374b7102` 2025-07-12 $24.99 Apple Card — NETFLIX.COM 121 Albright Way NETFLIX.COM 95032 CA USA
- `65ec3197ebeb16a5` 2025-09-12 $24.99 Apple Card — NETFLIX.COM 121 Albright Way NETFLIX.COM 95032 CA USA

## ZARA REGENT STREET 114-118 REGENT STREE LONDON W  ·  1 txn · $49.18  ·  proposed **other_opex** (0.90)
_apparel — likely personal / owner_draw unless wardrobe for shoots_
- `ce9e3dcfd9c35aa6` 2025-06-17 $49.18 Apple Card — ZARA REGENT STREET 114-118 REGENT STREE LONDON W1B 5FE GBRGBR

## SumUp *Paket M7E4CSTG43 Avenue Manet Saint-Brice  ·  1 txn · $48.86  ·  proposed **—** (0.00)
_no rule or hint matched_
- `26923fef89ce5c3e` 2025-06-13 $48.86 Apple Card — SumUp *Paket M7E4CSTG43 Avenue Manet Saint-Brice-s95350 FRAFRA

## Uvjmzuatmeast  ·  1 txn · $48.34  ·  proposed **other_opex** (0.20)
_Plaid business_category 'uncategorized / needs review'_
- `4aa5b15964dc2681` 2026-06-14 $48.34 Business Platinum Card® — Uvjmzuatmeast ; Apple Pay Purchase

## SumUp **Adam Sparkes 144 Cardinal Avenue 144 Mor  ·  1 txn · $46.70  ·  proposed **—** (0.00)
_no rule or hint matched_
- `ab1f55b68cda2ba8` 2025-06-19 $46.70 Apple Card — SumUp **Adam Sparkes 144 Cardinal Avenue 144 Morden SM44SX GBRGBR

## GOODBYE HORSES 5629 SMU BOULEVARD DALLAS  ·  3 txn · $46.68  ·  proposed **other_opex** (0.90)
_matched rule 'university'_
- `4e0631e849afacfc` 2025-11-14 $8.98 Apple Card — GOODBYE HORSES 5629 SMU BOULEVARD DALLAS 75206 TX USA
- `a71d19e1faa14d0b` 2025-11-15 $18.46 Apple Card — GOODBYE HORSES 5629 SMU BOULEVARD DALLAS 75206 TX USA
- `5ece9d2419a37a9a` 2026-02-28 $19.24 Apple Card — GOODBYE HORSES 5629 SMU BOULEVARD DALLAS 75206 TX USA

## THE LOT FASHION ISLAND999 Newport Center Dr 949-  ·  1 txn · $46.00  ·  proposed **other_opex** (0.90)
_apparel — likely personal / owner_draw unless wardrobe for shoots_
- `2fab4acda7f8d2d6` 2025-08-09 $46.00 Apple Card — THE LOT FASHION ISLAND999 Newport Center Dr 949-281-0069 92660 CA USA

## Zelle  ·  1 txn · $45.00  ·  proposed **contractors_agency** (0.90)
_per Brooks: Venmo/Wise to individuals = contractors unless clearly personal_
- `36411a1a7dfff0a0` 2026-07-02 $45.00 CHECKING ...6666 — Zelle to Peggy

## KIX TENANTS OSAKAFU IZUMISANOSHI SENSHUKUUKOKITA  ·  1 txn · $44.91  ·  proposed **—** (0.00)
_no rule or hint matched_
- `cb8712d2c12b5a8b` 2026-06-17 $44.91 Apple Card — KIX TENANTS OSAKAFU IZUMISANOSHI SENSHUKUUKOKITA OSAKA 5490001 JPNJPN

## LOUIES HAIRCUTS LLC 216 Bowery3rd Floor NEW YORK  ·  1 txn · $44.40  ·  proposed **other_opex** (0.90)
_likely personal — Brooks to confirm_
- `6a4eb5119e5d9ab5` 2024-11-25 $44.40 Apple Card — LOUIES HAIRCUTS LLC 216 Bowery3rd Floor NEW YORK 10012 NY USA

## TST-Brother Marcus - B1 Dirty Lane London SE19PA  ·  1 txn · $43.79  ·  proposed **—** (0.00)
_no rule or hint matched_
- `847dc3f28d385a65` 2025-07-17 $43.79 Apple Card — TST-Brother Marcus - B1 Dirty Lane London SE19PA GBRGBR

## ZOO NEW ENGLAND 1 FRANKLIN PARK ROAD BOSTON  ·  1 txn · $40.90  ·  proposed **meals_entertainment** (0.90)
_matched rule 'entertainment venues'_
- `69fc38234efb67c7` 2024-11-24 $40.90 Apple Card — ZOO NEW ENGLAND 1 FRANKLIN PARK ROAD BOSTON 02121 MA USA

## ARCADE MANIA LLC THE OUTLET MALL ROUTE 66 CARR 3  ·  1 txn · $40.00  ·  proposed **meals_entertainment** (0.90)
_matched rule 'entertainment venues'_
- `411573f4ca596194` 2025-03-15 $40.00 Apple Card — ARCADE MANIA LLC THE OUTLET MALL ROUTE 66 CARR 3 KM 18.4 CANOVANAS 00729 PR PRI

## ODEON Luxe Leicester S22 Leicester Square London  ·  2 txn · $34.41  ·  proposed **—** (0.00)
_no rule or hint matched_
- `75f8a3848efd0dad` 2025-07-25 $14.86 Apple Card — ODEON Luxe Leicester S22 Leicester Square London WC2H 7LQ LNDGBR
- `3e0e12f5a6df0c0f` 2025-07-26 $19.55 Apple Card — ODEON Luxe Leicester S22 Leicester Square London WC2H 7LQ LNDGBR

## SumUp *Frequency LTD Frequency 121 King Cross R   ·  8 txn · $34.11  ·  proposed **—** (0.00)
_no rule or hint matched_
- `12794655b7200d2c` 2025-06-10 $4.69 Apple Card — SumUp *Frequency LTD Frequency 121 King Cross R London WC1X 9NH GBR
- `fce5760f2e009bf0` 2025-06-11 $4.68 Apple Card — SumUp *Frequency LTD Frequency 121 King Cross R London WC1X 9NH GBR
- `d2f4a0e6c3cbd4df` 2025-06-11 $1.36 Apple Card — SumUp *Frequency LTD Frequency 121 King Cross R London WC1X 9NH GBR
- `c658a9720c75d7da` 2025-06-17 $4.70 Apple Card — SumUp *Frequency LTD Frequency 121 King Cross R London WC1X 9NH GBR
- `a5437fbb37db6f03` 2025-06-18 $4.70 Apple Card — SumUp *Frequency LTD Frequency 121 King Cross R London WC1X 9NH GBR
- `bad3a7f176c35b79` 2025-06-19 $4.66 Apple Card — SumUp *Frequency LTD Frequency 121 King Cross R London WC1X 9NH GBR
- … 2 more

## Anmol Jewellery LTD 141-149 Portobello Road Lond  ·  1 txn · $34.04  ·  proposed **—** (0.00)
_no rule or hint matched_
- `f19ec389003c3fdd` 2025-06-18 $34.04 Apple Card — Anmol Jewellery LTD 141-149 Portobello Road London W11 2DY GBRGBR

## Bigsmoke Taphouse and South Terminal Perimeter R  ·  1 txn · $33.88  ·  proposed **—** (0.00)
_no rule or hint matched_
- `52502bc94d25ed83` 2025-07-18 $33.88 Apple Card — Bigsmoke Taphouse and South Terminal Perimeter Road E Gatwick RH6 0NP GBRGBR

## PORTLANDS 247 - WOBURNWOBURN PLACE 36-38 LONDON   ·  1 txn · $32.04  ·  proposed **—** (0.00)
_no rule or hint matched_
- `70d99e07fed8e07e` 2025-06-01 $32.04 Apple Card — PORTLANDS 247 - WOBURNWOBURN PLACE 36-38 LONDON WC1H OJR GBRGBR

## Servy*Brewdog Devonshire House, 60 Goswell Road   ·  1 txn · $31.66  ·  proposed **—** (0.00)
_no rule or hint matched_
- `9cc92b815f8b7499` 2025-06-12 $31.66 Apple Card — Servy*Brewdog Devonshire House, 60 Goswell Road London EC1M 7AD GBRGBR

## RELAY AEROPORT NICE COTE D AZUR NICE CEDEX 3 FRA  ·  1 txn · $31.11  ·  proposed **—** (0.00)
_no rule or hint matched_
- `1130359616a8db39` 2025-07-07 $31.11 Apple Card — RELAY AEROPORT NICE COTE D AZUR NICE CEDEX 3 06281 FRAFRA

## BESTMART 7-14 COVENTRY STREET LONDON W1D 7DH GBR  ·  1 txn · $31.01  ·  proposed **—** (0.00)
_no rule or hint matched_
- `0a8e4b3e34764f97` 2025-07-16 $31.01 Apple Card — BESTMART 7-14 COVENTRY STREET LONDON W1D 7DH GBRGBR

## Cloud Jv8qvpg.co  ·  1 txn · $30.47  ·  proposed **software_saas** (0.50)
_Plaid business_category 'software / saas'_
- `d4034ba9d6671358` 2026-06-01 $30.47 Business Gold Card — Cloud Jv8qvpg.co ; Cloud Service

## H&M 0100BOSTON 100 Newbury Street BOSTON  ·  1 txn · $30.03  ·  proposed **—** (0.00)
_no rule or hint matched_
- `91f21988d179545d` 2025-02-17 $30.03 Apple Card — H&M 0100BOSTON 100 Newbury Street BOSTON 02116 MA USA

## F&D WIMBLEDON GATE 1 WIMBLEDON SW19 5AE GBR  ·  1 txn · $29.90  ·  proposed **—** (0.00)
_no rule or hint matched_
- `801dcc5b7dc9e52a` 2025-07-13 $29.90 Apple Card — F&D WIMBLEDON GATE 1 WIMBLEDON SW19 5AE GBR

## WH Smith InMotion LutoTerminal Building London L  ·  1 txn · $28.59  ·  proposed **—** (0.00)
_no rule or hint matched_
- `b8ea8d89c2a5ee2f` 2025-06-06 $28.59 Apple Card — WH Smith InMotion LutoTerminal Building London Luton Luton LU2 9LY GBR

## SUPER SNAX 37 TOTTENHAM COURT R LONDON W1T 1BY G  ·  1 txn · $28.53  ·  proposed **—** (0.00)
_no rule or hint matched_
- `4d7750386fb1440a` 2025-07-24 $28.53 Apple Card — SUPER SNAX 37 TOTTENHAM COURT R LONDON W1T 1BY GBRGBR

## ALLIANZ TRAVEL INS 9950 MAYLAND DR 8004960329  ·  1 txn · $28.49  ·  proposed **—** (0.00)
_no rule or hint matched_
- `b4ecdcf855d03c4b` 2025-03-14 $28.49 Apple Card — ALLIANZ TRAVEL INS 9950 MAYLAND DR 8004960329 23233 VA USA

## THE LONDON STORE I111 Kings Way Holborn London W  ·  1 txn · $28.49  ·  proposed **—** (0.00)
_no rule or hint matched_
- `bc86b8e614a1ee04` 2025-07-23 $28.49 Apple Card — SQ *THE LONDON STORE I111 Kings Way Holborn London WC2B6PP GBR

## SumUp *Amp Shots IrelThe Black Church St. Marys   ·  1 txn · $28.02  ·  proposed **—** (0.00)
_no rule or hint matched_
- `cd8ffb725e6f8c98` 2025-07-19 $28.02 Apple Card — SumUp *Amp Shots IrelThe Black Church St. Marys Place Dublin D07P4AX IRLIRL

## K1 SPEED - CARIBBEAN KKM 18.4 HM 17.5 CANOVANAS   ·  1 txn · $27.89  ·  proposed **—** (0.00)
_no rule or hint matched_
- `7b2eda8bf4310de9` 2025-03-15 $27.89 Apple Card — K1 SPEED - CARIBBEAN KKM 18.4 HM 17.5 CANOVANAS 00729 PR PRI

## WOW BAO - LOGAN AIBoston Logan Internationa East  ·  1 txn · $27.87  ·  proposed **—** (0.00)
_no rule or hint matched_
- `0fb5d8c56186bd77` 2025-03-07 $27.87 Apple Card — TST*WOW BAO - LOGAN AIBoston Logan Internationa East Boston 02128 MA USA

## Ministry of Sound | B 103 Gaunt Street London SE  ·  1 txn · $27.30  ·  proposed **—** (0.00)
_no rule or hint matched_
- `aba8331f9145052f` 2025-06-24 $27.30 Apple Card — Ministry of Sound | B 103 Gaunt Street London SE1 6DP GBRGBR

## Paddington Store 195 Praed Street London W2 1RH   ·  1 txn · $27.16  ·  proposed **—** (0.00)
_no rule or hint matched_
- `b8e01ec42e5abf95` 2025-06-10 $27.16 Apple Card — Paddington Store 195 Praed Street London W2 1RH GBRGBR

## MC DONALDS 145 AV DE VILLIERS PARIS IDFFRA  ·  1 txn · $26.95  ·  proposed **—** (0.00)
_no rule or hint matched_
- `de5ba82a795efdeb` 2025-06-14 $26.95 Apple Card — MC DONALDS 145 AV DE VILLIERS PARIS 75017 IDFFRA

## FARMACIA CHINCHILLA URB.EL ROSARIO 2 MARBELLA ES  ·  1 txn · $26.91  ·  proposed **—** (0.00)
_no rule or hint matched_
- `25b3fa34daeddf27` 2025-06-27 $26.91 Apple Card — FARMACIA CHINCHILLA URB.EL ROSARIO 2 MARBELLA 29604 ESPESP

## PRINCESS LOUISE 208-209 HIGH HOLBURN LONDON WC1V  ·  2 txn · $26.89  ·  proposed **—** (0.00)
_no rule or hint matched_
- `7e4a883e2999b0aa` 2025-06-01 $17.16 Apple Card — PRINCESS LOUISE 208-209 HIGH HOLBURN LONDON WC1V 7EP GBR
- `c2f88f0b2a02e846` 2025-06-01 $9.73 Apple Card — PRINCESS LOUISE 208-209 HIGH HOLBURN LONDON WC1V 7EP GBR

## Daily Cash Adjustment  ·  4 txn · $26.82  ·  proposed **—** (0.00)
_no rule or hint matched_
- `87ca5a8999ddb8b7` 2026-05-04 $0.40 Apple Card — Daily Cash Adjustment
- `e0117cff47bac11f` 2026-05-04 $1.27 Apple Card — Daily Cash Adjustment
- `87ca5a8999ddb8b7` 2026-05-04 $0.40 Apple Card — Daily Cash Adjustment
- `279e178b3c1fcffe` 2026-05-07 $24.75 Apple Card — Daily Cash Adjustment

## MICRO CENTER 727 MEMORIAL DR CAMBRIDGE  ·  1 txn · $26.81  ·  proposed **—** (0.00)
_no rule or hint matched_
- `5933027f5c6fb8aa` 2025-01-30 $26.81 Apple Card — MICRO CENTER #121 727 MEMORIAL DR CAMBRIDGE 02139 MA USA

## Zettle_*CHICKEN STAK132 Higham Station Avenue Lo  ·  2 txn · $26.49  ·  proposed **—** (0.00)
_no rule or hint matched_
- `b76c3c2db0fede24` 2025-06-12 $14.24 Apple Card — Zettle_*CHICKEN STAK132 Higham Station Avenue London E49XG GBRGBR
- `44d23ee672defe48` 2025-06-18 $12.25 Apple Card — Zettle_*CHICKEN STAK132 Higham Station Avenue London E49XG GBRGBR

## Cell Seoul  ·  2 txn · $26.20  ·  proposed **other_opex** (0.20)
_Plaid business_category 'uncategorized / needs review'_
- `72aff9305a9ebec0` 2026-06-21 $19.65 Business Platinum Card® — Cell Seoul
- `2ca56463ecd19079` 2026-06-21 $6.55 Business Platinum Card® — Cell Seoul

## HARVARD BUS EDUCATION 20 GUEST ST STE 700 617-78  ·  2 txn · $26.10  ·  proposed **—** (0.00)
_no rule or hint matched_
- `248f1cfff2d4aa17` 2025-02-05 $4.95 Apple Card — HARVARD BUS EDUCATION 20 GUEST ST STE 700 617-783-7600 02135 MA USA
- `7ab054616faf4220` 2025-02-27 $21.15 Apple Card — HARVARD BUS EDUCATION 20 GUEST ST STE 700 617-783-7600 02135 MA USA

## ST DYMPHNAS LLC 166 Allen Street New York  ·  1 txn · $25.75  ·  proposed **—** (0.00)
_no rule or hint matched_
- `246080893bad3648` 2025-03-30 $25.75 Apple Card — SQ *ST DYMPHNAS LLC 166 Allen Street New York 10002 NY USA

## JOYS C. MUELLE RIVERA.LOCAL 58 NUEVA ANDALUC2966  ·  1 txn · $25.68  ·  proposed **—** (0.00)
_no rule or hint matched_
- `62fd90a4269cecc3` 2025-07-20 $25.68 Apple Card — JOYS C. MUELLE RIVERA.LOCAL 58 NUEVA ANDALUC29660 ESPESP

## EP JARDIN DES TUILERIES PARIS 1 FRA  ·  1 txn · $25.56  ·  proposed **—** (0.00)
_no rule or hint matched_
- `b40f50c2fc4afa0c` 2025-06-15 $25.56 Apple Card — EP JARDIN DES TUILERIES PARIS 1 75001 FRA

## BOOTS,LONDON W1P 122 TOTTENHAM COURT ROAD LONDON  ·  1 txn · $25.55  ·  proposed **—** (0.00)
_no rule or hint matched_
- `9c81566baebc2409` 2025-06-19 $25.55 Apple Card — BOOTS,LONDON W1P 122 TOTTENHAM COURT ROAD LONDON W1T 7PP GBR

## ECOM TOOLS STANDARD Unit 814, 2800 Keele St TORO  ·  1 txn · $24.99  ·  proposed **—** (0.00)
_no rule or hint matched_
- `649c22ac28493727` 2024-11-26 $24.99 Apple Card — ECOM TOOLS STANDARD Unit 814, 2800 Keele St TORONTO M3M2G5 ON CAN

## Zettle_*Al-Ayach LTD Flat 214 holcroft co London  ·  2 txn · $24.37  ·  proposed **—** (0.00)
_no rule or hint matched_
- `7ded8893439b6133` 2025-06-02 $12.16 Apple Card — Zettle_*Al-Ayach LTD Flat 214 holcroft co London W1W 5DL En GBR
- `70496af2a7b57f04` 2025-06-11 $12.21 Apple Card — Zettle_*Al-Ayach LTD Flat 214 holcroft co London W1W 5DL En GBR

## QUICK BITES INT LUIS MUNOZ MARIN TER 787-791-850  ·  1 txn · $24.09  ·  proposed **—** (0.00)
_no rule or hint matched_
- `fea5e644aead8d3b` 2025-03-17 $24.09 Apple Card — QUICK BITES INT LUIS MUNOZ MARIN TER 787-791-8500 00979 PR PRI

## AMERICAS NATL PARKS - CASTILLO SAN CRISTOBAL SAN  ·  1 txn · $23.30  ·  proposed **—** (0.00)
_no rule or hint matched_
- `4591f673b20bb17f` 2025-03-09 $23.30 Apple Card — AMERICAS NATL PARKS - CASTILLO SAN CRISTOBAL SAN JUAN 00902 PRI

## TST-Doner Bros 180 high holborn London WC1V7AA G  ·  1 txn · $22.74  ·  proposed **—** (0.00)
_no rule or hint matched_
- `6a6f8e45532ad892` 2025-06-10 $22.74 Apple Card — TST-Doner Bros 180 high holborn London WC1V7AA GBRGBR

## WESTIN COPLEY FB 10 Huntington Ave BOSTON  ·  2 txn · $21.89  ·  proposed **—** (0.00)
_no rule or hint matched_
- `6e1ad75656f1c600` 2025-05-05 $5.89 Apple Card — WESTIN COPLEY FB 10 Huntington Ave BOSTON 02116 MA USA
- `ecadbe0e92a26d4f` 2025-05-05 $16.00 Apple Card — WESTIN COPLEY FB 10 Huntington Ave BOSTON 02116 MA USA

## Zettle_*AYASH ltd 427 flat 9 Edgware road London  ·  2 txn · $21.74  ·  proposed **—** (0.00)
_no rule or hint matched_
- `315297a72de156a4` 2025-06-24 $9.46 Apple Card — Zettle_*AYASH ltd 427 flat 9 Edgware road London W21BT GBRGBR
- `310a8affb51ef634` 2025-06-26 $12.28 Apple Card — Zettle_*AYASH ltd 427 flat 9 Edgware road London W21BT GBRGBR

## LGW SOUTH WDF SATELLITGWS SATTELITE GATWICK SOUT  ·  1 txn · $21.51  ·  proposed **—** (0.00)
_no rule or hint matched_
- `b25732e433cd3170` 2025-07-18 $21.51 Apple Card — LGW SOUTH WDF SATELLITGWS SATTELITE GATWICK SOUTHRH6 0QH GBRGBR

## A FUORVITO and SONS 64 Bellamy Street London SW1  ·  1 txn · $21.47  ·  proposed **—** (0.00)
_no rule or hint matched_
- `b33e7fb5fad23120` 2025-07-13 $21.47 Apple Card — A FUORVITO and SONS 64 Bellamy Street London SW12 8BU GBRGBR

## HELP.MAX.COM Warner Media30 Hudson Yards NEW YOR  ·  1 txn · $20.99  ·  proposed **other_opex** (0.90)
_looks personal — confirm business purpose or owner_draw_
- `a3b3e1f10809a4a1` 2025-02-17 $20.99 Apple Card — HELP.MAX.COM Warner Media30 Hudson Yards NEW YORK 10001 NY USA

## The Acai Girls 705 Fulham Road London SW6 5UL GB  ·  1 txn · $20.64  ·  proposed **—** (0.00)
_no rule or hint matched_
- `69c26e60bbaff497` 2025-07-10 $20.64 Apple Card — The Acai Girls 705 Fulham Road London SW6 5UL GBRGBR

## SOBAO TO MULTIPLY BLVD STE 112 SAN JUAN PR PRI  ·  3 txn · $20.55  ·  proposed **—** (0.00)
_no rule or hint matched_
- `3bb7a3d62b9c5d20` 2025-03-14 $3.48 Apple Card — SOBAO TO MULTIPLY BLVD STE 112 SAN JUAN 00926 PR PRI
- `721a8041632db230` 2025-03-15 $5.30 Apple Card — SOBAO TO MULTIPLY BLVD STE 112 SAN JUAN 00926 PR PRI
- `e84dea3941ada1b9` 2025-03-15 $11.77 Apple Card — SOBAO TO MULTIPLY BLVD STE 112 SAN JUAN 00926 PR PRI

## Albert Schloss London London, 20-24 Shaftesbury   ·  1 txn · $20.50  ·  proposed **—** (0.00)
_no rule or hint matched_
- `7d5582f6a6da8cf4` 2025-07-16 $20.50 Apple Card — Albert Schloss London London, 20-24 Shaftesbury Avenue London W1D 7EU GBRGBR

## TAO NY UPTOWN 42 E 58th Street NEW YORK  ·  1 txn · $20.00  ·  proposed **—** (0.00)
_no rule or hint matched_
- `f9f78b065083ad58` 2025-02-22 $20.00 Apple Card — TAO NY UPTOWN 42 E 58th Street NEW YORK 10022 NV USA

## SAN JUAN NATL HISTORIC501 CALLE NORZAGARAY SAN J  ·  1 txn · $20.00  ·  proposed **—** (0.00)
_no rule or hint matched_
- `babaf3ee3f8e3c43` 2025-03-09 $20.00 Apple Card — SAN JUAN NATL HISTORIC501 CALLE NORZAGARAY SAN JUAN 00901 PRI

## SOUTHERN METHODIST UNI3140 DYER ST MS DALLAS  ·  2 txn · $20.00  ·  proposed **other_opex** (0.90)
_matched rule 'university'_
- `b6d42be505494d69` 2025-09-27 $10.00 Apple Card — SOUTHERN METHODIST UNI3140 DYER ST MS #261 DALLAS 75275 TX USA
- `18b4adfdea9a4043` 2026-04-18 $10.00 Apple Card — SOUTHERN METHODIST UNI3140 DYER ST MS #261 DALLAS 75275 TX USA

## DEV BROTHERS 21 RUE DE DOUAI PARIS 9 FRAFRA  ·  1 txn · $19.75  ·  proposed **—** (0.00)
_no rule or hint matched_
- `1ce79abcbd7d5694` 2025-06-14 $19.75 Apple Card — DEV BROTHERS 21 RUE DE DOUAI PARIS 9 75009 FRAFRA

## Empire Casino - LSQ 5-6 Leicester Square London   ·  2 txn · $19.72  ·  proposed **meals_entertainment** (0.90)
_matched rule 'entertainment venues'_
- `165ee17103052cde` 2025-07-16 $9.86 Apple Card — Empire Casino - LSQ 5-6 Leicester Square London WC2H 7NA GBRGBR
- `165ee17103052cde` 2025-07-16 $9.86 Apple Card — Empire Casino - LSQ 5-6 Leicester Square London WC2H 7NA GBRGBR

## STAKEHAUS Earlham Street London WC2H9LD GBRGBR  ·  1 txn · $18.99  ·  proposed **—** (0.00)
_no rule or hint matched_
- `337d84feedf8ca22` 2025-06-03 $18.99 Apple Card — STAKEHAUS Earlham Street London WC2H9LD GBRGBR

## TABACCHERIA ALIMENTARIVIA PISACANE CARLO 14 PONZ  ·  1 txn · $18.46  ·  proposed **—** (0.00)
_no rule or hint matched_
- `250255d7f40f8385` 2025-06-21 $18.46 Apple Card — TABACCHERIA ALIMENTARIVIA PISACANE CARLO 14 PONZA 04027 LT ITA

## Bloodsports 27-29 Endell Street London WC2H 9BA   ·  1 txn · $18.25  ·  proposed **—** (0.00)
_no rule or hint matched_
- `9833162a6a4f2a13` 2025-06-01 $18.25 Apple Card — Bloodsports 27-29 Endell Street London WC2H 9BA GBRGBR

## PUBLICISDRUGSTOR 133 AVENUE DES CHAMPS ELYSEES P  ·  1 txn · $18.03  ·  proposed **—** (0.00)
_no rule or hint matched_
- `26835de91bd2d8a2` 2025-06-13 $18.03 Apple Card — PUBLICISDRUGSTOR 133 AVENUE DES CHAMPS ELYSEES PARIS 75008 FRAFRA

## LA SALA BY THE SEA C. URB. VILLA MARINA 0 URBANI  ·  1 txn · $17.98  ·  proposed **—** (0.00)
_no rule or hint matched_
- `e051335d59444aaa` 2025-07-19 $17.98 Apple Card — LA SALA BY THE SEA C. URB. VILLA MARINA 0 URBANIZACION 29660 ESPESP

## EATALY SPA ROMA TERMPIAZZA DEI CINQUECENTO ROMA   ·  1 txn · $17.76  ·  proposed **other_opex** (0.90)
_likely personal — Brooks to confirm_
- `40458214e7068c3c` 2025-06-20 $17.76 Apple Card — EATALY SPA ROMA TERMPIAZZA DEI CINQUECENTO ROMA 00185 ITA

## SOUTH SWELL HAND DIPPE1330 S. COAST HWY. LAGUNA   ·  1 txn · $17.70  ·  proposed **—** (0.00)
_no rule or hint matched_
- `9da6527467ba04e9` 2025-07-30 $17.70 Apple Card — SOUTH SWELL HAND DIPPE1330 S. COAST HWY. LAGUNA BEACH 92651 CA USA

## BBMSL*SHARI SHARI SOHOGF 11 OLD BAILEY ST Hong K  ·  1 txn · $17.60  ·  proposed **—** (0.00)
_no rule or hint matched_
- `f321d5f396513260` 2026-06-28 $17.60 Apple Card — BBMSL*SHARI SHARI SOHOGF 11 OLD BAILEY ST Hong Kong 000 HKGHKG

## RED LION PL. ANTONIO BANDERAS S/N (0 MARBELLA ES  ·  1 txn · $17.51  ·  proposed **—** (0.00)
_no rule or hint matched_
- `ac0e07e0eb02efb2` 2025-07-19 $17.51 Apple Card — RED LION PL. ANTONIO BANDERAS S/N (0 MARBELLA 29600 ESPESP

## PYRAMIDES 9 RUE DES PYRAMIDES PARIS 1 FRA  ·  1 txn · $17.31  ·  proposed **—** (0.00)
_no rule or hint matched_
- `9dcfb3cf8f6ac78a` 2025-06-14 $17.31 Apple Card — PYRAMIDES 9 RUE DES PYRAMIDES PARIS 1 75001 FRA

## ALI ARFAT CAMPO DE FIORI SNC ROMA RM ITA  ·  1 txn · $17.30  ·  proposed **—** (0.00)
_no rule or hint matched_
- `1e864f97333eb2bf` 2025-06-22 $17.30 Apple Card — ALI ARFAT CAMPO DE FIORI SNC ROMA 00186 RM ITA

## TERMINI SRL VIA VOLTURNO ROMA ITA  ·  1 txn · $17.18  ·  proposed **—** (0.00)
_no rule or hint matched_
- `9adb8d90fbc27b93` 2025-06-20 $17.18 Apple Card — TERMINI SRL VIA VOLTURNO ROMA 00185 ITA

## TRICOLORE 43 AVENUE DE ST MANDE PARIS 12 FRA  ·  1 txn · $16.84  ·  proposed **—** (0.00)
_no rule or hint matched_
- `e4bdf04e8627d31d` 2025-06-14 $16.84 Apple Card — TRICOLORE 43 AVENUE DE ST MANDE PARIS 12 75012 FRA

## INTERMARCHE 14 AVENUE DE LA GRANDE ARMEE PARIS F  ·  1 txn · $16.66  ·  proposed **—** (0.00)
_no rule or hint matched_
- `1991365d6ea4a149` 2025-06-13 $16.66 Apple Card — INTERMARCHE 14 AVENUE DE LA GRANDE ARMEE PARIS 75017 FRAFRA

## MENDOCINO FARMS -849 NEWPORT CENTER DR NEWPORT B  ·  1 txn · $16.27  ·  proposed **—** (0.00)
_no rule or hint matched_
- `fca07f78bb3377d3` 2025-01-07 $16.27 Apple Card — TST* MENDOCINO FARMS -849 NEWPORT CENTER DR NEWPORT BEACH92660 CA USA

## DA VINCI Marmontova ulica 5 Marmontova ul21000 H  ·  1 txn · $15.93  ·  proposed **—** (0.00)
_no rule or hint matched_
- `4c3ad60825eebe6a` 2025-06-07 $15.93 Apple Card — DA VINCI Marmontova ulica 5 Marmontova ul21000 HRVHRV

## GELSONS MARKETS 1660 SAN MIGUEL DR. NEWPORT BEAC  ·  1 txn · $15.88  ·  proposed **—** (0.00)
_no rule or hint matched_
- `241309c4bacb465d` 2025-05-06 $15.88 Apple Card — GELSONS MARKETS #6 1660 SAN MIGUEL DR. NEWPORT BEACH92660 CA USA

## NATURAL JUICE C. LG PUERTO BANUS 0 NUME0 MARBELL  ·  1 txn · $15.76  ·  proposed **—** (0.00)
_no rule or hint matched_
- `998af2fd824e4633` 2025-07-20 $15.76 Apple Card — NATURAL JUICE C. LG PUERTO BANUS 0 NUME0 MARBELLA 29660 ESPESP

## DOT COD TAKSHING HOUSE CENTRAL 000000000 HKG  ·  1 txn · $15.43  ·  proposed **—** (0.00)
_no rule or hint matched_
- `48b996e40746f405` 2026-06-28 $15.43 Apple Card — DOT COD TAKSHING HOUSE CENTRAL 000000000 HKG

## CER KINGS ROAD LTD126 New Kings Road London SW64  ·  3 txn · $15.42  ·  proposed **—** (0.00)
_no rule or hint matched_
- `8a63fa02de16a88c` 2025-07-08 $4.10 Apple Card — SQ *CER KINGS ROAD LTD126 New Kings Road London SW64LZ GBR
- `50bf0fb76223b741` 2025-07-09 $7.23 Apple Card — SQ *CER KINGS ROAD LTD126 New Kings Road London SW64LZ GBR
- `63a72d96430331b7` 2025-07-10 $4.09 Apple Card — SQ *CER KINGS ROAD LTD126 New Kings Road London SW64LZ GBR

## WH Smith Gatwick SouthRoom 3402 South Tl Gatwick  ·  1 txn · $15.33  ·  proposed **—** (0.00)
_no rule or hint matched_
- `a5589ad41633f0eb` 2025-06-19 $15.33 Apple Card — WH Smith Gatwick SouthRoom 3402 South Tl Gatwick Airport London RH6 0NN GBR

## Eat Momo Bank End 1 London SE19FJ GBRGBR  ·  1 txn · $15.17  ·  proposed **—** (0.00)
_no rule or hint matched_
- `c8ec4289e70b631b` 2025-07-02 $15.17 Apple Card — Eat Momo Bank End 1 London SE19FJ GBRGBR

## CHONG SHING DISPENSAR SHOP D G F 655 NATHAN ROAD  ·  1 txn · $14.80  ·  proposed **other_opex** (0.90)
_likely personal — Brooks to confirm_
- `f2012e9cc45f9f76` 2026-06-26 $14.80 Apple Card — CHONG SHING DISPENSAR SHOP D G F 655 NATHAN ROAD KL Hong Kong 999077 HKGHKG

## Which Wich Superior S 1 Bucknall Street London W  ·  1 txn · $14.46  ·  proposed **—** (0.00)
_no rule or hint matched_
- `ca4a873faf40d6b5` 2025-06-01 $14.46 Apple Card — Which Wich Superior S 1 Bucknall Street London WC2H8AG GBRGBR

## Zettle_*HCP GELATI LTD41 OLD COMPTON STREET LOND  ·  1 txn · $14.25  ·  proposed **—** (0.00)
_no rule or hint matched_
- `0450a24b0118bde6` 2025-06-10 $14.25 Apple Card — Zettle_*HCP GELATI LTD41 OLD COMPTON STREET LONDON W1D6HF GBRGBR

## ESTANCO MAQUINAS C. PINTOR CABALLERO ESTAN0 MARB  ·  2 txn · $14.18  ·  proposed **—** (0.00)
_no rule or hint matched_
- `135f8f3cd7b0ea69` 2025-07-19 $7.18 Apple Card — ESTANCO MAQUINAS C. PINTOR CABALLERO ESTAN0 MARBELLA 29670 ESPESP
- `4d96e188437045c6` 2025-07-19 $7.00 Apple Card — ESTANCO MAQUINAS C. PINTOR CABALLERO ESTAN0 MARBELLA 29670 ESPESP

## NIKONO MILLE PL. ANTONIO BANDERA 3 MARBELLA ESPE  ·  1 txn · $14.11  ·  proposed **—** (0.00)
_no rule or hint matched_
- `664324669a2a3c9d` 2025-06-27 $14.11 Apple Card — NIKONO MILLE PL. ANTONIO BANDERA 3 MARBELLA 29601 ESPESP

## Ministry of Sound | M 103 Gaunt Street London SE  ·  1 txn · $13.65  ·  proposed **—** (0.00)
_no rule or hint matched_
- `77c2f841e6fc351b` 2025-06-24 $13.65 Apple Card — Ministry of Sound | M 103 Gaunt Street London SE1 6DP GBRGBR

## Leesipo Seoul  ·  1 txn · $13.10  ·  proposed **other_opex** (0.20)
_Plaid business_category 'uncategorized / needs review'_
- `6c94ccba45efd7e9` 2026-06-19 $13.10 Business Platinum Card® — Leesipo Seoul ; Leesipo

## Darts Dramattico Dd Osaka  ·  1 txn · $13.05  ·  proposed **meals_entertainment** (0.90)
_matched rule 'entertainment venues'_
- `934f413aa1c61e25` 2026-06-18 $13.05 Business Platinum Card® — Darts Dramattico Dd Osaka ; Darts Dramattico

## Groupon, Inc. 600 W. Chicago Ave 312-288-6424  ·  1 txn · $13.00  ·  proposed **—** (0.00)
_no rule or hint matched_
- `421ebb4552507744` 2025-02-07 $13.00 Apple Card — Groupon, Inc. 600 W. Chicago Ave 312-288-6424 60654 IL USA

## aliexpress 400 El Camino South San Mateo  ·  1 txn · $12.99  ·  proposed **—** (0.00)
_no rule or hint matched_
- `326b64ef80692fc1` 2024-12-22 $12.99 Apple Card — aliexpress 400 El Camino South San Mateo 94402 CA USA

## ST DYMPHNAS LLC 65 East 1st Street New York  ·  1 txn · $12.88  ·  proposed **—** (0.00)
_no rule or hint matched_
- `28d8d587618ec68c` 2025-02-22 $12.88 Apple Card — SQ *ST DYMPHNAS LLC 65 East 1st Street New York 10003 NY USA

## INSOMNIA COOKIES- SANT430 State Street SANTA BAR  ·  1 txn · $12.87  ·  proposed **—** (0.00)
_no rule or hint matched_
- `d1af54f89ef25686` 2025-05-20 $12.87 Apple Card — INSOMNIA COOKIES- SANT430 State Street SANTA BARBARA93101 CA USA

## SSEOLSEUDEOIIPATI BUSAN  ·  2 txn · $12.32  ·  proposed **meals_entertainment** (0.60)
_Plaid business_category 'meals'_
- `cade623beba536b8` 2026-06-24 $11.67 Business Platinum Card® — SSEOLSEUDEOIIPATI BUSAN ; Thursday Party Busan
- `9f1e85a2ddc4abb2` 2026-06-24 $0.65 Business Platinum Card® — SSEOLSEUDEOIIPATI BUSAN ; Thursday Party Busan

## WATERSTONES 82 GOWER STREET GOWER ST LONDWC1E 6E  ·  3 txn · $12.28  ·  proposed **—** (0.00)
_no rule or hint matched_
- `b2d8f418442fc444` 2025-06-25 $4.10 Apple Card — WATERSTONES 82 GOWER STREET GOWER ST LONDWC1E 6EQ GBR
- `025e0a7f7367f939` 2025-06-26 $4.09 Apple Card — WATERSTONES 82 GOWER STREET GOWER ST LONDWC1E 6EQ GBR
- `025e0a7f7367f939` 2025-06-26 $4.09 Apple Card — WATERSTONES 82 GOWER STREET GOWER ST LONDWC1E 6EQ GBR

## Store 100 Twin River Rd Lincoln  ·  1 txn · $12.18  ·  proposed **—** (0.00)
_no rule or hint matched_
- `d9e47cfcfe5bfcc4` 2025-02-01 $12.18 Apple Card — Store 100 Twin River Rd Lincoln 02865 RI USA

## JoeJuice_NiceAirport Nice Airport Nice FRAFRA  ·  1 txn · $12.14  ·  proposed **—** (0.00)
_no rule or hint matched_
- `ec6fc222a158e2cf` 2025-07-07 $12.14 Apple Card — JoeJuice_NiceAirport Nice Airport Nice 06200 FRAFRA

## FARO ROMA VIA PIAVE 55 ROMA ITAITA  ·  1 txn · $12.11  ·  proposed **—** (0.00)
_no rule or hint matched_
- `f6705f31a19111eb` 2025-06-22 $12.11 Apple Card — FARO ROMA VIA PIAVE 55 ROMA 00187 ITAITA

## CLASSIC SHOP RIVA 2 OBALA HNP 19 SPLIT 17 HRV  ·  1 txn · $11.57  ·  proposed **—** (0.00)
_no rule or hint matched_
- `fdbd186ec170a6f5` 2025-06-08 $11.57 Apple Card — CLASSIC SHOP RIVA 2 OBALA HNP 19 SPLIT 21000 17 HRV

## LA LA LAND KIND CA5626 Bell Ave Dallas  ·  1 txn · $11.47  ·  proposed **—** (0.00)
_no rule or hint matched_
- `f89c1e96dc3da775` 2025-09-21 $11.47 Apple Card — TST*LA LA LAND KIND CA5626 Bell Ave Dallas 75206 TX USA

## BOSTON HALAL 961 COMMONWEALTH AVE BOSTON  ·  1 txn · $11.10  ·  proposed **—** (0.00)
_no rule or hint matched_
- `ed346db1cdaa3ad7` 2025-05-04 $11.10 Apple Card — BOSTON HALAL 961 COMMONWEALTH AVE BOSTON 02215 MA USA

## ZUNDOUYA DOUTONBORI OSAKAFU OSAKASHI CHUOKU SOEM  ·  1 txn · $10.64  ·  proposed **—** (0.00)
_no rule or hint matched_
- `2623e35663994c71` 2026-06-16 $10.64 Apple Card — ZUNDOUYA DOUTONBORI OSAKAFU OSAKASHI CHUOKU SOEMONCHO OSAKA 5420084 JPNJPN

## MARCEL FAUVETTE 3 RUE DESAIX PARIS 15 FRAFRA  ·  1 txn · $10.47  ·  proposed **—** (0.00)
_no rule or hint matched_
- `ccb44c8478887edf` 2025-06-12 $10.47 Apple Card — MARCEL FAUVETTE 3 RUE DESAIX PARIS 15 75015 FRAFRA

## SWAN 7 COSMO PLACE HOLBORN WC1N 3AP GBR  ·  1 txn · $10.41  ·  proposed **—** (0.00)
_no rule or hint matched_
- `3e2b024f357a0d0d` 2025-07-09 $10.41 Apple Card — SWAN 7 COSMO PLACE HOLBORN WC1N 3AP GBR

## TULUM LA PLACITA SANTURCE 215 C/CANALS SAN JUAN   ·  1 txn · $10.01  ·  proposed **—** (0.00)
_no rule or hint matched_
- `d0b506495d08eafb` 2025-03-07 $10.01 Apple Card — TULUM LA PLACITA SANTURCE 215 C/CANALS SAN JUAN 00907 PR PRI

## DYMPHIES|| 323 Bowery New York  ·  1 txn · $10.00  ·  proposed **—** (0.00)
_no rule or hint matched_
- `af001aa88141ee63` 2025-03-30 $10.00 Apple Card — SQ *DYMPHIES|| 323 Bowery New York 10003 NY USA

## EVOLVE CHIROPRACTIC & 30 FENWAY, STE 1 BOSTON  ·  1 txn · $10.00  ·  proposed **other_opex** (0.90)
_likely personal — Brooks to confirm_
- `2cd67364717d638d` 2025-05-01 $10.00 Apple Card — EVOLVE CHIROPRACTIC & 30 FENWAY, STE 1 BOSTON 02215 MA USA

## The Old Crown 33 New Oxford Street London WC1A 1  ·  1 txn · $9.93  ·  proposed **—** (0.00)
_no rule or hint matched_
- `a00185d7770d443a` 2025-06-01 $9.93 Apple Card — The Old Crown 33 New Oxford Street London WC1A 1BH GBRGBR

## MASSOLI DILETTA PIAZZA DEL BISCIONE 99 ROMA RM I  ·  1 txn · $9.81  ·  proposed **—** (0.00)
_no rule or hint matched_
- `73ac4f25e7fa130b` 2025-06-22 $9.81 Apple Card — MASSOLI DILETTA PIAZZA DEL BISCIONE 99 ROMA 00100 RM ITA

## SumUp *BARBIERI LIA Piazza Dei Cinquecento PIA R  ·  1 txn · $9.80  ·  proposed **—** (0.00)
_no rule or hint matched_
- `bde08e0a1ddf56bf` 2025-06-20 $9.80 Apple Card — SumUp *BARBIERI LIA Piazza Dei Cinquecento PIA Roma 00185 ITA

## Zettle_*Silver Fox GalSilver Fox Gallery Portobe  ·  1 txn · $9.53  ·  proposed **—** (0.00)
_no rule or hint matched_
- `a278090a62dc23f2` 2025-06-18 $9.53 Apple Card — Zettle_*Silver Fox GalSilver Fox Gallery Portobello Rd LONDON W112DY GBRGBR

## TISAK P-2490 OBALA HR.NAR.PREPORODA 6 SPLIT HRV  ·  1 txn · $9.37  ·  proposed **—** (0.00)
_no rule or hint matched_
- `f8a92b763228dd59` 2025-06-07 $9.37 Apple Card — TISAK P-2490 OBALA HR.NAR.PREPORODA 6 SPLIT 21000 HRV

## SumUp *Arafet Abichou8 rue Abel Hovelacque Paris  ·  1 txn · $9.31  ·  proposed **—** (0.00)
_no rule or hint matched_
- `1dfea6e61d5e9fa9` 2025-06-12 $9.31 Apple Card — SumUp *Arafet Abichou8 rue Abel Hovelacque Paris 75013 FRA

## HK0030 - AirpLANTAU HK  ·  2 txn · $9.19  ·  proposed **travel** (0.60)
_Plaid business_category 'travel'_
- `482cfe3e99160c91` 2026-06-25 $4.85 Business Platinum Card® — AplPay HK0030 - AirpLANTAU HK ; Hong Kong Airport Transit
- `37890e7031f017d4` 2026-06-26 $4.34 Business Platinum Card® — AplPay HK0030 - AirpLANTAU HK ; Airport Lantau Transit

## YELLOW APPLE OBALA HRV. PREPORODA 6 Split HR HRV  ·  1 txn · $9.17  ·  proposed **—** (0.00)
_no rule or hint matched_
- `b5bdc924e3a336e7` 2025-06-07 $9.17 Apple Card — YELLOW APPLE OBALA HRV. PREPORODA 6 Split 21000 HR HRV

## BACIO DI LATTE 133 Newport Center Dr Newport Bea  ·  1 txn · $9.15  ·  proposed **—** (0.00)
_no rule or hint matched_
- `00c398aa68c5c4c9` 2025-05-28 $9.15 Apple Card — SQ *BACIO DI LATTE 133 Newport Center Dr Newport Beach92660 CA USA

## BA High 52033451034941BA High 520334510349418 CR  ·  1 txn · $8.89  ·  proposed **—** (0.00)
_no rule or hint matched_
- `607ddd68fa7831bf` 2025-07-07 $8.89 Apple Card — BA High 52033451034941BA High 520334510349418 CRAWLEY RH10 RH10 1JH GBRGBR

## SumUp *Crepes Ice creOUTSIDE KIOSK REGN STOP B L  ·  1 txn · $8.80  ·  proposed **—** (0.00)
_no rule or hint matched_
- `2c336bf6d141e837` 2025-07-27 $8.80 Apple Card — SumUp *Crepes Ice creOUTSIDE KIOSK REGN STOP B London W1B 2EW GBR

## OK SUPERMARKET C. AV DE LAS NACIONES UNI0 NUEVA   ·  1 txn · $8.11  ·  proposed **—** (0.00)
_no rule or hint matched_
- `694c8f6e5c96ab0b` 2025-06-27 $8.11 Apple Card — OK SUPERMARKET C. AV DE LAS NACIONES UNI0 NUEVA ANDALUC29660 ESPESP

## ENOTECA GUERRINI SRL VIA DEI BAULLARI 18 ROMA RM  ·  1 txn · $8.08  ·  proposed **—** (0.00)
_no rule or hint matched_
- `545de7fbcaa6082f` 2025-06-22 $8.08 Apple Card — ENOTECA GUERRINI SRL VIA DEI BAULLARI 18 ROMA 00100 RM ITA

## ESTANCO ROCIO ALGABA PSO.MARTIMO (CASCO URBANO2   ·  1 txn · $8.05  ·  proposed **—** (0.00)
_no rule or hint matched_
- `436adcf2adb8ac62` 2025-06-28 $8.05 Apple Card — ESTANCO ROCIO ALGABA PSO.MARTIMO (CASCO URBANO2 MARBELLA 29602 ESPESP

## PARCHMENT-UNIV DOCS 6263 N. Scottsdale Rd. 480-7  ·  1 txn · $8.00  ·  proposed **—** (0.00)
_no rule or hint matched_
- `f75e911cc1e6b425` 2024-11-11 $8.00 Apple Card — PARCHMENT-UNIV DOCS 6263 N. Scottsdale Rd. #330 480-719-1646 85250 AZ USA

## PBC- CANTON MA317 100 JOHN ROAD CANTON  ·  3 txn · $7.50  ·  proposed **—** (0.00)
_no rule or hint matched_
- `19c70ae1202bf575` 2025-02-28 $2.50 Apple Card — PBC- CANTON MA317 100 JOHN ROAD CANTON 02021 MA USA
- `19c70ae1202bf575` 2025-02-28 $2.50 Apple Card — PBC- CANTON MA317 100 JOHN ROAD CANTON 02021 MA USA
- `46e13a0c39ff479c` 2025-03-20 $2.50 Apple Card — PBC- CANTON MA317 100 JOHN ROAD CANTON 02021 MA USA

## TUFANO PIETRO VIA DANIELE MANIN ROMA ITA  ·  1 txn · $7.50  ·  proposed **—** (0.00)
_no rule or hint matched_
- `7a14c49c72066e06` 2025-06-23 $7.50 Apple Card — TUFANO PIETRO VIA DANIELE MANIN ROMA 00185 ITA

## BENUGO-BRITISH MUSEUM BRITISH MUSEUM LONDON WC1B  ·  1 txn · $7.47  ·  proposed **meals_entertainment** (0.90)
_matched rule 'entertainment venues'_
- `9806cc6608866749` 2025-06-10 $7.47 Apple Card — BENUGO-BRITISH MUSEUM BRITISH MUSEUM LONDON WC1B WC1B 3DG GBR

## Vyta Termini STAZIONE TERMINI SNC ROMA ITAITA  ·  1 txn · $7.15  ·  proposed **—** (0.00)
_no rule or hint matched_
- `38c525f5a0c4aad3` 2025-06-23 $7.15 Apple Card — Vyta Termini STAZIONE TERMINI SNC ROMA 00185 ITAITA

## PRESSED - FASHION ISLA1181 NEWPORT CENTER DR NEW  ·  1 txn · $7.00  ·  proposed **—** (0.00)
_no rule or hint matched_
- `9ec491697e8f75a1` 2025-05-06 $7.00 Apple Card — PRESSED - FASHION ISLA1181 NEWPORT CENTER DR NEWPORT BEACH92660 CA USA

## IPR  ·  1 txn · $7.00  ·  proposed **other_opex** (0.20)
_Plaid business_category 'uncategorized / needs review'_
- `cb974415389519ca` 2026-06-02 $7.00 CHECKING ...6666 — IPR

## IPR* VFJUD TORONTO CAN S356183000657106 CARD 896  ·  1 txn · $7.00  ·  proposed **other_opex** (0.20)
_Plaid business_category 'uncategorized / needs review'_
- `406b3b37b514da00` 2026-07-02 $7.00 CHECKING ...6666 — RECURRING PAYMENT AUTHORIZED ON 07/01 IPR* VFJUD TORONTO CAN S356183000657106 CARD 8963 ; 

## DOC POPCORN THE OUTL CARR 3 STE 205 SPACE K7 CAN  ·  1 txn · $6.96  ·  proposed **—** (0.00)
_no rule or hint matched_
- `b3dffdd187b6e23e` 2025-03-15 $6.96 Apple Card — DOC POPCORN THE OUTL CARR 3 STE 205 SPACE K7 CANOVANAS 00729 PR PRI

## % ARABICA COVENT G5 King Street London WC2E8HN G  ·  1 txn · $6.76  ·  proposed **—** (0.00)
_no rule or hint matched_
- `afa3bc3307561edb` 2025-06-25 $6.76 Apple Card — SQ *% ARABICA COVENT G5 King Street London WC2E8HN GBR

## STUDENAC 354 PUT PLOKITA 26 SPLIT 17 HRV  ·  1 txn · $6.67  ·  proposed **—** (0.00)
_no rule or hint matched_
- `ae4a81b808ac38a1` 2025-06-07 $6.67 Apple Card — STUDENAC 354 PUT PLOKITA 26 SPLIT 21000 17 HRV

## PlaystationNetwork 2207 Bridgepointe Pkwy San Ma  ·  1 txn · $6.36  ·  proposed **other_opex** (0.90)
_looks personal — confirm business purpose or owner_draw_
- `b560dda7054aaf95` 2026-02-14 $6.36 Apple Card — PlaystationNetwork 2207 Bridgepointe Pkwy San Mateo 94404 CA USA

## SJU AIRPORT CONV STOREAEROPUERTO LUIS MUNOZ MA C  ·  1 txn · $6.05  ·  proposed **—** (0.00)
_no rule or hint matched_
- `991aed292a796a50` 2025-03-16 $6.05 Apple Card — SJU AIRPORT CONV STOREAEROPUERTO LUIS MUNOZ MA CAROLINA 00981 PR PRI

## WEBSHARE* RNW PROXY EV440 N BARRANCA AVE#6464 CO  ·  1 txn · $6.00  ·  proposed **—** (0.00)
_no rule or hint matched_
- `7e865f1a2827a6f3` 2024-12-18 $6.00 Apple Card — WEBSHARE* RNW PROXY EV440 N BARRANCA AVE#6464 COVINA 91723 CA USA

## PARKDECKCHAIRS Parkdeck chairs, The Storeyard, R  ·  1 txn · $5.41  ·  proposed **—** (0.00)
_no rule or hint matched_
- `fadf02d3ffa8927e` 2025-07-26 $5.41 Apple Card — SQ *PARKDECKCHAIRS Parkdeck chairs, The Storeyard, Regents Park,NW14NR GBR

## BOOTS 1137 DEPARTURE LOUNGE SOUTH TERMINA GATWIC  ·  2 txn · $5.32  ·  proposed **meals_entertainment** (0.90)
_matched rule 'entertainment venues'_
- `3a38e5f78e597b4c` 2025-07-03 $3.44 Apple Card — BOOTS 1137 DEPARTURE LOUNGE SOUTH TERMINA GATWICK AIRPORH6 0NN GBR
- `45d39e608134c3b0` 2025-07-18 $1.88 Apple Card — BOOTS 1137 DEPARTURE LOUNGE SOUTH TERMINA GATWICK AIRPORH6 0NN GBR

## HAEWOONDAEYAKKOOK BUSAN KOR  ·  1 txn · $5.22  ·  proposed **other_opex** (0.90)
_likely personal — Brooks to confirm_
- `85b9aa286255fce7` 2026-06-23 $5.22 Apple Card — HAEWOONDAEYAKKOOK BUSAN 48095 KOR

## CLASSIC SHOP T8 Obala kneza Domagoja 1 SPLIT 17   ·  1 txn · $4.93  ·  proposed **—** (0.00)
_no rule or hint matched_
- `b4aa56ee1863e972` 2025-06-08 $4.93 Apple Card — CLASSIC SHOP T8 Obala kneza Domagoja 1 SPLIT 21000 17 HRV

## WEBSHARE* RNW PROXY LJ440 N BARRANCA AVE#6464 CO  ·  1 txn · $4.50  ·  proposed **—** (0.00)
_no rule or hint matched_
- `544ae8f36b07143f` 2024-11-18 $4.50 Apple Card — WEBSHARE* RNW PROXY LJ440 N BARRANCA AVE#6464 COVINA 91723 CA USA

## WH Smith Gatwick NorthNorth Tnal Gatwick Airport  ·  1 txn · $4.33  ·  proposed **—** (0.00)
_no rule or hint matched_
- `e7c86cfd7587d764` 2025-06-12 $4.33 Apple Card — WH Smith Gatwick NorthNorth Tnal Gatwick Airport Gatwick Gatwick RH6 0NP GBR

## CASTLE PORTOBELLO ROAD LONDON W11 1W111LU GBR  ·  1 txn · $4.22  ·  proposed **—** (0.00)
_no rule or hint matched_
- `356acdf7c62804ad` 2025-06-18 $4.22 Apple Card — CASTLE PORTOBELLO ROAD LONDON W11 1W111LU GBR

## D Mart 51 Tottenham Court Road London W1T 2EQ GB  ·  1 txn · $4.04  ·  proposed **—** (0.00)
_no rule or hint matched_
- `50672d47c2478b82` 2025-06-01 $4.04 Apple Card — D Mart 51 Tottenham Court Road London W1T 2EQ GBRGBR

## Beam Anson Road SG 079903 SGPSGP  ·  1 txn · $4.02  ·  proposed **—** (0.00)
_no rule or hint matched_
- `4b13e32b8054ef75` 2026-06-18 $4.02 Apple Card — Beam Anson Road SG 079903 SGPSGP

## HILLTOP PLAZA 8117 PRESTON RD DALLAS  ·  1 txn · $4.00  ·  proposed **—** (0.00)
_no rule or hint matched_
- `f169cc8aeaee0a19` 2025-10-08 $4.00 Apple Card — 91853 - HILLTOP PLAZA 8117 PRESTON RD DALLAS 75225 TX USA

## BLANK STREET UK LIBasement & Ground Floors, 300   ·  1 txn · $3.93  ·  proposed **—** (0.00)
_no rule or hint matched_
- `e894de69a53c18d5` 2025-06-04 $3.93 Apple Card — SQ *BLANK STREET UK LIBasement & Ground Floors, 300 Pentonville Road London N1 9NR GBR

## Moonhoaeuimoo  ·  1 txn · $3.90  ·  proposed **other_opex** (0.20)
_Plaid business_category 'uncategorized / needs review'_
- `7f3183b0020508ec` 2026-06-23 $3.90 Business Platinum Card® — Moonhoaeuimoo Busan

## SumUp *two sizes srl via del governo vecchio 88   ·  1 txn · $3.46  ·  proposed **—** (0.00)
_no rule or hint matched_
- `87ab175dae7077b2` 2025-06-22 $3.46 Apple Card — SumUp *two sizes srl via del governo vecchio 88 rm 00186 ITA

## CLASSIC SHOP T7 Obala Hrvatskog narodno SPLIT 17  ·  1 txn · $3.32  ·  proposed **—** (0.00)
_no rule or hint matched_
- `c7e6ede14099c8d1` 2025-06-09 $3.32 Apple Card — CLASSIC SHOP T7 Obala Hrvatskog narodno SPLIT 21000 17 HRV

## Selecta SAS Immeuble le Mermoz, 53 Av Le Bourget  ·  1 txn · $3.02  ·  proposed **—** (0.00)
_no rule or hint matched_
- `2b0a4f21097e3c59` 2025-06-16 $3.02 Apple Card — Selecta SAS Immeuble le Mermoz, 53 Av Le Bourget 93350 FRAFRA

## CHOOSE GREEN PLANT DOVERSKA 24 SPLIT 17 HRV  ·  1 txn · $2.98  ·  proposed **—** (0.00)
_no rule or hint matched_
- `00fec3fabdd19d26` 2025-06-09 $2.98 Apple Card — CHOOSE GREEN PLANT DOVERSKA 24 SPLIT 21000 17 HRV

## DELICIJE 4 OBALA HRV. NAR. PREPOROD Split HR HRV  ·  1 txn · $2.62  ·  proposed **—** (0.00)
_no rule or hint matched_
- `4da3a8361486aadf` 2025-06-09 $2.62 Apple Card — DELICIJE 4 OBALA HRV. NAR. PREPOROD Split 21000 HR HRV

## MBTA-550007839164-455918 TREMONT ST STE100 BOSTO  ·  1 txn · $2.40  ·  proposed **—** (0.00)
_no rule or hint matched_
- `1bb411823ed595d7` 2025-05-02 $2.40 Apple Card — MBTA-550007839164-455918 TREMONT ST STE100 BOSTON 02116 MA USA

## TERMINI B DIR LAUR PIAZZA DEI CINQUECENTO ROMA I  ·  1 txn · $2.31  ·  proposed **—** (0.00)
_no rule or hint matched_
- `b3a2fc3dbd15d829` 2025-06-20 $2.31 Apple Card — TERMINI B DIR LAUR PIAZZA DEI CINQUECENTO ROMA 00185 ITA

## IL VITTORIANO PIAZZA VENEZIA 1 ROMA RM ITA  ·  1 txn · $2.31  ·  proposed **—** (0.00)
_no rule or hint matched_
- `4c1132c28835648b` 2025-06-22 $2.31 Apple Card — IL VITTORIANO PIAZZA VENEZIA 1 ROMA 00186 RM ITA

## SOGEDAI Via F. III Gracchi 40/42 CINISELLO BAL20  ·  2 txn · $2.30  ·  proposed **—** (0.00)
_no rule or hint matched_
- `6bf71e6854101f7d` 2025-06-21 $1.15 Apple Card — SOGEDAI Via F. III Gracchi 40/42 CINISELLO BAL20092 ITAITA
- `6bf71e6854101f7d` 2025-06-21 $1.15 Apple Card — SOGEDAI Via F. III Gracchi 40/42 CINISELLO BAL20092 ITAITA

## NAME-CHEAP.COM* OCV7RC4600 East Washington Stree  ·  1 txn · $1.96  ·  proposed **—** (0.00)
_no rule or hint matched_
- `4373c3007e232e17` 2024-11-06 $1.96 Apple Card — NAME-CHEAP.COM* OCV7RC4600 East Washington Street, Suite 305 PHOENIX 85034 AZ USA

## NAME-CHEAP.COM* ZSK4NY4600 East Washington Stree  ·  1 txn · $1.96  ·  proposed **—** (0.00)
_no rule or hint matched_
- `adef3a9ccdbb01da` 2024-11-12 $1.96 Apple Card — NAME-CHEAP.COM* ZSK4NY4600 East Washington Street, Suite 305 PHOENIX 85034 AZ USA

## NAME-CHEAP.COM* UZIVXL4600 East Washington Stree  ·  1 txn · $1.96  ·  proposed **—** (0.00)
_no rule or hint matched_
- `d3fa63eb5983bc17` 2024-11-16 $1.96 Apple Card — NAME-CHEAP.COM* UZIVXL4600 East Washington Street, Suite 305 PHOENIX 85034 AZ USA

## NAME-CHEAP.COM* O4FROL4600 East Washington Stree  ·  1 txn · $1.96  ·  proposed **—** (0.00)
_no rule or hint matched_
- `6f5ca137408e48d5` 2024-11-18 $1.96 Apple Card — NAME-CHEAP.COM* O4FROL4600 East Washington Street, Suite 305 PHOENIX 85034 AZ USA

## NAME-CHEAP.COM* CO7UDZ4600 East Washington Stree  ·  1 txn · $1.96  ·  proposed **—** (0.00)
_no rule or hint matched_
- `6c0017ab862f1a9e` 2024-11-19 $1.96 Apple Card — NAME-CHEAP.COM* CO7UDZ4600 East Washington Street, Suite 305 PHOENIX 85034 AZ USA

## NAME-CHEAP.COM* JLJ2AL4600 East Washington Stree  ·  1 txn · $1.96  ·  proposed **—** (0.00)
_no rule or hint matched_
- `c14a4be86b77764b` 2024-11-19 $1.96 Apple Card — NAME-CHEAP.COM* JLJ2AL4600 East Washington Street, Suite 305 PHOENIX 85034 AZ USA

## NAME-CHEAP.COM* DZLG1F4600 East Washington Stree  ·  1 txn · $1.96  ·  proposed **—** (0.00)
_no rule or hint matched_
- `f92965bfa8eea9a3` 2024-11-21 $1.96 Apple Card — NAME-CHEAP.COM* DZLG1F4600 East Washington Street, Suite 305 PHOENIX 85034 AZ USA

## NAME-CHEAP.COM* HOLC2Z4600 East Washington Stree  ·  1 txn · $1.96  ·  proposed **—** (0.00)
_no rule or hint matched_
- `f4af5e81fef911ab` 2024-11-21 $1.96 Apple Card — NAME-CHEAP.COM* HOLC2Z4600 East Washington Street, Suite 305 PHOENIX 85034 AZ USA

## NAME-CHEAP.COM* GQ0YJN4600 East Washington Stree  ·  1 txn · $1.96  ·  proposed **—** (0.00)
_no rule or hint matched_
- `18cfa65f2467caa9` 2024-12-20 $1.96 Apple Card — NAME-CHEAP.COM* GQ0YJN4600 East Washington Street, Suite 305 PHOENIX 85034 AZ USA

## ATAC TAP&GO VIA PRENESTINA 45 ROMA ITA  ·  1 txn · $1.73  ·  proposed **—** (0.00)
_no rule or hint matched_
- `8974a0c727581019` 2025-06-21 $1.73 Apple Card — ATAC TAP&GO VIA PRENESTINA 45 ROMA 00100 ITA

## MBTA-550007839164-208810 PARK PLAZA BOSTON  ·  1 txn · $1.70  ·  proposed **—** (0.00)
_no rule or hint matched_
- `6755d87575545cf6` 2024-11-12 $1.70 Apple Card — MBTA-550007839164-208810 PARK PLAZA BOSTON 02116 MA USA

## SEOUL TRANSPORTATION CSEOULSEONGDONG-GUYONGDAP-D  ·  2 txn · $1.69  ·  proposed **—** (0.00)
_no rule or hint matched_
- `cbb4776ee3967487` 2026-06-18 $0.33 Apple Card — SEOUL TRANSPORTATION CSEOULSEONGDONG-GUYONGDAP-DONG Seoul 04806 KOR
- `f8a68d4be0d1fc8e` 2026-06-18 $1.36 Apple Card — SEOUL TRANSPORTATION CSEOULSEONGDONG-GUYONGDAP-DONG Seoul 04806 KOR

## Nyx*KM DISPENSING LLC 147 North Rd Chelmsford  ·  1 txn · $1.50  ·  proposed **—** (0.00)
_no rule or hint matched_
- `42d8735e9761f58d` 2025-02-18 $1.50 Apple Card — Nyx*KM DISPENSING LLC 147 North Rd Chelmsford 01824 MA USA

## Nayax **KM Dispensing North Road Chilmark  ·  1 txn · $1.50  ·  proposed **—** (0.00)
_no rule or hint matched_
- `fbb2645537c64e5e` 2025-05-05 $1.50 Apple Card — Nayax **KM Dispensing North Road Chilmark 02535 MA USA

## 7/24 SUPERMARKET 6 C. JULIO IGLESIAS, LOCAL 4 PU  ·  1 txn · $1.17  ·  proposed **—** (0.00)
_no rule or hint matched_
- `c1ab4a98418d61ca` 2025-07-19 $1.17 Apple Card — 7/24 SUPERMARKET 6 C. JULIO IGLESIAS, LOCAL 4 PUERTO BANUS 29660 ESPESP

## GSU UNION COURT 775 COMMONWEALTH AVE BOSTON  ·  1 txn · $1.04  ·  proposed **—** (0.00)
_no rule or hint matched_
- `80e415321531221f` 2024-12-06 $1.04 Apple Card — GSU UNION COURT 775 COMMONWEALTH AVE BOSTON 02215 MA USA

## Kocespay.korea Seoul Kor  ·  1 txn · $0.66  ·  proposed **other_opex** (0.20)
_Plaid business_category 'uncategorized / needs review'_
- `eb357fd7da559749` 2026-06-23 $0.66 CHECKING ...6666 — Kocespay.korea Seoul Kor ; KOCES Pay
