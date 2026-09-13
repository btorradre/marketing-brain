# Product-Type Design System Database

This is the database that powers "Establish a design system before writing any component" (see SKILL.md). Given a product type (e.g. SaaS, Healthcare, Beauty, Fintech, Marketplace), it maps to a recommended style, landing-page pattern, color-palette focus, and a set of decision rules / anti-patterns — so style, color, and layout choices are made deliberately and consistently rather than ad hoc, component by component.

There are three linked tables below, all keyed to the same ~161 product types:

1. **Product types → style/pattern recommendation** (`products.csv`) — for each product type: matching keywords, the primary style recommendation, secondary style options, the recommended landing-page pattern, a dashboard style (where applicable), the color-palette focus, and key considerations.
2. **Landing-page patterns** (`landing.csv`) — 34 named page-structure patterns (Hero + Features + CTA, Hero-Centric + Trust, etc.), each with its section order, primary CTA placement, color strategy, recommended effects, and conversion-optimization notes.
3. **Design-system reasoning rules** (`ui-reasoning.csv`) — the same ~161 categories with a recommended pattern, style priority, color mood, typography mood, key effects, a machine-readable `Decision_Rules` JSON block (conditional logic such as `"if_ux_focused": "prioritize-minimalism"`), anti-patterns to avoid, and a severity rating. This is the reasoning layer the original tool's `--design-system` flag applies on top of the raw product/style/color tables.

## 1. Product types → style/pattern recommendation

| No | Product Type | Keywords | Primary Style Recommendation | Secondary Styles | Landing Page Pattern | Dashboard Style (if applicable) | Color Palette Focus | Key Considerations |
|---|---|---|---|---|---|---|---|---|
| 1 | SaaS (General) | app, b2b, cloud, general, saas, software, subscription | Glassmorphism + Flat Design | Soft UI Evolution, Minimalism | Hero + Features + CTA | Data-Dense + Real-Time Monitoring | Trust blue + accent contrast | Balance modern feel with clarity. Focus on CTAs. |
| 2 | Micro SaaS | app, b2b, cloud, indie, micro, micro-saas, niche, saas, small, software, solo, subscription | Flat Design + Vibrant & Block | Motion-Driven, Micro-interactions | Minimal & Direct + Demo | Executive Dashboard | Vibrant primary + white space | Keep simple, show product quickly. Speed is key. |
| 3 | E-commerce | buy, commerce, e, ecommerce, products, retail, sell, shop, store | Vibrant & Block-based | Aurora UI, Motion-Driven | Feature-Rich Showcase | Sales Intelligence Dashboard | Brand primary + success green | Engagement & conversions. High visual hierarchy. |
| 4 | E-commerce Luxury | buy, commerce, e, ecommerce, elegant, exclusive, high-end, luxury, premium, products, retail, sell, shop, store | Liquid Glass + Glassmorphism | 3D & Hyperrealism, Aurora UI | Feature-Rich Showcase | Sales Intelligence Dashboard | Premium colors + minimal accent | Elegance & sophistication. Premium materials. |
| 5 | B2B Service | appointment, b, b2b, booking, business, consultation, corporate, enterprise, service | Trust & Authority + Minimal | Feature-Rich, Conversion-Optimized | Feature-Rich Showcase | Sales Intelligence Dashboard | Professional blue + neutral grey | Credibility essential. Clear ROI messaging. |
| 6 | Financial Dashboard | admin, analytics, dashboard, data, financial, panel | Dark Mode (OLED) + Data-Dense | Minimalism, Accessible & Ethical | N/A - Dashboard focused | Financial Dashboard | Dark bg + red/green alerts + trust blue | High contrast, real-time updates, accuracy paramount. |
| 7 | Analytics Dashboard | admin, analytics, dashboard, data, panel | Data-Dense + Heat Map & Heatmap | Minimalism, Dark Mode (OLED) | N/A - Analytics focused | Drill-Down Analytics + Comparative | Cool→Hot gradients + neutral grey | Clarity > aesthetics. Color-coded data priority. |
| 8 | Healthcare App | app, clinic, health, healthcare, medical, patient | Neumorphism + Accessible & Ethical | Soft UI Evolution, Claymorphism (for patients) | Social Proof-Focused | User Behavior Analytics | Calm blue + health green + trust | Accessibility mandatory. Calming aesthetic. |
| 9 | Educational App | app, course, education, educational, learning, school, training | Claymorphism + Micro-interactions | Vibrant & Block-based, Flat Design | Storytelling-Driven | User Behavior Analytics | Playful colors + clear hierarchy | Engagement & ease of use. Age-appropriate design. |
| 10 | Creative Agency | agency, creative, design, marketing, studio | Brutalism + Motion-Driven | Retro-Futurism, Storytelling-Driven | Storytelling-Driven | N/A - Portfolio focused | Bold primaries + artistic freedom | Differentiation key. Wow-factor necessary. |
| 11 | Portfolio/Personal | creative, personal, portfolio, projects, showcase, work | Motion-Driven + Minimalism | Brutalism, Aurora UI | Storytelling-Driven | N/A - Personal branding | Brand primary + artistic interpretation | Showcase work. Personality shine through. |
| 12 | Gaming | entertainment, esports, game, gaming, play | 3D & Hyperrealism + Retro-Futurism | Motion-Driven, Vibrant & Block | Feature-Rich Showcase | N/A - Game focused | Vibrant + neon + immersive colors | Immersion priority. Performance critical. |
| 13 | Government/Public Service | appointment, booking, consultation, government, public, service | Accessible & Ethical + Minimalism | Flat Design, Inclusive Design | Minimal & Direct | Executive Dashboard | Professional blue + high contrast | WCAG AAA mandatory. Trust paramount. |
| 14 | Fintech/Crypto | banking, blockchain, crypto, defi, finance, fintech, money, nft, payment, web3 | Glassmorphism + Dark Mode (OLED) | Retro-Futurism, Motion-Driven | Conversion-Optimized | Real-Time Monitoring + Predictive | Dark tech colors + trust + vibrant accents | Security perception. Real-time data critical. |
| 15 | Social Media App | app, community, content, entertainment, media, network, sharing, social, streaming, users, video | Vibrant & Block-based + Motion-Driven | Aurora UI, Micro-interactions | Feature-Rich Showcase | User Behavior Analytics | Vibrant + engagement colors | Engagement & retention. Addictive design ethics. |
| 16 | Productivity Tool | collaboration, productivity, project, task, tool, workflow | Flat Design + Micro-interactions | Minimalism, Soft UI Evolution | Interactive Product Demo | Drill-Down Analytics | Clear hierarchy + functional colors | Ease of use. Speed & efficiency focus. |
| 17 | Design System/Component Library | component, design, library, system | Minimalism + Accessible & Ethical | Flat Design, Zero Interface | Feature-Rich Showcase | N/A - Dev focused | Clear hierarchy + code-like structure | Consistency. Developer-first approach. |
| 18 | AI/Chatbot Platform | ai, artificial-intelligence, automation, chatbot, machine-learning, ml, platform | AI-Native UI + Minimalism | Zero Interface, Glassmorphism | Interactive Product Demo | AI/ML Analytics Dashboard | Neutral + AI Purple (#6366F1) | Conversational UI. Streaming text. Context awareness. Minimal chrome. |
| 19 | NFT/Web3 Platform | nft, platform, web | Cyberpunk UI + Glassmorphism | Aurora UI, 3D & Hyperrealism | Feature-Rich Showcase | Crypto/Blockchain Dashboard | Dark + Neon + Gold (#FFD700) | Wallet integration. Transaction feedback. Gas fees display. Dark mode essential. |
| 20 | Creator Economy Platform | creator, economy, platform | Vibrant & Block-based + Bento Box Grid | Motion-Driven, Aurora UI | Social Proof-Focused | User Behavior Analytics | Vibrant + Brand colors | Creator profiles. Monetization display. Engagement metrics. Social proof. |
| 21 | Remote Work/Collaboration Tool | collaboration, remote, tool, work | Soft UI Evolution + Minimalism | Glassmorphism, Micro-interactions | Feature-Rich Showcase | Drill-Down Analytics | Calm Blue + Neutral grey | Real-time collaboration. Status indicators. Video integration. Notification management. |
| 22 | Mental Health App | app, health, mental | Neumorphism + Accessible & Ethical | Claymorphism, Soft UI Evolution | Social Proof-Focused | Healthcare Analytics | Calm Pastels + Trust colors | Calming aesthetics. Privacy-first. Crisis resources. Progress tracking. Accessibility mandatory. |
| 23 | Pet Tech App | app, pet, tech | Claymorphism + Vibrant & Block-based | Micro-interactions, Flat Design | Storytelling-Driven | User Behavior Analytics | Playful + Warm colors | Pet profiles. Health tracking. Playful UI. Photo galleries. Vet integration. |
| 24 | Smart Home/IoT Dashboard | admin, analytics, dashboard, data, home, iot, panel, smart | Glassmorphism + Dark Mode (OLED) | Minimalism, AI-Native UI | Interactive Product Demo | Real-Time Monitoring | Dark + Status indicator colors | Device status. Real-time controls. Energy monitoring. Automation rules. Quick actions. |
| 25 | EV/Charging Ecosystem | charging, ecosystem, ev | Minimalism + Aurora UI | Glassmorphism, Organic Biophilic | Hero-Centric Design | Energy/Utilities Dashboard | Electric Blue (#009CD1) + Green | Charging station maps. Range estimation. Cost calculation. Environmental impact. |
| 26 | Subscription Box Service | appointment, booking, box, consultation, membership, plan, recurring, service, subscription | Vibrant & Block-based + Motion-Driven | Claymorphism, Aurora UI | Feature-Rich Showcase | E-commerce Analytics | Brand + Excitement colors | Unboxing experience. Personalization quiz. Subscription management. Product reveals. |
| 27 | Podcast Platform | platform, podcast | Dark Mode (OLED) + Minimalism | Motion-Driven, Vibrant & Block-based | Storytelling-Driven | Media/Entertainment Dashboard | Dark + Audio waveform accents | Audio player UX. Episode discovery. Creator tools. Analytics for podcasters. |
| 28 | Dating App | app, dating | Vibrant & Block-based + Motion-Driven | Aurora UI, Glassmorphism | Social Proof-Focused | User Behavior Analytics | Warm + Romantic (Pink/Red gradients) | Profile cards. Swipe interactions. Match animations. Safety features. Video chat. |
| 29 | Micro-Credentials/Badges Platform | badges, credentials, micro, platform | Minimalism + Flat Design | Accessible & Ethical, Swiss Modernism 2.0 | Trust & Authority | Education Dashboard | Trust Blue + Gold (#FFD700) | Credential verification. Badge display. Progress tracking. Issuer trust. LinkedIn integration. |
| 30 | Knowledge Base/Documentation | base, documentation, knowledge | Minimalism + Accessible & Ethical | Swiss Modernism 2.0, Flat Design | FAQ/Documentation | N/A - Documentation focused | Clean hierarchy + minimal color | Search-first. Clear navigation. Code highlighting. Version switching. Feedback system. |
| 31 | Hyperlocal Services | appointment, booking, consultation, hyperlocal, service, services | Minimalism + Vibrant & Block-based | Micro-interactions, Flat Design | Conversion-Optimized | Drill-Down Analytics + Map | Location markers + Trust colors | Map integration. Service categories. Provider profiles. Booking system. Reviews. |
| 32 | Beauty/Spa/Wellness Service | appointment, beauty, booking, consultation, service, spa, wellness | Soft UI Evolution + Neumorphism | Glassmorphism, Minimalism | Hero-Centric Design + Social Proof | User Behavior Analytics | Soft pastels (Pink #FFB6C1 Sage #90EE90) + Cream + Gold accents | Calming aesthetic. Booking system. Service menu. Before/after gallery. Testimonials. Relaxing imagery. |
| 33 | Luxury/Premium Brand | brand, elegant, exclusive, high-end, luxury, premium | Liquid Glass + Glassmorphism | Minimalism, 3D & Hyperrealism | Storytelling-Driven + Feature-Rich | Sales Intelligence Dashboard | Black + Gold (#FFD700) + White + Minimal accent | Elegance paramount. Premium imagery. Storytelling. High-quality visuals. Exclusive feel. |
| 34 | Restaurant/Food Service | appointment, booking, consultation, delivery, food, menu, order, restaurant, service | Vibrant & Block-based + Motion-Driven | Claymorphism, Flat Design | Hero-Centric Design + Conversion | N/A - Booking focused | Warm colors (Orange Red Brown) + appetizing imagery | Menu display. Online ordering. Reservation system. Food photography. Location/hours prominent. |
| 35 | Fitness/Gym App | app, exercise, fitness, gym, health, workout | Vibrant & Block-based + Dark Mode (OLED) | Motion-Driven, Neumorphism | Feature-Rich Showcase | User Behavior Analytics | Energetic (Orange #FF6B35 Electric Blue) + Dark bg | Progress tracking. Workout plans. Community features. Achievements. Motivational design. |
| 36 | Real Estate/Property | buy, estate, housing, property, real, real-estate, rent | Glassmorphism + Minimalism | Motion-Driven, 3D & Hyperrealism | Hero-Centric Design + Feature-Rich | Sales Intelligence Dashboard | Trust Blue (#0077B6) + Gold accents + White | Property listings. Virtual tours. Map integration. Agent profiles. Mortgage calculator. High-quality imagery. |
| 37 | Travel/Tourism Agency | agency, booking, creative, design, flight, hotel, marketing, studio, tourism, travel, vacation | Aurora UI + Motion-Driven | Vibrant & Block-based, Glassmorphism | Storytelling-Driven + Hero-Centric | Booking Analytics | Vibrant destination colors + Sky Blue + Warm accents | Destination showcase. Booking system. Itinerary builder. Reviews. Inspiration galleries. Mobile-first. |
| 38 | Hotel/Hospitality | hospitality, hotel | Liquid Glass + Minimalism | Glassmorphism, Soft UI Evolution | Hero-Centric Design + Social Proof | Revenue Management Dashboard | Warm neutrals + Gold (#D4AF37) + Brand accent | Room booking. Amenities showcase. Location maps. Guest reviews. Seasonal pricing. Luxury imagery. |
| 39 | Wedding/Event Planning | conference, event, meetup, planning, registration, ticket, wedding | Soft UI Evolution + Aurora UI | Glassmorphism, Motion-Driven | Storytelling-Driven + Social Proof | N/A - Planning focused | Soft Pink (#FFD6E0) + Gold + Cream + Sage | Portfolio gallery. Vendor directory. Planning tools. Timeline. Budget tracker. Romantic aesthetic. |
| 40 | Legal Services | appointment, attorney, booking, compliance, consultation, contract, law, legal, service, services | Trust & Authority + Minimalism | Accessible & Ethical, Swiss Modernism 2.0 | Trust & Authority + Minimal | Case Management Dashboard | Navy Blue (#1E3A5F) + Gold + White | Credibility paramount. Practice areas. Attorney profiles. Case results. Contact forms. Professional imagery. |
| 41 | Insurance Platform | insurance, platform | Trust & Authority + Flat Design | Accessible & Ethical, Minimalism | Conversion-Optimized + Trust | Claims Analytics Dashboard | Trust Blue (#0066CC) + Green (security) + Neutral | Quote calculator. Policy comparison. Claims process. Trust signals. Clear pricing. Security badges. |
| 42 | Banking/Traditional Finance | banking, finance, traditional | Minimalism + Accessible & Ethical | Trust & Authority, Dark Mode (OLED) | Trust & Authority + Feature-Rich | Financial Dashboard | Navy (#0A1628) + Trust Blue + Gold accents | Security-first. Account overview. Transaction history. Mobile banking. Accessibility critical. Trust paramount. |
| 43 | Online Course/E-learning | course, e, learning, online | Claymorphism + Vibrant & Block-based | Motion-Driven, Flat Design | Feature-Rich Showcase + Social Proof | Education Dashboard | Vibrant learning colors + Progress green | Course catalog. Progress tracking. Video player. Quizzes. Certificates. Community forums. Gamification. |
| 44 | Non-profit/Charity | charity, non, profit | Accessible & Ethical + Organic Biophilic | Minimalism, Storytelling-Driven | Storytelling-Driven + Trust | Donation Analytics Dashboard | Cause-related colors + Trust + Warm | Impact stories. Donation flow. Transparency reports. Volunteer signup. Event calendar. Emotional connection. |
| 45 | Music Streaming | music, streaming | Dark Mode (OLED) + Vibrant & Block-based | Motion-Driven, Aurora UI | Feature-Rich Showcase | Media/Entertainment Dashboard | Dark (#121212) + Vibrant accents + Album art colors | Audio player. Playlist management. Artist pages. Personalization. Social features. Waveform visualizations. |
| 46 | Video Streaming/OTT | ott, streaming, video | Dark Mode (OLED) + Motion-Driven | Glassmorphism, Vibrant & Block-based | Hero-Centric Design + Feature-Rich | Media/Entertainment Dashboard | Dark bg + Content poster colors + Brand accent | Video player. Content discovery. Watchlist. Continue watching. Personalized recommendations. Thumbnail-heavy. |
| 47 | Job Board/Recruitment | board, job, recruitment | Flat Design + Minimalism | Vibrant & Block-based, Accessible & Ethical | Conversion-Optimized + Feature-Rich | HR Analytics Dashboard | Professional Blue + Success Green + Neutral | Job listings. Search/filter. Company profiles. Application tracking. Resume upload. Salary insights. |
| 48 | Marketplace (P2P) | buyers, listings, marketplace, p, platform, sellers | Vibrant & Block-based + Flat Design | Micro-interactions, Trust & Authority | Feature-Rich Showcase + Social Proof | E-commerce Analytics | Trust colors + Category colors + Success green | Seller/buyer profiles. Listings. Reviews/ratings. Secure payment. Messaging. Search/filter. Trust badges. |
| 49 | Logistics/Delivery | delivery, logistics | Minimalism + Flat Design | Dark Mode (OLED), Micro-interactions | Feature-Rich Showcase + Conversion | Real-Time Monitoring + Route Analytics | Blue (#2563EB) + Orange (tracking) + Green (delivered) | Real-time tracking. Delivery scheduling. Route optimization. Driver management. Status updates. Map integration. |
| 50 | Agriculture/Farm Tech | agriculture, farm, tech | Organic Biophilic + Flat Design | Minimalism, Accessible & Ethical | Feature-Rich Showcase + Trust | IoT Sensor Dashboard | Earth Green (#4A7C23) + Brown + Sky Blue | Crop monitoring. Weather data. IoT sensors. Yield tracking. Market prices. Sustainable imagery. |
| 51 | Construction/Architecture | architecture, construction | Minimalism + 3D & Hyperrealism | Brutalism, Swiss Modernism 2.0 | Hero-Centric Design + Feature-Rich | Project Management Dashboard | Grey (#4A4A4A) + Orange (safety) + Blueprint Blue | Project portfolio. 3D renders. Timeline. Material specs. Team collaboration. Blueprint aesthetic. |
| 52 | Automotive/Car Dealership | automotive, car, dealership | Motion-Driven + 3D & Hyperrealism | Dark Mode (OLED), Glassmorphism | Hero-Centric Design + Feature-Rich | Sales Intelligence Dashboard | Brand colors + Metallic accents + Dark/Light | Vehicle showcase. 360° views. Comparison tools. Financing calculator. Test drive booking. High-quality imagery. |
| 53 | Photography Studio | photography, studio | Motion-Driven + Minimalism | Aurora UI, Glassmorphism | Storytelling-Driven + Hero-Centric | N/A - Portfolio focused | Black + White + Minimal accent | Portfolio gallery. Before/after. Service packages. Booking system. Client galleries. Full-bleed imagery. |
| 54 | Coworking Space | coworking, space | Vibrant & Block-based + Glassmorphism | Minimalism, Motion-Driven | Hero-Centric Design + Feature-Rich | Occupancy Dashboard | Energetic colors + Wood tones + Brand accent | Space tour. Membership plans. Booking system. Amenities. Community events. Virtual tour. |
| 55 | Home Services (Plumber/Electrician) | appointment, booking, consultation, electrician, home, plumber, service, services | Flat Design + Trust & Authority | Minimalism, Accessible & Ethical | Conversion-Optimized + Trust | Service Analytics | Trust Blue + Safety Orange + Professional grey | Service list. Emergency contact. Booking. Price transparency. Certifications. Local trust signals. |
| 56 | Childcare/Daycare | childcare, daycare | Claymorphism + Vibrant & Block-based | Soft UI Evolution, Accessible & Ethical | Social Proof-Focused + Trust | Parent Dashboard | Playful pastels + Safe colors + Warm accents | Programs. Staff profiles. Safety certifications. Parent portal. Activity updates. Cheerful imagery. |
| 57 | Senior Care/Elderly | care, elderly, senior | Accessible & Ethical + Soft UI Evolution | Minimalism, Neumorphism | Trust & Authority + Social Proof | Healthcare Analytics | Calm Blue + Warm neutrals + Large text | Care services. Staff qualifications. Facility tour. Family portal. Large touch targets. High contrast. Accessibility-first. |
| 58 | Medical Clinic | clinic, medical | Accessible & Ethical + Minimalism | Neumorphism, Trust & Authority | Trust & Authority + Conversion | Healthcare Analytics | Medical Blue (#0077B6) + Trust White + Calm Green | Services. Doctor profiles. Online booking. Patient portal. Insurance info. HIPAA compliant. Trust signals. |
| 59 | Pharmacy/Drug Store | drug, pharmacy, store | Flat Design + Accessible & Ethical | Minimalism, Trust & Authority | Conversion-Optimized + Trust | Inventory Dashboard | Pharmacy Green + Trust Blue + Clean White | Product catalog. Prescription upload. Refill reminders. Health info. Store locator. Safety certifications. |
| 60 | Dental Practice | dental, practice | Soft UI Evolution + Minimalism | Accessible & Ethical, Trust & Authority | Social Proof-Focused + Conversion | Patient Analytics | Fresh Blue + White + Smile Yellow accent | Services. Dentist profiles. Before/after. Online booking. Insurance. Patient testimonials. Friendly imagery. |
| 61 | Veterinary Clinic | clinic, veterinary | Claymorphism + Accessible & Ethical | Soft UI Evolution, Flat Design | Social Proof-Focused + Trust | Pet Health Dashboard | Caring Blue + Pet-friendly colors + Warm accents | Pet services. Vet profiles. Online booking. Pet portal. Emergency info. Friendly animal imagery. |
| 62 | Florist/Plant Shop | florist, plant, shop | Organic Biophilic + Vibrant & Block-based | Aurora UI, Motion-Driven | Hero-Centric Design + Conversion | E-commerce Analytics | Natural Green + Floral pinks/purples + Earth tones | Product catalog. Occasion categories. Delivery scheduling. Care guides. Seasonal collections. Beautiful imagery. |
| 63 | Bakery/Cafe | bakery, cafe | Vibrant & Block-based + Soft UI Evolution | Claymorphism, Motion-Driven | Hero-Centric Design + Conversion | N/A - Order focused | Warm Brown + Cream + Appetizing accents | Menu display. Online ordering. Location/hours. Catering. Seasonal specials. Appetizing photography. |
| 64 | Brewery/Winery | brewery, winery | Motion-Driven + Storytelling-Driven | Dark Mode (OLED), Organic Biophilic | Storytelling-Driven + Hero-Centric | N/A - E-commerce focused | Deep amber/burgundy + Gold + Craft aesthetic | Product showcase. Story/heritage. Tasting notes. Events. Club membership. Artisanal imagery. |
| 65 | Airline | airline, aviation, flight, travel, booking, airport, flying | Minimalism + Glassmorphism | Motion-Driven, Accessible & Ethical | Conversion-Optimized + Feature-Rich | Operations Dashboard | Sky Blue + Brand colors + Trust accents | Flight search. Booking. Check-in. Boarding pass. Loyalty program. Route maps. Mobile-first. |
| 66 | News/Media Platform | content, entertainment, media, news, platform, streaming, video | Minimalism + Flat Design | Dark Mode (OLED), Accessible & Ethical | Hero-Centric Design + Feature-Rich | Media Analytics Dashboard | Brand colors + High contrast + Category colors | Article layout. Breaking news. Categories. Search. Subscription. Mobile reading. Fast loading. |
| 67 | Magazine/Blog | articles, blog, content, magazine, posts, writing | Swiss Modernism 2.0 + Motion-Driven | Minimalism, Aurora UI | Storytelling-Driven + Hero-Centric | Content Analytics | Editorial colors + Brand primary + Clean white | Article showcase. Category navigation. Author profiles. Newsletter signup. Related content. Typography-focused. |
| 68 | Freelancer Platform | freelancer, platform | Flat Design + Minimalism | Vibrant & Block-based, Micro-interactions | Feature-Rich Showcase + Conversion | Marketplace Analytics | Professional Blue + Success Green + Neutral | Profile creation. Portfolio. Skill matching. Messaging. Payment. Reviews. Project management. |
| 69 | Marketing Agency | agency, creative, design, marketing, studio | Brutalism + Motion-Driven | Vibrant & Block-based, Aurora UI | Storytelling-Driven + Feature-Rich | Campaign Analytics | Bold brand colors + Creative freedom | Portfolio. Case studies. Services. Team. Creative showcase. Results-focused. Bold aesthetic. |
| 70 | Event Management | conference, event, management, meetup, registration, ticket | Vibrant & Block-based + Motion-Driven | Glassmorphism, Aurora UI | Hero-Centric Design + Feature-Rich | Event Analytics | Event theme colors + Excitement accents | Event showcase. Registration. Agenda. Speakers. Sponsors. Ticket sales. Countdown timer. |
| 71 | Membership/Community | community, membership | Vibrant & Block-based + Soft UI Evolution | Bento Box Grid, Micro-interactions | Social Proof-Focused + Conversion | Community Analytics | Community brand colors + Engagement accents | Member benefits. Pricing tiers. Community showcase. Events. Member directory. Exclusive content. |
| 72 | Newsletter Platform | newsletter, platform | Minimalism + Flat Design | Swiss Modernism 2.0, Accessible & Ethical | Minimal & Direct + Conversion | Email Analytics | Brand primary + Clean white + CTA accent | Subscribe form. Archive. About. Social proof. Sample content. Simple conversion. |
| 73 | Digital Products/Downloads | digital, downloads, products | Vibrant & Block-based + Motion-Driven | Glassmorphism, Bento Box Grid | Feature-Rich Showcase + Conversion | E-commerce Analytics | Product category colors + Brand + Success green | Product showcase. Preview. Pricing. Instant delivery. License management. Customer reviews. |
| 74 | Church/Religious Organization | church, organization, religious | Accessible & Ethical + Soft UI Evolution | Minimalism, Trust & Authority | Hero-Centric Design + Social Proof | N/A - Community focused | Warm Gold + Deep Purple/Blue + White | Service times. Events. Sermons. Community. Giving. Location. Welcoming imagery. |
| 75 | Sports Team/Club | club, sports, team | Vibrant & Block-based + Motion-Driven | Dark Mode (OLED), 3D & Hyperrealism | Hero-Centric Design + Feature-Rich | Performance Analytics | Team colors + Energetic accents | Schedule. Roster. News. Tickets. Merchandise. Fan engagement. Action imagery. |
| 76 | Museum/Gallery | gallery, museum | Minimalism + Motion-Driven | Swiss Modernism 2.0, 3D & Hyperrealism | Storytelling-Driven + Feature-Rich | Visitor Analytics | Art-appropriate neutrals + Exhibition accents | Exhibitions. Collections. Tickets. Events. Virtual tours. Educational content. Art-focused design. |
| 77 | Theater/Cinema | cinema, theater | Dark Mode (OLED) + Motion-Driven | Vibrant & Block-based, Glassmorphism | Hero-Centric Design + Conversion | Booking Analytics | Dark + Spotlight accents + Gold | Showtimes. Seat selection. Trailers. Coming soon. Membership. Dramatic imagery. |
| 78 | Language Learning App | app, language, learning | Claymorphism + Vibrant & Block-based | Micro-interactions, Flat Design | Feature-Rich Showcase + Social Proof | Learning Analytics | Playful colors + Progress indicators + Country flags | Lesson structure. Progress tracking. Gamification. Speaking practice. Community. Achievement badges. |
| 79 | Coding Bootcamp | bootcamp, coding | Dark Mode (OLED) + Minimalism | Cyberpunk UI, Flat Design | Feature-Rich Showcase + Social Proof | Student Analytics | Code editor colors + Brand + Success green | Curriculum. Projects. Career outcomes. Alumni. Pricing. Application. Terminal aesthetic. |
| 80 | Cybersecurity Platform | cyber, security, platform | Cyberpunk UI + Dark Mode (OLED) | Neubrutalism, Minimal & Direct | Trust & Authority + Real-Time | Real-Time Monitoring + Heat Map | Matrix Green + Deep Black + Terminal feel | Data density. Threat visualization. Dark mode default. |
| 81 | Developer Tool / IDE | dev, developer, tool, ide | Dark Mode (OLED) + Minimalism | Flat Design, Bento Box Grid | Minimal & Direct + Documentation | Real-Time Monitor + Terminal | Dark syntax theme colors + Blue focus | Keyboard shortcuts. Syntax highlighting. Fast performance. |
| 82 | Biotech / Life Sciences | biotech, biology, science | Glassmorphism + Clean Science | Minimalism, Organic Biophilic | Storytelling-Driven + Research | Data-Dense + Predictive | Sterile White + DNA Blue + Life Green | Data accuracy. Cleanliness. Complex data viz. |
| 83 | Space Tech / Aerospace | aerospace, space, tech | Holographic / HUD + Dark Mode | Glassmorphism, 3D & Hyperrealism | Immersive Experience + Hero | Real-Time Monitoring + 3D | Deep Space Black + Star White + Metallic | High-tech feel. Precision. Telemetry data. |
| 84 | Architecture / Interior | architecture, design, interior | Exaggerated Minimalism + High Imagery | Swiss Modernism 2.0, Parallax | Portfolio Grid + Visuals | Project Management + Gallery | Monochrome + Gold Accent + High Imagery | High-res images. Typography. Space. |
| 85 | Quantum Computing Interface | quantum, computing, physics, qubit, future, science | Holographic / HUD + Dark Mode | Glassmorphism, Spatial UI | Immersive/Interactive Experience | 3D Spatial Data + Real-Time Monitor | Quantum Blue #00FFFF + Deep Black + Interference patterns | Visualize complexity. Qubit states. Probability clouds. High-tech trust. |
| 86 | Biohacking / Longevity App | biohacking, health, longevity, tracking, wellness, science | Biomimetic / Organic 2.0 | Minimalism, Dark Mode (OLED) | Data-Dense + Storytelling | Real-Time Monitor + Biological Data | Cellular Pink/Red + DNA Blue + Clean White | Personal data privacy. Scientific credibility. Biological visualizations. |
| 87 | Autonomous Drone Fleet Manager | drone, autonomous, fleet, aerial, logistics, robotics | HUD / Sci-Fi FUI | Real-Time Monitor, Spatial UI | Real-Time Monitor | Geographic + Real-Time | Tactical Green #00FF00 + Alert Red + Map Dark | Real-time telemetry. 3D spatial awareness. Latency indicators. Safety alerts. |
| 88 | Generative Art Platform | art, generative, ai, creative, platform, gallery | Minimalism (Frame) + Gen Z Chaos | Masonry Grid, Dark Mode | Bento Grid Showcase | Gallery / Portfolio | Neutral #F5F5F5 (Canvas) + User Content | Content is king. Fast loading. Creator attribution. Minting flow. |
| 89 | Spatial Computing OS / App | spatial, vr, ar, vision, os, immersive, mixed-reality | Spatial UI (VisionOS) | Glassmorphism, 3D & Hyperrealism | Immersive/Interactive Experience | Spatial Dashboard | Frosted Glass + System Colors + Depth | Gaze/Pinch interaction. Depth hierarchy. Environment awareness. |
| 90 | Sustainable Energy / Climate Tech | climate, energy, sustainable, green, tech, carbon | Organic Biophilic + E-Ink / Paper | Data-Dense, Swiss Modernism | Interactive Demo + Data | Energy/Utilities Dashboard | Earth Green + Sky Blue + Solar Yellow | Data transparency. Impact visualization. Low-carbon web design. |
| 91 | Personal Finance Tracker | budget, expense, money, finance, spending, savings, tracker, personal, wallet | Glassmorphism + Dark Mode (OLED) | Minimalism, Flat Design | Interactive Product Demo | Financial Dashboard | Calm blue + success green + alert red + chart accents | Category pie/donut charts. Monthly trend lines. Budget progress bars. Transaction list with swipe actions. Receipt camera. Currency formatting. Recurring entries. |
| 92 | Chat & Messaging App | chat, message, messenger, im, realtime, conversation, inbox, dm, whatsapp, telegram | Minimalism + Micro-interactions | Glassmorphism, Flat Design | Feature-Rich Showcase + Demo | User Behavior Analytics | Brand primary + bubble contrast (sender/receiver) + typing grey | Bubble UI (left/right alignment). Typing indicators. Read receipts (✓✓). Image/file preview. Emoji reactions. Group avatars. Online status dots. Swipe-to-reply. |
| 93 | Notes & Writing App | notes, memo, writing, editor, notebook, markdown, journal, notion, obsidian | Minimalism + Flat Design | Swiss Modernism 2.0, Soft UI Evolution | Minimal & Direct | N/A - Editor focused | Clean white/cream + minimal accent + editor syntax colors | WYSIWYG or Markdown toggle. Folder/tag organization. Full-text search. Cloud sync. Typography-first. Distraction-free zen mode. Slash-command palette. |
| 94 | Habit Tracker | habit, streak, routine, daily, tracker, goals, consistency, discipline | Claymorphism + Vibrant & Block-based | Micro-interactions, Flat Design | Social Proof-Focused + Demo | User Behavior Analytics | Streak warm (amber/orange) + progress green + motivational accents | Streak calendar heatmap. Daily check-in interaction. Gamification (badges/levels/fire). Reminder push. Progress ring charts. Weekly/monthly stats. Motivational micro-copy. |
| 95 | Food Delivery / On-Demand | delivery, food, order, uber-eats, doordash, takeout, on-demand, courier | Vibrant & Block-based + Motion-Driven | Glassmorphism, Flat Design | Hero-Centric Design + Feature-Rich | Real-Time Monitoring + Map | Appetizing warm (orange/red) + trust blue + map accent | Restaurant cards with ratings. Menu category horizontal scroll. Cart bottom sheet. Real-time map tracking + driver ETA. Order status stepper. Rating post-delivery. |
| 96 | Ride Hailing / Transportation | ride, taxi, uber, lyft, transport, carpool, driver, trip, fare | Minimalism + Glassmorphism | Dark Mode (OLED), Motion-Driven | Conversion-Optimized + Demo | Real-Time Monitoring + Map | Brand primary + map neutral + status indicator colors | Map-centric full-screen UI. Pickup/dropoff pins + route polyline. Driver card (photo/rating/vehicle). Fare estimate. Trip timer. Safety SOS button. Payment sheet. |
| 97 | Recipe & Cooking App | recipe, cooking, food, kitchen, cookbook, meal, ingredient, chef | Claymorphism + Vibrant & Block-based | Soft UI Evolution, Organic Biophilic | Hero-Centric Design + Feature-Rich | N/A - Content focused | Warm food tones (terracotta/sage/cream) + appetizing imagery | Step-by-step with checkable instructions. Ingredient list with serving adjuster. Built-in timer per step. Cooking mode (screen-awake + large text). Save/bookmark. Share. |
| 98 | Meditation & Mindfulness | meditation, mindfulness, calm, breathe, wellness, relaxation, sleep, headspace | Neumorphism + Soft UI Evolution | Aurora UI, Glassmorphism | Storytelling-Driven + Social Proof | User Behavior Analytics | Ultra-calm pastels (lavender/sage/sky) + breathing animation gradient | Breathing circle animation. Session duration picker. Ambient sound mixer. Streak/consistency tracking. Guided audio player. Sleep timer. Minimal chrome. Slow easing transitions only. |
| 99 | Weather App | weather, forecast, temperature, climate, rain, sun, location, humidity | Glassmorphism + Aurora UI | Motion-Driven, Minimalism | Hero-Centric Design | N/A - Utility focused | Atmospheric gradients (sky blue → sunset → storm grey) + temp scale | Location auto-detect. Hourly horizontal scroll + daily/weekly list. Animated weather icons. Air quality index. UV/wind/humidity chips. Radar map overlay. Widget-friendly layout. |
| 100 | Diary & Journal App | diary, journal, personal, daily, reflection, mood, gratitude, writing | Soft UI Evolution + Minimalism | Neumorphism, Sketch Hand-Drawn | Storytelling-Driven | N/A - Personal focused | Warm paper tones (cream/linen) + muted ink + mood-coded accents | Calendar month-view entry. Mood tag selector (emoji/color). Photo/voice attachment. Writing prompts. Privacy lock (FaceID/PIN). Search across entries. Export to PDF. |
| 101 | CRM & Client Management | crm, client, customer, sales, pipeline, contact, lead, deal, hubspot | Flat Design + Minimalism | Soft UI Evolution, Micro-interactions | Feature-Rich Showcase + Demo | Sales Intelligence Dashboard | Professional blue + pipeline stage colors + closed-won green | Contact card list with avatar. Pipeline kanban board. Activity timeline. Quick-log (call/email/meeting). Deal amount + probability. Tag/segment filter. Mobile quick-actions. |
| 102 | Inventory & Stock Management | inventory, stock, warehouse, product, barcode, supply, sku, management | Flat Design + Minimalism | Dark Mode (OLED), Accessible & Ethical | Feature-Rich Showcase | Real-Time Monitoring + Data-Dense | Functional neutral + status traffic-light (green/amber/red) + scanner accent | Product list/grid with thumbnails. Barcode/QR scanner. Stock level badges. Low-stock alert banner. Category/location filter. Batch edit. Reorder trigger. Audit log. |
| 103 | Flashcard & Study Tool | flashcard, quiz, study, spaced-repetition, anki, learn, memory, exam | Claymorphism + Micro-interactions | Vibrant & Block-based, Flat Design | Feature-Rich Showcase + Demo | Learning Analytics | Playful primary + correct green + incorrect red + progress blue | 3D card flip animation. Spaced repetition algorithm. Deck browser. Session progress bar. Streak tracking. Timed quiz mode. Share/import decks. Rich text + image cards. |
| 104 | Booking & Appointment App | booking, appointment, schedule, calendar, reservation, slot, service | Soft UI Evolution + Flat Design | Minimalism, Micro-interactions | Conversion-Optimized | Drill-Down Analytics | Trust blue + available green + booked grey + confirm accent | Calendar strip or month picker. Available time-slot grid. Service + staff selector. Confirmation summary. Reminder push. Reschedule/cancel flow. Two-sided (provider ↔ client). |
| 105 | Invoice & Billing Tool | invoice, billing, payment, receipt, freelance, estimate, quote, accounting | Minimalism + Flat Design | Swiss Modernism 2.0, Accessible & Ethical | Conversion-Optimized + Trust | Financial Dashboard | Professional navy + paid green + overdue red + neutral grey | Invoice template with line items. Tax/discount calculation. Status badges (Draft/Sent/Paid/Overdue). PDF export + share. Payment link generation. Client address book. Recurring invoices. |
| 106 | Grocery & Shopping List | grocery, shopping, list, supermarket, checklist, pantry, meal-plan, buy | Flat Design + Vibrant & Block-based | Claymorphism, Micro-interactions | Minimal & Direct + Demo | N/A - List focused | Fresh green + food-category colors + checkmark accent | Category-grouped list. Tap-to-check interaction (with strikethrough). Quantity stepper. Share list with family. Store aisle sorting. Barcode scan to add. Frequently bought suggestions. |
| 107 | Timer & Pomodoro | timer, pomodoro, countdown, stopwatch, focus, clock, productivity, interval | Minimalism + Neumorphism | Dark Mode (OLED), Micro-interactions | Minimal & Direct | N/A - Utility focused | High-contrast on dark + focus red/amber + break green | Large centered countdown digits. Circular progress ring. Session/break auto-switch. Session history log. Custom interval settings. Sound + haptic alerts. Focus stats chart. |
| 108 | Parenting & Baby Tracker | baby, parenting, child, feeding, sleep, diaper, milestone, family, newborn | Claymorphism + Soft UI Evolution | Vibrant & Block-based, Accessible & Ethical | Social Proof-Focused + Trust | User Behavior Analytics | Soft pastels (baby pink/sky blue/mint/peach) + warm accents | Feed/sleep/diaper quick-log buttons. Growth percentile chart. Milestone timeline with photos. Multiple child profiles. Partner invite + shared access. Pediatric reference. One-handed operation. |
| 109 | Scanner & Document Manager | scanner, document, ocr, pdf, scan, camera, file, archive, digitize | Minimalism + Flat Design | Dark Mode (OLED), Accessible & Ethical | Feature-Rich Showcase + Demo | N/A - Tool focused | Clean white + camera viewfinder accent + file-type color coding | Camera capture with auto-edge detection. Crop/rotate/enhance. OCR text extraction overlay. PDF multi-page creation. Folder tree organization. Cloud sync. Share/export. Batch scan mode. |
| 110 | Calendar & Scheduling App | calendar, scheduling, planner, agenda, events, reminder, appointment, organize, date, sync | Flat Design + Micro-interactions | Minimalism, Soft UI Evolution | Feature-Rich Showcase + Demo | N/A - Calendar focused | Clean blue + event category accent colors + success green | Event color coding. Week/month/day views. Recurring events. Conflict detection. Multi-calendar sync. |
| 111 | Password Manager | password, security, vault, credentials, login, secure, encrypt, keychain, 2fa, biometric | Minimalism + Accessible & Ethical | Dark Mode (OLED), Trust & Authority | Trust & Authority + Feature-Rich | N/A - Vault focused | Trust blue + security green + dark neutral | Security-first. Zero-knowledge architecture. Biometric unlock. Breach alert dashboard. Password generator. |
| 112 | Expense Splitter / Bill Split | split, expense, bill, aa, share, friends, group, settle, debt, payment, owe | Flat Design + Vibrant & Block-based | Minimalism, Micro-interactions | Minimal & Direct + Demo | N/A - Balance focused | Success green + alert red + neutral grey + avatar accent colors | Group expense tracking. Debt simplification algorithm. Payment reminders. Multi-currency. Receipt photo import. |
| 113 | Voice Recorder & Memo | voice, recorder, memo, audio, transcription, dictate, recording, microphone, note, otter | Minimalism + AI-Native UI | Flat Design, Dark Mode (OLED) | Interactive Product Demo + Minimal | N/A - Recording focused | Clean white + recording red + waveform accent | Waveform display. Background recording. Auto-transcription (AI). Tag/organize. Cloud sync. |
| 114 | Bookmark & Read-Later | bookmark, read-later, save, article, pocket, link, reading, archive, collection, raindrop | Minimalism + Flat Design | Editorial Grid, Swiss Modernism 2.0 | Minimal & Direct + Demo | N/A - List focused | Paper warm white + ink neutral + minimal accent + tag colors | Fast save via share sheet. Article distraction-free view. Tags and collections. Offline sync. Reading progress. |
| 115 | Translator App | translate, language, text, voice, ocr, dictionary, multilingual, real-time, detect, deepl | Flat Design + AI-Native UI | Minimalism, Micro-interactions | Feature-Rich Showcase + Interactive Demo | N/A - Utility focused | Global blue + neutral grey + language flag accent | Real-time camera translation (OCR). Voice input and output. Offline mode. Conversation mode. Phrasebook. |
| 116 | Calculator & Unit Converter | calculator, converter, unit, math, currency, measurement, scientific, formula, percentage | Neumorphism + Minimalism | Flat Design, Dark Mode (OLED) | Minimal & Direct | N/A - Utility focused | Dark functional + orange operation keys + clear button hierarchy | Scientific mode toggle. Live currency rates. Calculation history. Widget support. Gesture input. |
| 117 | Alarm & World Clock | alarm, clock, world, timezone, timer, wake, sleep, schedule, reminder, bedtime | Dark Mode (OLED) + Minimalism | Neumorphism, Flat Design | Minimal & Direct | N/A - Utility focused | Deep dark + ambient glow accent + timezone gradient | Gentle wake (gradual volume). Timezone visualizer. Sleep tracking integration. Smart alarm skip. Bedtime mode. |
| 118 | File Manager & Transfer | file, manager, transfer, folder, document, storage, cloud, share, organize, compress | Flat Design + Minimalism | Accessible & Ethical, Dark Mode (OLED) | Feature-Rich Showcase + Demo | N/A - File tree focused | Functional neutral + file type color coding (PDF orange, doc blue, image purple) | Folder tree navigation. File type preview. Wireless P2P transfer. Cloud integration. Compress and extract. |
| 119 | Email Client | email, mail, inbox, compose, thread, newsletter, filter, reply, gmail, spark, superhuman | Flat Design + Minimalism | Micro-interactions, Soft UI Evolution | Feature-Rich Showcase + Demo | N/A - Inbox focused | Clean white + brand primary + priority red + snooze amber | Unified inbox. Swipe actions (archive/delete/snooze). Priority sorting. Smart reply. Unsubscribe tool. |
| 120 | Casual Puzzle Game | puzzle, casual, match, brain, game, relaxing, level, tiles, logic, block, three | Claymorphism + Vibrant & Block-based | Micro-interactions, Motion-Driven | Feature-Rich Showcase + Social Proof | N/A - Game focused | Cheerful pastels + progression gradient + reward gold + bright accent | Satisfying match/clear animations. Progressive difficulty. Daily challenges. No-skip tutorials. Offline play. |
| 121 | Trivia & Quiz Game | trivia, quiz, knowledge, question, answer, challenge, leaderboard, fact, brain, compete | Vibrant & Block-based + Micro-interactions | Claymorphism, Flat Design | Feature-Rich Showcase + Social Proof | Leaderboard Analytics | Energetic blue + correct green + incorrect red + leaderboard gold | Timer pressure UX. Category selection. Streak system. Real-time multiplayer. Daily quiz mode. |
| 122 | Card & Board Game | card, board, chess, checkers, poker, strategy, turn-based, multiplayer, classic, tabletop | 3D & Hyperrealism + Flat Design | Motion-Driven, Dark Mode (OLED) | Feature-Rich Showcase | N/A - Game focused | Game-theme felt green + dark wood + card back patterns | Real-time or async multiplayer. Game state sync. Tutorial mode. Match history. ELO rating system. |
| 123 | Idle & Clicker Game | idle, clicker, incremental, passive, cookie, adventure, progress, offline, collect, prestige | Vibrant & Block-based + Motion-Driven | Claymorphism, 3D & Hyperrealism | Feature-Rich Showcase | N/A - Progress focused | Coin gold + upgrade blue + prestige purple + progress green | Offline progress calculation. Satisfying number animations. Upgrade tree clarity. Prestige system. Optional ads. |
| 124 | Word & Crossword Game | word, crossword, wordle, spelling, vocabulary, letters, grid, puzzle, dictionary, daily | Minimalism + Flat Design | Swiss Modernism 2.0, Micro-interactions | Minimal & Direct + Demo | N/A - Game focused | Clean white + warm letter tiles + success green + shake red | Daily challenge with shareable results. Physical keyboard feel. Difficulty levels. Dictionary hints. Streak stats. |
| 125 | Arcade & Retro Game | arcade, retro, 8bit, action, shoot, runner, tap, reflex, endless, pixel, classic, score | Pixel Art + Retro-Futurism | Vibrant & Block-based, Motion-Driven | Feature-Rich Showcase + Hero-Centric | N/A - Score focused | Neon on black + pixel palette + score gold + danger red | Instant play with no login. Game Center leaderboards. Haptic feedback on collision. Offline. Controller support. |
| 126 | Photo Editor & Filters | photo, edit, filter, vsco, snapseed, enhance, crop, retouch, adjust, luts, preset, adjust | Minimalism + Dark Mode (OLED) | Motion-Driven, Flat Design | Feature-Rich Showcase + Interactive Demo | N/A - Editor focused | Dark editor background + vibrant filter preview strip + tool icon accent | Non-destructive editing. Filter preview carousel. Histogram. RAW support. Batch export. Social share direct. |
| 127 | Short Video Editor | video, edit, capcut, inshot, clip, reel, tiktok, trim, effects, transitions, music, timeline | Dark Mode (OLED) + Motion-Driven | Vibrant & Block-based, Glassmorphism | Feature-Rich Showcase + Hero-Centric | N/A - Timeline editor focused | Dark background + timeline track accent colors + effect preview vivid | Multi-track timeline. Licensed music library. Text overlays. Auto-captions. Export 9:16 / 16:9 / 1:1. |
| 128 | Drawing & Sketching Canvas | drawing, sketch, procreate, canvas, paint, illustration, digital, brush, layers, art, stylus | Minimalism + Dark Mode (OLED) | Anti-Polish Raw, Motion-Driven | Interactive Product Demo + Storytelling | N/A - Canvas focused | Neutral canvas + full-spectrum color picker + tool panel dark | Pressure sensitivity. Infinite canvas (pan/zoom). Layer management. Undo history. Export PNG/PSD/SVG. |
| 129 | Music Creation & Beat Maker | music, beat, daw, garageband, create, loop, sample, instrument, track, compose, record, midi | Dark Mode (OLED) + Motion-Driven | Cyberpunk UI, Glassmorphism | Interactive Product Demo + Storytelling | N/A - DAW focused | Dark studio background + track colors rainbow + waveform accent + BPM pulse | Touch piano and drum pad. Loop browser. MIDI support. Export MP3/WAV. Low-latency audio engine. |
| 130 | Meme & Sticker Maker | meme, sticker, maker, funny, caption, template, edit, share, viral, emoji, creator, reaction | Vibrant & Block-based + Flat Design | Gen Z Chaos, Claymorphism | Feature-Rich Showcase + Social Proof | N/A - Creator focused | Bold primary + comedic yellow + viral red + high saturation accent | Template library. Caption text overlay. Font variety. Reaction sticker packs. Share to all platforms. Fast creation. |
| 131 | AI Photo & Avatar Generator | ai, photo, avatar, lensa, portrait, generate, selfie, style, filter, prisma, art | AI-Native UI + Aurora UI | Glassmorphism, Minimalism | Feature-Rich Showcase + Social Proof | N/A - Generation focused | AI purple + aurora gradients + before/after neutral | Style selection. Multiple output variations. Privacy policy prominent. Fast generation. Credits/subscription system. |
| 132 | Link-in-Bio Page Builder | bio, link, linktree, personal, page, creator, social, portfolio, profile, landing, custom | Vibrant & Block-based + Bento Box Grid | Minimalism, Glassmorphism | Conversion-Optimized + Social Proof | Analytics (click tracking) | Brand-customizable + accent link color + clean white canvas | Drag-drop builder. Theme templates. Click analytics. Custom domain. Social icon integration. QR code export. |
| 133 | Wardrobe & Outfit Planner | wardrobe, outfit, fashion, clothes, closet, style, wear, plan, capsule, ootd, lookbook | Minimalism + Motion-Driven | Aurora UI, Soft UI Evolution | Storytelling-Driven + Feature-Rich | N/A - Wardrobe focused | Clean fashion neutral + full clothes color palette + accent | Photo catalog of clothes. AI outfit suggestions. Calendar integration. Capsule wardrobe. Season filtering. |
| 134 | Plant Care Tracker | plant, care, water, garden, tracker, reminder, species, photo, grow, health, planta | Organic Biophilic + Soft UI Evolution | Claymorphism, Flat Design | Storytelling-Driven + Social Proof | N/A - Plant collection focused | Nature greens + earth brown + sunny yellow reminder + water blue | Plant database with care guides. Watering reminders. Growth photo timeline. AI health diagnosis. Collection sharing. |
| 135 | Book & Reading Tracker | book, reading, tracker, goodreads, library, shelf, progress, review, notes, goal, literature | Swiss Modernism 2.0 + Minimalism | E-Ink Paper, Soft UI Evolution | Social Proof-Focused + Feature-Rich | N/A - Library focused | Warm paper white + ink brown + reading progress green + book cover colors | Barcode scan to add. Progress percentage. Annual reading goal. Notes and quotes. Friends activity. Genre stats. |
| 136 | Couple & Relationship App | couple, relationship, partner, love, date, anniversary, memory, shared, intimate, between | Aurora UI + Soft UI Evolution | Claymorphism, Glassmorphism | Storytelling-Driven + Social Proof | N/A - Couple focused | Warm romantic pink/rose + soft gradient + memory photo tones | Shared timeline. Anniversary countdowns. Secret chat. Photo albums. Love language quiz. Date night ideas. |
| 137 | Family Calendar & Chores | family, calendar, chores, tasks, household, shared, kids, schedule, cozi, organize, member | Flat Design + Claymorphism | Accessible & Ethical, Vibrant & Block-based | Feature-Rich Showcase + Social Proof | N/A - Family hub focused | Warm playful + member color coding + chore completion green | Member color coding. Chore assignment rotation. Recurring events. Shared shopping list. Allowance tracking. |
| 138 | Mood Tracker | mood, emotion, feeling, mental, daily, journal, wellbeing, check-in, log, track, daylio | Soft UI Evolution + Minimalism | Aurora UI, Neumorphism | Storytelling-Driven + Social Proof | N/A - Mood chart focused | Emotion gradient (blue sad to yellow happy) + pastel per mood + insight accent | One-tap daily check-in. Emotion wheel selector. Mood calendar heatmap. Pattern insights. Export and share. |
| 139 | Gift & Wishlist | gift, wishlist, present, birthday, occasion, registry, idea, shop, list, share, surprise | Vibrant & Block-based + Soft UI Evolution | Claymorphism, Flat Design | Minimal & Direct + Conversion | N/A - List focused | Celebration warm pink/gold/red + category colors + surprise accent | Add from any URL. Price range filter. Reserved-by-others system. Occasion calendar. Collaborative list. Surprise mode. |
| 140 | Running & Cycling GPS | running, cycling, gps, strava, track, route, speed, distance, cadence, pace, workout, sport | Dark Mode (OLED) + Vibrant & Block-based | Motion-Driven, Glassmorphism | Feature-Rich Showcase + Social Proof | Performance Analytics | Energetic orange + map accent + pace zones (green/yellow/red) | Live GPS tracking. Route map. Auto-pause detection. Segment leaderboards. Training zones. Social feed. Garmin sync. |
| 141 | Yoga & Stretching Guide | yoga, stretch, flexibility, pose, asana, guided, session, calm, routine, wellness, down-dog | Organic Biophilic + Soft UI Evolution | Neumorphism, Minimalism | Storytelling-Driven + Social Proof | N/A - Session focused | Earth calming sage/terracotta/cream + breathing gradient + warm accent | Pose library with illustrations. Guided sessions with audio. Breathing exercises. Progress calendar. Beginner to advanced. |
| 142 | Sleep Tracker | sleep, tracker, alarm, cycle, quality, snore, analysis, rem, deep, smart, wake, insomnia | Dark Mode (OLED) + Neumorphism | Glassmorphism, Minimalism | Feature-Rich Showcase + Social Proof | Healthcare Analytics | Deep midnight blue + stars/moon accent + sleep quality gradient (poor red to great green) | Sleep cycle detection. Smart alarm wakes at light sleep. Snore detection. Weekly trends. Apple Health integration. |
| 143 | Calorie & Nutrition Counter | calorie, nutrition, food, diet, macro, protein, carb, fat, log, fitness, myfitnesspal | Flat Design + Vibrant & Block-based | Minimalism, Claymorphism | Feature-Rich Showcase + Social Proof | Healthcare Analytics | Healthy green + macro colors (protein blue, carb orange, fat yellow) + progress circle | Barcode scanner food log. Large database. Macro goals. Restaurant lookup. Recipe builder. AI photo food logging. |
| 144 | Period & Cycle Tracker | period, cycle, menstrual, fertility, ovulation, pms, log, women, health, flo, clue, hormone | Soft UI Evolution + Aurora UI | Accessible & Ethical, Claymorphism | Social Proof-Focused + Trust | Healthcare Analytics | Rose/blush + lavender + fertility green + soft calendar tones | Cycle prediction. Symptom logging. Fertility window. Personalized insights. Privacy-first. Partner sharing option. |
| 145 | Medication & Pill Reminder | medication, pill, reminder, dose, schedule, prescription, drug, health, medisafe, refill | Accessible & Ethical + Flat Design | Minimalism, Trust & Authority | Trust & Authority + Feature-Rich | N/A - Schedule focused | Medical trust blue + missed alert red + taken green + clean white | Multi-medication schedule. Caregiver sharing. Refill reminders. Drug interaction warnings. Large touch targets. |
| 146 | Water & Hydration Reminder | water, hydration, drink, reminder, daily, tracker, glasses, intake, health, cup, aqua | Claymorphism + Vibrant & Block-based | Flat Design, Micro-interactions | Minimal & Direct + Demo | N/A - Daily goal focused | Refreshing blue + water wave animation + goal progress accent | Tap to log quickly. Animated fill visualization. Custom reminders. Goal by weight/weather. Streak system. Widget. |
| 147 | Fasting & Intermittent Timer | fasting, intermittent, 16:8, timer, fast, eating, window, keto, diet, zero, weight, protocol | Minimalism + Dark Mode (OLED) | Neumorphism, Flat Design | Feature-Rich Showcase + Social Proof | N/A - Timer focused | Fasting deep blue/purple + eating window green + timeline neutral | Protocol selector (16:8, 18:6, OMAD). Circular countdown timer. Fasting history log. Tips during fast. Electrolytes. |
| 148 | Anonymous Community / Confession | anonymous, community, confess, whisper, secret, vent, share, safe, private, social, yikyak | Dark Mode (OLED) + Minimalism | Glassmorphism, Soft UI Evolution | Social Proof-Focused + Feature-Rich | User Behavior Analytics | Dark protective + subtle gradient + upvote green + empathy warm accent | Anonymous posting with moderation. Safety reporting. Reaction system. Trending topics. Mental health resources link. |
| 149 | Local Events & Discovery | local, events, discovery, meetup, nearby, social, city, activities, calendar, community, explore | Vibrant & Block-based + Motion-Driven | Glassmorphism, Flat Design | Hero-Centric Design + Feature-Rich | Event Analytics | City vibrant + event category colors + map accent + date highlight | Location-based discovery. Category filters. RSVP flow. Map view. Friend attendance. Organizer tools. Reminders. |
| 150 | Study Together / Virtual Coworking | study, focus, cowork, pomodoro, virtual, together, session, accountability, live, stream, room | Minimalism + Soft UI Evolution | Flat Design, Dark Mode (OLED) | Social Proof-Focused + Feature-Rich | User Behavior Analytics | Calm focus blue + session progress indicator + ambient warm neutrals | Live study rooms with video/avatar presence. Shared focus timer. Ambient music. Goals sharing. Streak accountability. |
| 151 | Coding Challenge & Practice | coding, leetcode, challenge, algorithm, practice, programming, competitive, skill, interview, problem | Dark Mode (OLED) + Cyberpunk UI | Minimalism, Flat Design | Feature-Rich Showcase + Social Proof | Student Analytics | Code editor dark + success green + difficulty gradient (easy green / medium amber / hard red) | Code editor with syntax highlight. Multiple languages. Hint system. Solution explanation. Company tags. Contest mode. |
| 152 | Kids Learning (ABC & Math) | kids, children, learning, abc, math, phonics, numbers, education, games, preschool, early | Claymorphism + Vibrant & Block-based | Micro-interactions, Flat Design | Social Proof-Focused + Trust | Parent Dashboard | Bright primary + child-safe pastels + reward gold + interactive accent | Age-appropriate UI for 2-8. No ads. No dark patterns. Curriculum aligned. Parent progress reports. Reward system. |
| 153 | Music Instrument Learning | music, instrument, piano, guitar, learn, lesson, tutorial, notes, play, chord, practice, simply | Vibrant & Block-based + Motion-Driven | Dark Mode (OLED), Soft UI Evolution | Interactive Product Demo + Social Proof | Learning Analytics | Musical warm deep red/brown + note color system + skill progress bar | Interactive instrument on-screen. Sheet music display. Song library. Slow-tempo practice. Recording and playback. Teacher mode. |
| 154 | Parking Finder | parking, spot, finder, map, pay, meter, garage, location, car, reserve, spothero | Minimalism + Glassmorphism | Flat Design, Micro-interactions | Conversion-Optimized + Feature-Rich | Real-Time Monitoring + Map | Trust blue + available green + occupied red + map neutral | Real-time availability. In-app navigation. Payment integration. Parking timer alert. Favorite spots. Street vs garage. |
| 155 | Public Transit Guide | transit, bus, metro, subway, train, route, schedule, map, city, commute, trip, citymapper | Flat Design + Accessible & Ethical | Minimalism, Motion-Driven | Feature-Rich Showcase + Interactive Demo | Real-Time Monitoring + Map | Transit brand line colors + real-time indicator green/red + map neutral | Real-time arrivals. Offline maps. Disruption alerts. Multi-modal routing. Fare calculation. Accessibility features. |
| 156 | Road Trip Planner | road, trip, drive, route, planner, travel, stop, map, adventure, scenic, car, wanderlog | Aurora UI + Organic Biophilic | Motion-Driven, Vibrant & Block-based | Storytelling-Driven + Hero-Centric | N/A - Trip focused | Adventure warm sunset orange + map teal + stop markers + road neutral | Route planning with stops. Point-of-interest discovery. Gas/food/hotel along route. Offline maps. Trip sharing. |
| 157 | VPN & Privacy Tool | vpn, privacy, secure, anonymous, encrypt, proxy, ip, protect, shield, network, nordvpn | Minimalism + Dark Mode (OLED) | Cyberpunk UI, Trust & Authority | Trust & Authority + Conversion-Optimized | N/A - Connection focused | Dark shield blue + connected green + disconnected red + trust accent | One-tap connect. Server selection by country. No-log policy prominent. Speed indicator. Kill switch. Protocol choice. |
| 158 | Emergency SOS & Safety | emergency, sos, safety, alert, location, help, danger, crisis, first-aid, guard, bsafe | Accessible & Ethical + Flat Design | Dark Mode (OLED), Minimalism | Trust & Authority + Social Proof | N/A - Safety focused | Alert red + safety blue + location green + high contrast critical | One-tap SOS. Emergency contacts auto-notify. Live location sharing. Fake call feature. Safe walk mode. Local emergency numbers. |
| 159 | Wallpaper & Theme App | wallpaper, theme, background, customize, aesthetic, home-screen, lock-screen, widget, design, zedge | Vibrant & Block-based + Aurora UI | Glassmorphism, Motion-Driven | Feature-Rich Showcase + Social Proof | N/A - Gallery focused | Content-driven + trending aesthetic palettes + download accent | Category browsing. Preview on device. Daily wallpaper auto-set. Widget matching. Creator uploads. Resolution auto-fit. |
| 160 | White Noise & Ambient Sound | white noise, ambient, sound, sleep, focus, rain, nature, relax, concentration, background, noisli | Minimalism + Dark Mode (OLED) | Neumorphism, Organic Biophilic | Minimal & Direct + Social Proof | N/A - Player focused | Calming dark + ambient texture visual + subtle sound wave + sleep blue | Sound mixer with multiple simultaneous layers. Sleep timer with fade. Custom soundscapes. Offline. Background audio. |
| 161 | Home Decoration & Interior Design | home, interior, decor, design, furniture, room, renovation, ar, plan, inspire, 3d, houzz | Minimalism + 3D Product Preview | Organic Biophilic, Aurora UI | Storytelling-Driven + Feature-Rich | N/A - Project focused | Neutral interior palette + material texture accent + AR blue | AR room visualization. Style quiz. Product catalog with purchase links. 3D room planner. Mood board. Before/after. |

## 2. Landing-page patterns

| No | Pattern Name | Keywords | Section Order | Primary CTA Placement | Color Strategy | Recommended Effects | Conversion Optimization |
|---|---|---|---|---|---|---|---|
| 1 | Hero + Features + CTA | hero, hero-centric, hero-centric design, features, feature-rich, feature-rich showcase, cta, call-to-action | 1. Hero with headline/image, 2. Value prop, 3. Key features (3-5), 4. CTA section, 5. Footer | Hero (sticky) + Bottom | Hero: Brand primary or vibrant. Features: Card bg #FAFAFA. CTA: Contrasting accent color | Hero parallax, feature card hover lift, CTA glow on hover | Deep CTA placement. Use contrasting color (at least 7:1 contrast ratio). Sticky navbar CTA. |
| 2 | Hero + Testimonials + CTA | hero, testimonials, social-proof, social-proof-focused, social proof focused, trust, reviews, cta | 1. Hero, 2. Problem statement, 3. Solution overview, 4. Testimonials carousel, 5. CTA | Hero (sticky) + Post-testimonials | Hero: Brand color. Testimonials: Light bg #F5F5F5. Quotes: Italic, muted color #666. CTA: Vibrant | Testimonial carousel slide animations, quote marks animations, avatar fade-in | Social proof before CTA. Use 3-5 testimonials. Include photo + name + role. CTA after social proof. |
| 3 | Product Demo + Features | demo, product-demo, features, showcase, interactive, interactive-product-demo, interactive product demo | 1. Hero, 2. Product video/mockup (center), 3. Feature breakdown per section, 4. Comparison (optional), 5. CTA | Video center + CTA right/bottom | Video surround: Brand color overlay. Features: Icon color #0080FF. Text: Dark #222 | Video play button pulse, feature scroll reveals, demo interaction highlights | Embedded product demo increases engagement. Use interactive mockup if possible. Auto-play video muted. |
| 4 | Minimal Single Column | minimal, simple, direct, minimal & direct, minimal-direct, single-column, clean | 1. Hero headline, 2. Short description, 3. Benefit bullets (3 max), 4. CTA, 5. Footer | Center, large CTA button | Minimalist: Brand + white #FFFFFF + accent. Buttons: High contrast 7:1+. Text: Black/Dark grey | Minimal hover effects. Smooth scroll. CTA scale on hover (subtle) | Single CTA focus. Large typography. Lots of whitespace. No nav clutter. Mobile-first. |
| 5 | Funnel (3-Step Conversion) | funnel, conversion, conversion-optimized, conversion optimized, steps, wizard, onboarding | 1. Hero, 2. Step 1 (problem), 3. Step 2 (solution), 4. Step 3 (action), 5. CTA progression | Each step: mini-CTA. Final: main CTA | Step colors: 1 (Red/Problem), 2 (Orange/Process), 3 (Green/Solution). CTA: Brand color | Step number animations, progress bar fill, step transitions smooth scroll | Progressive disclosure. Show only essential info per step. Use progress indicators. Multiple CTAs. |
| 6 | Comparison Table + CTA | comparison, table, compare, versus, cta | 1. Hero, 2. Problem intro, 3. Comparison table (product vs competitors), 4. Pricing (optional), 5. CTA | Table: Right column. CTA: Below table | Table: Alternating rows (white/light grey). Your product: Highlight #FFFACD (light yellow) or green. Text: Dark | Table row hover highlight, price toggle animations, feature checkmark animations | Use comparison to show unique value. Highlight your product row. Include 'free trial' in pricing row. |
| 7 | Lead Magnet + Form | lead, form, signup, capture, email, magnet | 1. Hero (benefit headline), 2. Lead magnet preview (ebook cover, checklist, etc), 3. Form (minimal fields), 4. CTA submit | Form CTA: Submit button | Lead magnet: Professional design. Form: Clean white bg. Inputs: Light border #CCCCCC. CTA: Brand color | Form focus state animations, input validation animations, success confirmation animation | Form fields ≤ 3 for best conversion. Offer valuable lead magnet preview. Show form submission progress. |
| 8 | Pricing Page + CTA | pricing, plans, tiers, comparison, cta | 1. Hero (pricing headline), 2. Price comparison cards, 3. Feature comparison table, 4. FAQ section, 5. Final CTA | Each card: CTA button. Sticky CTA in nav | Free: Grey, Starter: Blue, Pro: Green/Gold, Enterprise: Dark. Cards: 1px border, shadow | Price toggle animation (monthly/yearly), card comparison highlight, FAQ accordion open/close | Recommend starter plan (pre-select/highlight). Show annual discount (20-30%). Use FAQs to address concerns. |
| 9 | Video-First Hero | video, hero, media, visual, engaging | 1. Hero with video background, 2. Key features overlay, 3. Benefits section, 4. CTA | Overlay on video (center/bottom) + Bottom section | Dark overlay 60% on video. Brand accent for CTA. White text on dark. | Video autoplay muted, parallax scroll, text fade-in on scroll | 86% higher engagement with video. Add captions for accessibility. Compress video for performance. |
| 10 | Scroll-Triggered Storytelling | storytelling, scroll, narrative, story, immersive | 1. Intro hook, 2. Chapter 1 (problem), 3. Chapter 2 (journey), 4. Chapter 3 (solution), 5. Climax CTA | End of each chapter (mini) + Final climax CTA | Progressive reveal. Each chapter has distinct color. Building intensity. | ScrollTrigger animations, parallax layers, progressive disclosure, chapter transitions | Narrative increases time-on-page 3x. Use progress indicator. Mobile: simplify animations. |
| 11 | AI Personalization Landing | ai, personalization, smart, recommendation, dynamic | 1. Dynamic hero (personalized), 2. Relevant features, 3. Tailored testimonials, 4. Smart CTA | Context-aware placement based on user segment | Adaptive based on user data. A/B test color variations per segment. | Dynamic content swap, fade transitions, personalized product recommendations | 20%+ conversion with personalization. Requires analytics integration. Fallback for new users. |
| 12 | Waitlist/Coming Soon | waitlist, coming-soon, launch, early-access, notify | 1. Hero with countdown, 2. Product teaser/preview, 3. Email capture form, 4. Social proof (waitlist count) | Email form prominent (above fold) + Sticky form on scroll | Anticipation: Dark + accent highlights. Countdown in brand color. Urgency indicators. | Countdown timer animation, email validation feedback, success confetti, social share buttons | Scarcity + exclusivity. Show waitlist count. Early access benefits. Referral program. |
| 13 | Comparison Table Focus | comparison, table, versus, compare, features | 1. Hero (problem statement), 2. Comparison matrix (you vs competitors), 3. Feature deep-dive, 4. Winner CTA | After comparison table (highlighted row) + Bottom | Your product column highlighted (accent bg or green). Competitors neutral. Checkmarks green. | Table row hover highlight, feature checkmark animations, sticky comparison header | Show value vs competitors. 35% higher conversion. Be factual. Include pricing if favorable. |
| 14 | Pricing-Focused Landing | pricing, price, cost, plans, subscription | 1. Hero (value proposition), 2. Pricing cards (3 tiers), 3. Feature comparison, 4. FAQ, 5. Final CTA | Each pricing card + Sticky CTA in nav + Bottom | Popular plan highlighted (brand color border/bg). Free: grey. Enterprise: dark/premium. | Price toggle monthly/annual animation, card hover lift, FAQ accordion smooth open | Annual discount 20-30%. Recommend mid-tier (most popular badge). Address objections in FAQ. |
| 15 | App Store Style Landing | app, mobile, download, store, install | 1. Hero with device mockup, 2. Screenshots carousel, 3. Features with icons, 4. Reviews/ratings, 5. Download CTAs | Download buttons prominent (App Store + Play Store) throughout | Dark/light matching app store feel. Star ratings in gold. Screenshots with device frames. | Device mockup rotations, screenshot slider, star rating animations, download button pulse | Show real screenshots. Include ratings (4.5+ stars). QR code for mobile. Platform-specific CTAs. |
| 16 | FAQ/Documentation Landing | faq, documentation, help, support, questions, faq/documentation, knowledge base | 1. Hero with search bar, 2. Popular categories, 3. FAQ accordion, 4. Contact/support CTA | Search bar prominent + Contact CTA for unresolved questions | Clean, high readability. Minimal color. Category icons in brand color. Success green for resolved. | Search autocomplete, smooth accordion open/close, category hover, helpful feedback buttons | Reduce support tickets. Track search analytics. Show related articles. Contact escalation path. |
| 17 | Immersive/Interactive Experience | immersive, interactive, experience, 3d, animation, immersive/interactive experience | 1. Full-screen interactive element, 2. Guided product tour, 3. Key benefits revealed, 4. CTA after completion | After interaction complete + Skip option for impatient users | Immersive experience colors. Dark background for focus. Highlight interactive elements. | WebGL, 3D interactions, gamification elements, progress indicators, reward animations | 40% higher engagement. Performance trade-off. Provide skip option. Mobile fallback essential. |
| 18 | Event/Conference Landing | event, conference, meetup, registration, schedule, hero-centric design, hero-centric | 1. Hero (date/location/countdown), 2. Speakers grid, 3. Agenda/schedule, 4. Sponsors, 5. Register CTA | Register CTA sticky + After speakers + Bottom | Urgency colors (countdown). Event branding. Speaker cards professional. Sponsor logos neutral. | Countdown timer, speaker hover cards with bio, agenda tabs, early bird countdown | Early bird pricing with deadline. Social proof (past attendees). Speaker credibility. Multi-ticket discounts. |
| 19 | Product Review/Ratings Focused | reviews, ratings, testimonials, social-proof, social-proof-focused, stars | 1. Hero (product + aggregate rating), 2. Rating breakdown, 3. Individual reviews, 4. Buy/CTA | After reviews summary + Buy button alongside reviews | Trust colors. Star ratings gold. Verified badge green. Review sentiment colors. | Star fill animations, review filtering, helpful vote interactions, photo lightbox | User-generated content builds trust. Show verified purchases. Filter by rating. Respond to negative reviews. |
| 20 | Community/Forum Landing | community, forum, social, members, discussion | 1. Hero (community value prop), 2. Popular topics/categories, 3. Active members showcase, 4. Join CTA | Join button prominent + After member showcase | Warm, welcoming. Member photos add humanity. Topic badges in brand colors. Activity indicators green. | Member avatars animation, activity feed live updates, topic hover previews, join success celebration | Show active community (member count, posts today). Highlight benefits. Preview content. Easy onboarding. |
| 21 | Before-After Transformation | before-after, transformation, results, comparison | 1. Hero (problem state), 2. Transformation slider/comparison, 3. How it works, 4. Results CTA | After transformation reveal + Bottom | Contrast: muted/grey (before) vs vibrant/colorful (after). Success green for results. | Slider comparison interaction, before/after reveal animations, result counters, testimonial videos | Visual proof of value. 45% higher conversion. Real results. Specific metrics. Guarantee offer. |
| 22 | Marketplace / Directory | marketplace, directory, search, listing | 1. Hero (Search focused), 2. Categories, 3. Featured Listings, 4. Trust/Safety, 5. CTA (Become a host/seller) | Hero Search Bar + Navbar 'List your item' | Search: High contrast. Categories: Visual icons. Trust: Blue/Green. | Search autocomplete animation, map hover pins, card carousel | Search bar is the CTA. Reduce friction to search. Popular searches suggestions. |
| 23 | Newsletter / Content First | newsletter, content, writer, blog, subscribe, minimal & direct, minimal-direct | 1. Hero (Value Prop + Form), 2. Recent Issues/Archives, 3. Social Proof (Subscriber count), 4. About Author | Hero inline form + Sticky header form | Minimalist. Paper-like background. Text focus. Accent color for Subscribe. | Text highlight animations, typewriter effect, subtle fade-in | Single field form (Email only). Show 'Join X, 000 readers'. Read sample link. |
| 24 | Webinar Registration | webinar, registration, event, training, live | 1. Hero (Topic + Timer + Form), 2. What you'll learn, 3. Speaker Bio, 4. Urgency/Bonuses, 5. Form (again) | Hero (Right side form) + Bottom anchor | Urgency: Red/Orange. Professional: Blue/Navy. Form: High contrast white. | Countdown timer, speaker avatar float, urgent ticker | Limited seats logic. 'Live' indicator. Auto-fill timezone. |
| 25 | Enterprise Gateway | enterprise, corporate, gateway, solutions, portal, trust, authority, trust & authority | 1. Hero (Video/Mission), 2. Solutions by Industry, 3. Solutions by Role, 4. Client Logos, 5. Contact Sales | Contact Sales (Primary) + Login (Secondary) | Corporate: Navy/Grey. High integrity. Conservative accents. | Slow video background, logo carousel, tab switching for industries | Path selection (I am a...). Mega menu navigation. Trust signals prominent. |
| 26 | Portfolio Grid | portfolio, grid, showcase, gallery, masonry, portfolio grid + visuals | 1. Hero (Name/Role), 2. Project Grid (Masonry), 3. About/Philosophy, 4. Contact | Project Card Hover + Footer Contact | Neutral background (let work shine). Text: Black/White. Accent: Minimal. | Image lazy load reveal, hover overlay info, lightbox view | Visuals first. Filter by category. Fast loading essential. |
| 27 | Horizontal Scroll Journey | horizontal, scroll, journey, gallery, storytelling, panoramic, storytelling-driven | 1. Intro (Vertical), 2. The Journey (Horizontal Track), 3. Detail Reveal, 4. Vertical Footer | Floating Sticky CTA or End of Horizontal Track | Continuous palette transition. Chapter colors. Progress bar #000000. | Scroll-jacking (careful), parallax layers, horizontal slide, progress indicator | Immersive product discovery. High engagement. Keep navigation visible. |
| 28 | Bento Grid Showcase | bento, grid, features, modular, apple-style, showcase, feature-rich showcase | 1. Hero, 2. Bento Grid (Key Features), 3. Detail Cards, 4. Tech Specs, 5. CTA | Floating Action Button or Bottom of Grid | Card backgrounds: #F5F5F7 or Glass. Icons: Vibrant brand colors. Text: Dark. | Hover card scale (1.02), video inside cards, tilt effect, staggered reveal | Scannable value props. High information density without clutter. Mobile stack. |
| 29 | Interactive 3D Configurator | 3d, configurator, customizer, interactive, product, interactive product demo | 1. Hero (Configurator), 2. Feature Highlight (synced), 3. Price/Specs, 4. Purchase | Inside Configurator UI + Sticky Bottom Bar | Neutral studio background. Product: Realistic materials. UI: Minimal overlay. | Real-time rendering, material swap animation, camera rotate/zoom, light reflection | Increases ownership feeling. 360 view reduces return rates. Direct add-to-cart. |
| 30 | AI-Driven Dynamic Landing | ai, dynamic, personalized, adaptive, generative | 1. Prompt/Input Hero, 2. Generated Result Preview, 3. How it Works, 4. Value Prop | Input Field (Hero) + 'Try it' Buttons | Adaptive to user input. Dark mode for compute feel. Neon accents. | Typing text effects, shimmering generation loaders, morphing layouts | Immediate value demonstration. 'Show, don't tell'. Low friction start. |
| 31 | Feature-Rich Showcase | feature-rich, feature-rich showcase, features, showcase, product showcase | 1. Hero (value prop), 2. Feature grid/cards (4-6), 3. Use cases or benefits, 4. Social proof or logos, 5. CTA | Hero (sticky) + After features + Bottom | Brand primary + card bg #FAFAFA. Feature icons accent. CTA contrasting. | Feature card hover lift, scroll reveal, icon micro-interactions | Clear feature hierarchy. One key message per card. Strong CTA repetition. |
| 32 | Hero-Centric Design | hero-centric, hero-centric design, hero-first, hero above fold | 1. Full-bleed Hero (headline + visual), 2. Single value prop strip, 3. Key benefit or proof, 4. Primary CTA | Hero dominant (center/bottom) + Sticky nav CTA | Hero: High-impact visual. Minimal text. CTA 7:1 contrast. | Hero parallax or video, CTA pulse on scroll, minimal chrome | One primary CTA. Hero is 60-80% above fold. Mobile: same hierarchy. |
| 33 | Trust & Authority + Conversion | trust & authority, trust, authority, conversion, credibility, enterprise | 1. Hero (mission/credibility), 2. Proof (logos, certs, stats), 3. Solution overview, 4. Clear CTA path | Contact Sales / Get Quote (primary) + Nav | Navy/Grey corporate. Trust blue. Accent for CTA only. | Logo carousel, stat counters, testimonial strip | Security badges. Case studies. Transparent pricing. Low-friction form. |
| 34 | Real-Time / Operations Landing | real-time, real-time monitor, operations, dashboard, telemetry, live data | 1. Hero (product + live preview or status), 2. Key metrics/indicators, 3. How it works, 4. CTA (Start trial / Contact) | Primary CTA in nav + After metrics | Dark or neutral. Status colors (green/amber/red). Data-dense but scannable. | Live data ticker, status pulse, minimal decoration | For ops/security/iot products. Demo or sandbox link. Trust signals. |

## 3. Design-system reasoning rules

#### SaaS (General)

- **No:** 1
- **Recommended_Pattern:** Hero + Features + CTA
- **Style_Priority:** Glassmorphism + Flat Design
- **Color_Mood:** Trust blue + Accent contrast
- **Typography_Mood:** Professional + Hierarchy
- **Key_Effects:** Subtle hover (200-250ms) + Smooth transitions
- **Decision_Rules:** {"if_ux_focused": "prioritize-minimalism", "if_data_heavy": "add-glassmorphism"}
- **Anti_Patterns:** Excessive animation + Dark mode by default
- **Severity:** HIGH

#### Micro SaaS

- **No:** 2
- **Recommended_Pattern:** Hero-Centric + Trust
- **Style_Priority:** Motion-Driven + Vibrant & Block
- **Color_Mood:** Bold primaries + Accent contrast
- **Typography_Mood:** Modern + Energetic typography
- **Key_Effects:** Scroll-triggered animations + Parallax
- **Decision_Rules:** {"if_pre_launch": "use-waitlist-pattern", "if_video_ready": "add-hero-video"}
- **Anti_Patterns:** Static design + No video + Poor mobile
- **Severity:** HIGH

#### E-commerce

- **No:** 3
- **Recommended_Pattern:** Feature-Rich Showcase
- **Style_Priority:** Vibrant & Block-based
- **Color_Mood:** Brand primary + Success green
- **Typography_Mood:** Engaging + Clear hierarchy
- **Key_Effects:** Card hover lift (200ms) + Scale effect
- **Decision_Rules:** {"if_luxury": "switch-to-liquid-glass", "if_conversion_focused": "add-urgency-colors"}
- **Anti_Patterns:** Flat design without depth + Text-heavy pages
- **Severity:** HIGH

#### E-commerce Luxury

- **No:** 4
- **Recommended_Pattern:** Feature-Rich Showcase
- **Style_Priority:** Liquid Glass + Glassmorphism
- **Color_Mood:** Premium colors + Minimal accent
- **Typography_Mood:** Elegant + Refined typography
- **Key_Effects:** Chromatic aberration + Fluid animations (400-600ms)
- **Decision_Rules:** {"if_checkout": "emphasize-trust", "if_hero_needed": "use-3d-hyperrealism"}
- **Anti_Patterns:** Vibrant & Block-based + Playful colors
- **Severity:** HIGH

#### B2B Service

- **No:** 5
- **Recommended_Pattern:** Feature-Rich Showcase + Trust
- **Style_Priority:** Trust & Authority + Minimalism
- **Color_Mood:** Professional blue + Neutral grey
- **Typography_Mood:** Formal + Clear typography
- **Key_Effects:** Section transitions + Feature reveals
- **Decision_Rules:** {"must_have": "case-studies", "must_have": "roi-messaging"}
- **Anti_Patterns:** Playful design + Hidden credentials + AI purple/pink gradients
- **Severity:** HIGH

#### Financial Dashboard

- **No:** 6
- **Recommended_Pattern:** Data-Dense Dashboard
- **Style_Priority:** Dark Mode (OLED) + Data-Dense
- **Color_Mood:** Dark bg + Red/Green alerts + Trust blue
- **Typography_Mood:** Clear + Readable typography
- **Key_Effects:** Real-time number animations + Alert pulse
- **Decision_Rules:** {"must_have": "real-time-updates", "must_have": "high-contrast"}
- **Anti_Patterns:** Light mode default + Slow rendering
- **Severity:** HIGH

#### Analytics Dashboard

- **No:** 7
- **Recommended_Pattern:** Data-Dense + Drill-Down
- **Style_Priority:** Data-Dense + Heat Map
- **Color_Mood:** Cool→Hot gradients + Neutral grey
- **Typography_Mood:** Clear + Functional typography
- **Key_Effects:** Hover tooltips + Chart zoom + Filter animations
- **Decision_Rules:** {"must_have": "data-export", "if_large_dataset": "virtualize-lists"}
- **Anti_Patterns:** Ornate design + No filtering
- **Severity:** HIGH

#### Healthcare App

- **No:** 8
- **Recommended_Pattern:** Social Proof-Focused
- **Style_Priority:** Neumorphism + Accessible & Ethical
- **Color_Mood:** Calm blue + Health green
- **Typography_Mood:** Readable + Large type (16px+)
- **Key_Effects:** Soft box-shadow + Smooth press (150ms)
- **Decision_Rules:** {"must_have": "wcag-aaa-compliance", "if_medication": "red-alert-colors"}
- **Anti_Patterns:** Bright neon colors + Motion-heavy animations + AI purple/pink gradients
- **Severity:** HIGH

#### Educational App

- **No:** 9
- **Recommended_Pattern:** Feature-Rich Showcase
- **Style_Priority:** Claymorphism + Micro-interactions
- **Color_Mood:** Playful colors + Clear hierarchy
- **Typography_Mood:** Friendly + Engaging typography
- **Key_Effects:** Soft press (200ms) + Fluffy elements
- **Decision_Rules:** {"if_gamification": "add-progress-animation", "if_children": "increase-playfulness"}
- **Anti_Patterns:** Dark modes + Complex jargon
- **Severity:** MEDIUM

#### Creative Agency

- **No:** 10
- **Recommended_Pattern:** Storytelling-Driven
- **Style_Priority:** Brutalism + Motion-Driven
- **Color_Mood:** Bold primaries + Artistic freedom
- **Typography_Mood:** Bold + Expressive typography
- **Key_Effects:** CRT scanlines + Neon glow + Glitch effects
- **Decision_Rules:** {"must_have": "case-studies", "if_boutique": "increase-artistic-freedom"}
- **Anti_Patterns:** Corporate minimalism + Hidden portfolio
- **Severity:** HIGH

#### Portfolio/Personal

- **No:** 11
- **Recommended_Pattern:** Storytelling-Driven
- **Style_Priority:** Motion-Driven + Minimalism
- **Color_Mood:** Brand primary + Artistic
- **Typography_Mood:** Expressive + Variable typography
- **Key_Effects:** Parallax (3-5 layers) + Scroll-triggered reveals
- **Decision_Rules:** {"if_creative_field": "add-brutalism", "if_minimal_portfolio": "reduce-motion"}
- **Anti_Patterns:** Corporate templates + Generic layouts
- **Severity:** MEDIUM

#### Gaming

- **No:** 12
- **Recommended_Pattern:** Feature-Rich Showcase
- **Style_Priority:** 3D & Hyperrealism + Retro-Futurism
- **Color_Mood:** Vibrant + Neon + Immersive
- **Typography_Mood:** Bold + Impactful typography
- **Key_Effects:** WebGL 3D rendering + Glitch effects
- **Decision_Rules:** {"if_competitive": "add-real-time-stats", "if_casual": "increase-playfulness"}
- **Anti_Patterns:** Minimalist design + Static assets
- **Severity:** HIGH

#### Government/Public Service

- **No:** 13
- **Recommended_Pattern:** Minimal & Direct
- **Style_Priority:** Accessible & Ethical + Minimalism
- **Color_Mood:** Professional blue + High contrast
- **Typography_Mood:** Clear + Large typography
- **Key_Effects:** Clear focus rings (3-4px) + Skip links
- **Decision_Rules:** {"must_have": "wcag-aaa", "must_have": "keyboard-navigation"}
- **Anti_Patterns:** Ornate design + Low contrast + Motion effects + AI purple/pink gradients
- **Severity:** HIGH

#### Fintech/Crypto

- **No:** 14
- **Recommended_Pattern:** Trust & Authority
- **Style_Priority:** Minimalism + Accessible & Ethical
- **Color_Mood:** Navy + Trust Blue + Gold
- **Typography_Mood:** Professional + Trustworthy
- **Key_Effects:** Smooth state transitions + Number animations
- **Decision_Rules:** {"must_have": "security-first", "if_dashboard": "use-dark-mode"}
- **Anti_Patterns:** Playful design + Unclear fees + AI purple/pink gradients
- **Severity:** HIGH

#### Social Media App

- **No:** 15
- **Recommended_Pattern:** Feature-Rich Showcase
- **Style_Priority:** Vibrant & Block-based + Motion-Driven
- **Color_Mood:** Vibrant + Engagement colors
- **Typography_Mood:** Modern + Bold typography
- **Key_Effects:** Large scroll animations + Icon animations
- **Decision_Rules:** {"if_engagement_metric": "add-motion", "if_content_focused": "minimize-chrome"}
- **Anti_Patterns:** Heavy skeuomorphism + Accessibility ignored
- **Severity:** MEDIUM

#### Productivity Tool

- **No:** 16
- **Recommended_Pattern:** Interactive Demo + Feature-Rich
- **Style_Priority:** Flat Design + Micro-interactions
- **Color_Mood:** Clear hierarchy + Functional colors
- **Typography_Mood:** Clean + Efficient typography
- **Key_Effects:** Quick actions (150ms) + Task animations
- **Decision_Rules:** {"must_have": "keyboard-shortcuts", "if_collaboration": "add-real-time-cursors"}
- **Anti_Patterns:** Complex onboarding + Slow performance
- **Severity:** HIGH

#### Design System/Component Library

- **No:** 17
- **Recommended_Pattern:** Feature-Rich + Documentation
- **Style_Priority:** Minimalism + Accessible & Ethical
- **Color_Mood:** Clear hierarchy + Code-like structure
- **Typography_Mood:** Monospace + Clear typography
- **Key_Effects:** Code copy animations + Component previews
- **Decision_Rules:** {"must_have": "search", "must_have": "code-examples"}
- **Anti_Patterns:** Poor documentation + No live preview
- **Severity:** HIGH

#### AI/Chatbot Platform

- **No:** 18
- **Recommended_Pattern:** Interactive Demo + Minimal
- **Style_Priority:** AI-Native UI + Minimalism
- **Color_Mood:** Neutral + AI Purple (#6366F1)
- **Typography_Mood:** Modern + Clear typography
- **Key_Effects:** Streaming text + Typing indicators + Fade-in
- **Decision_Rules:** {"must_have": "conversational-ui", "must_have": "context-awareness"}
- **Anti_Patterns:** Heavy chrome + Slow response feedback
- **Severity:** HIGH

#### NFT/Web3 Platform

- **No:** 19
- **Recommended_Pattern:** Feature-Rich Showcase
- **Style_Priority:** Cyberpunk UI + Glassmorphism
- **Color_Mood:** Dark + Neon + Gold (#FFD700)
- **Typography_Mood:** Bold + Modern typography
- **Key_Effects:** Wallet connect animations + Transaction feedback
- **Decision_Rules:** {"must_have": "wallet-integration", "must_have": "gas-fees-display"}
- **Anti_Patterns:** Light mode default + No transaction status
- **Severity:** HIGH

#### Creator Economy Platform

- **No:** 20
- **Recommended_Pattern:** Social Proof + Feature-Rich
- **Style_Priority:** Vibrant & Block-based + Bento Box Grid
- **Color_Mood:** Vibrant + Brand colors
- **Typography_Mood:** Modern + Bold typography
- **Key_Effects:** Engagement counter animations + Profile reveals
- **Decision_Rules:** {"must_have": "creator-profiles", "must_have": "monetization-display"}
- **Anti_Patterns:** Generic layout + Hidden earnings
- **Severity:** MEDIUM

#### Remote Work/Collaboration Tool

- **No:** 21
- **Recommended_Pattern:** Feature-Rich + Real-Time
- **Style_Priority:** Soft UI Evolution + Minimalism
- **Color_Mood:** Calm Blue + Neutral grey
- **Typography_Mood:** Clean + Readable typography
- **Key_Effects:** Real-time presence indicators + Notification badges
- **Decision_Rules:** {"must_have": "status-indicators", "must_have": "video-integration"}
- **Anti_Patterns:** Cluttered interface + No presence
- **Severity:** HIGH

#### Mental Health App

- **No:** 22
- **Recommended_Pattern:** Social Proof-Focused
- **Style_Priority:** Neumorphism + Accessible & Ethical
- **Color_Mood:** Calm Pastels + Trust colors
- **Typography_Mood:** Calming + Readable typography
- **Key_Effects:** Soft press + Breathing animations
- **Decision_Rules:** {"must_have": "privacy-first", "if_meditation": "add-breathing-animation"}
- **Anti_Patterns:** Bright neon + Motion overload
- **Severity:** HIGH

#### Pet Tech App

- **No:** 23
- **Recommended_Pattern:** Storytelling + Feature-Rich
- **Style_Priority:** Claymorphism + Vibrant & Block-based
- **Color_Mood:** Playful + Warm colors
- **Typography_Mood:** Friendly + Playful typography
- **Key_Effects:** Pet profile animations + Health tracking charts
- **Decision_Rules:** {"must_have": "pet-profiles", "if_health": "add-vet-integration"}
- **Anti_Patterns:** Generic design + No personality
- **Severity:** MEDIUM

#### Smart Home/IoT Dashboard

- **No:** 24
- **Recommended_Pattern:** Real-Time Monitoring
- **Style_Priority:** Glassmorphism + Dark Mode (OLED)
- **Color_Mood:** Dark + Status indicator colors
- **Typography_Mood:** Clear + Functional typography
- **Key_Effects:** Device status pulse + Quick action animations
- **Decision_Rules:** {"must_have": "real-time-controls", "must_have": "energy-monitoring"}
- **Anti_Patterns:** Slow updates + No automation
- **Severity:** HIGH

#### EV/Charging Ecosystem

- **No:** 25
- **Recommended_Pattern:** Hero-Centric + Feature-Rich
- **Style_Priority:** Minimalism + Aurora UI
- **Color_Mood:** Electric Blue (#009CD1) + Green
- **Typography_Mood:** Modern + Clear typography
- **Key_Effects:** Range estimation animations + Map interactions
- **Decision_Rules:** {"must_have": "charging-map", "must_have": "range-calculator"}
- **Anti_Patterns:** Poor map UX + Hidden costs
- **Severity:** HIGH

#### Subscription Box Service

- **No:** 26
- **Recommended_Pattern:** Feature-Rich + Conversion
- **Style_Priority:** Vibrant & Block-based + Motion-Driven
- **Color_Mood:** Brand + Excitement colors
- **Typography_Mood:** Engaging + Clear typography
- **Key_Effects:** Unboxing reveal animations + Product carousel
- **Decision_Rules:** {"must_have": "personalization-quiz", "must_have": "subscription-management"}
- **Anti_Patterns:** Confusing pricing + No unboxing preview
- **Severity:** HIGH

#### Podcast Platform

- **No:** 27
- **Recommended_Pattern:** Storytelling + Feature-Rich
- **Style_Priority:** Dark Mode (OLED) + Minimalism
- **Color_Mood:** Dark + Audio waveform accents
- **Typography_Mood:** Modern + Clear typography
- **Key_Effects:** Waveform visualizations + Episode transitions
- **Decision_Rules:** {"must_have": "audio-player-ux", "must_have": "episode-discovery"}
- **Anti_Patterns:** Poor audio player + Cluttered layout
- **Severity:** HIGH

#### Dating App

- **No:** 28
- **Recommended_Pattern:** Social Proof + Feature-Rich
- **Style_Priority:** Vibrant & Block-based + Motion-Driven
- **Color_Mood:** Warm + Romantic (Pink/Red gradients)
- **Typography_Mood:** Modern + Friendly typography
- **Key_Effects:** Profile card swipe + Match animations
- **Decision_Rules:** {"must_have": "profile-cards", "must_have": "safety-features"}
- **Anti_Patterns:** Generic profiles + No safety
- **Severity:** HIGH

#### Micro-Credentials/Badges Platform

- **No:** 29
- **Recommended_Pattern:** Trust & Authority + Feature
- **Style_Priority:** Minimalism + Flat Design
- **Color_Mood:** Trust Blue + Gold (#FFD700)
- **Typography_Mood:** Professional + Clear typography
- **Key_Effects:** Badge reveal animations + Progress tracking
- **Decision_Rules:** {"must_have": "credential-verification", "must_have": "progress-display"}
- **Anti_Patterns:** No verification + Hidden progress
- **Severity:** MEDIUM

#### Knowledge Base/Documentation

- **No:** 30
- **Recommended_Pattern:** FAQ + Minimal
- **Style_Priority:** Minimalism + Accessible & Ethical
- **Color_Mood:** Clean hierarchy + Minimal color
- **Typography_Mood:** Clear + Readable typography
- **Key_Effects:** Search highlight + Smooth scrolling
- **Decision_Rules:** {"must_have": "search-first", "must_have": "version-switching"}
- **Anti_Patterns:** Poor navigation + No search
- **Severity:** HIGH

#### Hyperlocal Services

- **No:** 31
- **Recommended_Pattern:** Conversion + Feature-Rich
- **Style_Priority:** Minimalism + Vibrant & Block-based
- **Color_Mood:** Location markers + Trust colors
- **Typography_Mood:** Clear + Functional typography
- **Key_Effects:** Map hover + Provider card reveals
- **Decision_Rules:** {"must_have": "map-integration", "must_have": "booking-system"}
- **Anti_Patterns:** No map + Hidden reviews
- **Severity:** HIGH

#### Beauty/Spa/Wellness Service

- **No:** 32
- **Recommended_Pattern:** Hero-Centric + Social Proof
- **Style_Priority:** Soft UI Evolution + Neumorphism
- **Color_Mood:** Soft pastels (Pink Sage Cream) + Gold accents
- **Typography_Mood:** Elegant + Calming typography
- **Key_Effects:** Soft shadows + Smooth transitions (200-300ms) + Gentle hover
- **Decision_Rules:** {"must_have": "booking-system", "must_have": "before-after-gallery", "if_luxury": "add-gold-accents"}
- **Anti_Patterns:** Bright neon colors + Harsh animations + Dark mode
- **Severity:** HIGH

#### Luxury/Premium Brand

- **No:** 33
- **Recommended_Pattern:** Storytelling + Feature-Rich
- **Style_Priority:** Liquid Glass + Glassmorphism
- **Color_Mood:** Black + Gold (#FFD700) + White
- **Typography_Mood:** Elegant + Refined typography
- **Key_Effects:** Slow parallax + Premium reveals (400-600ms)
- **Decision_Rules:** {"must_have": "high-quality-imagery", "must_have": "storytelling"}
- **Anti_Patterns:** Cheap visuals + Fast animations
- **Severity:** HIGH

#### Restaurant/Food Service

- **No:** 34
- **Recommended_Pattern:** Hero-Centric + Conversion
- **Style_Priority:** Vibrant & Block-based + Motion-Driven
- **Color_Mood:** Warm colors (Orange Red Brown)
- **Typography_Mood:** Appetizing + Clear typography
- **Key_Effects:** Food image reveal + Menu hover effects
- **Decision_Rules:** {"must_have": "high_quality_images", "if_delivery": "emphasize-speed"}
- **Anti_Patterns:** Low-quality imagery + Outdated hours
- **Severity:** HIGH

#### Fitness/Gym App

- **No:** 35
- **Recommended_Pattern:** Feature-Rich + Data
- **Style_Priority:** Vibrant & Block-based + Dark Mode (OLED)
- **Color_Mood:** Energetic (Orange #FF6B35) + Dark bg
- **Typography_Mood:** Bold + Motivational typography
- **Key_Effects:** Progress ring animations + Achievement unlocks
- **Decision_Rules:** {"must_have": "progress-tracking", "must_have": "workout-plans"}
- **Anti_Patterns:** Static design + No gamification
- **Severity:** HIGH

#### Real Estate/Property

- **No:** 36
- **Recommended_Pattern:** Hero-Centric + Feature-Rich
- **Style_Priority:** Glassmorphism + Minimalism
- **Color_Mood:** Trust Blue + Gold + White
- **Typography_Mood:** Professional + Confident
- **Key_Effects:** 3D property tour zoom + Map hover
- **Decision_Rules:** {"if_luxury": "add-3d-models", "must_have": "map-integration"}
- **Anti_Patterns:** Poor photos + No virtual tours
- **Severity:** HIGH

#### Travel/Tourism Agency

- **No:** 37
- **Recommended_Pattern:** Storytelling-Driven + Hero
- **Style_Priority:** Aurora UI + Motion-Driven
- **Color_Mood:** Vibrant destination + Sky Blue
- **Typography_Mood:** Inspirational + Engaging
- **Key_Effects:** Destination parallax + Itinerary animations
- **Decision_Rules:** {"if_experience_focused": "use-storytelling", "must_have": "mobile-booking"}
- **Anti_Patterns:** Generic photos + Complex booking
- **Severity:** HIGH

#### Hotel/Hospitality

- **No:** 38
- **Recommended_Pattern:** Hero-Centric + Social Proof
- **Style_Priority:** Liquid Glass + Minimalism
- **Color_Mood:** Warm neutrals + Gold (#D4AF37)
- **Typography_Mood:** Elegant + Welcoming typography
- **Key_Effects:** Room gallery + Amenity reveals
- **Decision_Rules:** {"must_have": "room-booking", "must_have": "virtual-tour"}
- **Anti_Patterns:** Poor photos + Complex booking
- **Severity:** HIGH

#### Wedding/Event Planning

- **No:** 39
- **Recommended_Pattern:** Storytelling + Social Proof
- **Style_Priority:** Soft UI Evolution + Aurora UI
- **Color_Mood:** Soft Pink (#FFD6E0) + Gold + Cream
- **Typography_Mood:** Elegant + Romantic typography
- **Key_Effects:** Gallery reveals + Timeline animations
- **Decision_Rules:** {"must_have": "portfolio-gallery", "must_have": "planning-tools"}
- **Anti_Patterns:** Generic templates + No portfolio
- **Severity:** HIGH

#### Legal Services

- **No:** 40
- **Recommended_Pattern:** Trust & Authority + Minimal
- **Style_Priority:** Trust & Authority + Minimalism
- **Color_Mood:** Navy Blue (#1E3A5F) + Gold + White
- **Typography_Mood:** Professional + Authoritative typography
- **Key_Effects:** Practice area reveal + Attorney profile animations
- **Decision_Rules:** {"must_have": "case-results", "must_have": "credential-display"}
- **Anti_Patterns:** Outdated design + Hidden credentials + AI purple/pink gradients
- **Severity:** HIGH

#### Insurance Platform

- **No:** 41
- **Recommended_Pattern:** Conversion + Trust
- **Style_Priority:** Trust & Authority + Flat Design
- **Color_Mood:** Trust Blue (#0066CC) + Green + Neutral
- **Typography_Mood:** Clear + Professional typography
- **Key_Effects:** Quote calculator animations + Policy comparison
- **Decision_Rules:** {"must_have": "quote-calculator", "must_have": "policy-comparison"}
- **Anti_Patterns:** Confusing pricing + No trust signals + AI purple/pink gradients
- **Severity:** HIGH

#### Banking/Traditional Finance

- **No:** 42
- **Recommended_Pattern:** Trust & Authority + Feature
- **Style_Priority:** Minimalism + Accessible & Ethical
- **Color_Mood:** Navy (#0A1628) + Trust Blue + Gold
- **Typography_Mood:** Professional + Trustworthy typography
- **Key_Effects:** Smooth number animations + Security indicators
- **Decision_Rules:** {"must_have": "security-first", "must_have": "accessibility"}
- **Anti_Patterns:** Playful design + Poor security UX + AI purple/pink gradients
- **Severity:** HIGH

#### Online Course/E-learning

- **No:** 43
- **Recommended_Pattern:** Feature-Rich + Social Proof
- **Style_Priority:** Claymorphism + Vibrant & Block-based
- **Color_Mood:** Vibrant learning colors + Progress green
- **Typography_Mood:** Friendly + Engaging typography
- **Key_Effects:** Progress bar animations + Certificate reveals
- **Decision_Rules:** {"must_have": "progress-tracking", "must_have": "video-player"}
- **Anti_Patterns:** Boring design + No gamification
- **Severity:** HIGH

#### Non-profit/Charity

- **No:** 44
- **Recommended_Pattern:** Storytelling + Trust
- **Style_Priority:** Accessible & Ethical + Organic Biophilic
- **Color_Mood:** Cause-related colors + Trust + Warm
- **Typography_Mood:** Heartfelt + Readable typography
- **Key_Effects:** Impact counter animations + Story reveals
- **Decision_Rules:** {"must_have": "impact-stories", "must_have": "donation-transparency"}
- **Anti_Patterns:** No impact data + Hidden financials
- **Severity:** HIGH

#### Music Streaming

- **No:** 45
- **Recommended_Pattern:** Feature-Rich Showcase
- **Style_Priority:** Dark Mode (OLED) + Vibrant & Block-based
- **Color_Mood:** Dark (#121212) + Vibrant accents + Album art colors
- **Typography_Mood:** Modern + Bold typography
- **Key_Effects:** Waveform visualization + Playlist animations
- **Decision_Rules:** {"must_have": "audio-player-ux", "if_discovery_focused": "add-playlist-recommendations"}
- **Anti_Patterns:** Cluttered layout + Poor audio player UX
- **Severity:** HIGH

#### Video Streaming/OTT

- **No:** 46
- **Recommended_Pattern:** Hero-Centric + Feature-Rich
- **Style_Priority:** Dark Mode (OLED) + Motion-Driven
- **Color_Mood:** Dark bg + Poster colors + Brand accent
- **Typography_Mood:** Bold + Engaging typography
- **Key_Effects:** Video player animations + Content carousel (parallax)
- **Decision_Rules:** {"must_have": "continue-watching", "if_personalized": "add-recommendations"}
- **Anti_Patterns:** Static layout + Slow video player
- **Severity:** HIGH

#### Job Board/Recruitment

- **No:** 47
- **Recommended_Pattern:** Conversion-Optimized + Feature-Rich
- **Style_Priority:** Flat Design + Minimalism
- **Color_Mood:** Professional Blue + Success Green + Neutral
- **Typography_Mood:** Clear + Professional typography
- **Key_Effects:** Search/filter animations + Application flow
- **Decision_Rules:** {"must_have": "advanced-search", "if_salary_focused": "highlight-compensation"}
- **Anti_Patterns:** Outdated forms + Hidden filters
- **Severity:** HIGH

#### Marketplace (P2P)

- **No:** 48
- **Recommended_Pattern:** Feature-Rich Showcase + Social Proof
- **Style_Priority:** Vibrant & Block-based + Flat Design
- **Color_Mood:** Trust colors + Category colors + Success green
- **Typography_Mood:** Modern + Engaging typography
- **Key_Effects:** Review star animations + Listing hover effects
- **Decision_Rules:** {"must_have": "seller-profiles", "must_have": "secure-payment"}
- **Anti_Patterns:** Low trust signals + Confusing layout
- **Severity:** HIGH

#### Logistics/Delivery

- **No:** 49
- **Recommended_Pattern:** Feature-Rich Showcase + Real-Time
- **Style_Priority:** Minimalism + Flat Design
- **Color_Mood:** Blue (#2563EB) + Orange (tracking) + Green
- **Typography_Mood:** Clear + Functional typography
- **Key_Effects:** Real-time tracking animation + Status pulse
- **Decision_Rules:** {"must_have": "tracking-map", "must_have": "delivery-updates"}
- **Anti_Patterns:** Static tracking + No map integration + AI purple/pink gradients
- **Severity:** HIGH

#### Agriculture/Farm Tech

- **No:** 50
- **Recommended_Pattern:** Feature-Rich Showcase
- **Style_Priority:** Organic Biophilic + Flat Design
- **Color_Mood:** Earth Green (#4A7C23) + Brown + Sky Blue
- **Typography_Mood:** Clear + Informative typography
- **Key_Effects:** Data visualization + Weather animations
- **Decision_Rules:** {"must_have": "sensor-dashboard", "if_crop_focused": "add-health-indicators"}
- **Anti_Patterns:** Generic design + Ignored accessibility + AI purple/pink gradients
- **Severity:** MEDIUM

#### Construction/Architecture

- **No:** 51
- **Recommended_Pattern:** Hero-Centric + Feature-Rich
- **Style_Priority:** Minimalism + 3D & Hyperrealism
- **Color_Mood:** Grey (#4A4A4A) + Orange (safety) + Blueprint Blue
- **Typography_Mood:** Professional + Bold typography
- **Key_Effects:** 3D model viewer + Timeline animations
- **Decision_Rules:** {"must_have": "project-portfolio", "if_team_collaboration": "add-real-time-updates"}
- **Anti_Patterns:** 2D-only layouts + Poor image quality + AI purple/pink gradients
- **Severity:** HIGH

#### Automotive/Car Dealership

- **No:** 52
- **Recommended_Pattern:** Hero-Centric + Feature-Rich
- **Style_Priority:** Motion-Driven + 3D & Hyperrealism
- **Color_Mood:** Brand colors + Metallic + Dark/Light
- **Typography_Mood:** Bold + Confident typography
- **Key_Effects:** 360 product view + Configurator animations
- **Decision_Rules:** {"must_have": "vehicle-comparison", "must_have": "financing-calculator"}
- **Anti_Patterns:** Static product pages + Poor UX
- **Severity:** HIGH

#### Photography Studio

- **No:** 53
- **Recommended_Pattern:** Storytelling-Driven + Hero-Centric
- **Style_Priority:** Motion-Driven + Minimalism
- **Color_Mood:** Black + White + Minimal accent
- **Typography_Mood:** Elegant + Minimal typography
- **Key_Effects:** Full-bleed gallery + Before/after reveal
- **Decision_Rules:** {"must_have": "portfolio-showcase", "if_booking": "add-calendar-system"}
- **Anti_Patterns:** Heavy text + Poor image showcase
- **Severity:** HIGH

#### Coworking Space

- **No:** 54
- **Recommended_Pattern:** Hero-Centric + Feature-Rich
- **Style_Priority:** Vibrant & Block-based + Glassmorphism
- **Color_Mood:** Energetic colors + Wood tones + Brand
- **Typography_Mood:** Modern + Engaging typography
- **Key_Effects:** Space tour video + Amenity reveal animations
- **Decision_Rules:** {"must_have": "virtual-tour", "must_have": "booking-system"}
- **Anti_Patterns:** Outdated photos + Confusing layout
- **Severity:** MEDIUM

#### Home Services (Plumber/Electrician)

- **No:** 55
- **Recommended_Pattern:** Conversion-Optimized + Trust
- **Style_Priority:** Flat Design + Trust & Authority
- **Color_Mood:** Trust Blue + Safety Orange + Grey
- **Typography_Mood:** Professional + Clear typography
- **Key_Effects:** Emergency contact highlight + Service menu animations
- **Decision_Rules:** {"must_have": "emergency-contact", "must_have": "certifications-display"}
- **Anti_Patterns:** Hidden contact info + No certifications
- **Severity:** HIGH

#### Childcare/Daycare

- **No:** 56
- **Recommended_Pattern:** Social Proof-Focused + Trust
- **Style_Priority:** Claymorphism + Vibrant & Block-based
- **Color_Mood:** Playful pastels + Safe colors + Warm
- **Typography_Mood:** Friendly + Playful typography
- **Key_Effects:** Parent portal animations + Activity gallery reveal
- **Decision_Rules:** {"must_have": "parent-communication", "must_have": "safety-certifications"}
- **Anti_Patterns:** Generic design + Hidden safety info
- **Severity:** HIGH

#### Senior Care/Elderly

- **No:** 57
- **Recommended_Pattern:** Trust & Authority + Accessible
- **Style_Priority:** Accessible & Ethical + Soft UI Evolution
- **Color_Mood:** Calm Blue + Warm neutrals + Large text
- **Typography_Mood:** Large + Clear typography (18px+)
- **Key_Effects:** Large touch targets + Clear navigation
- **Decision_Rules:** {"must_have": "wcag-aaa", "must_have": "family-portal"}
- **Anti_Patterns:** Small text + Complex navigation + AI purple/pink gradients
- **Severity:** HIGH

#### Medical Clinic

- **No:** 58
- **Recommended_Pattern:** Trust & Authority + Conversion
- **Style_Priority:** Accessible & Ethical + Minimalism
- **Color_Mood:** Medical Blue (#0077B6) + Trust White
- **Typography_Mood:** Professional + Readable typography
- **Key_Effects:** Online booking flow + Doctor profile reveals
- **Decision_Rules:** {"must_have": "appointment-booking", "must_have": "insurance-info"}
- **Anti_Patterns:** Outdated interface + Confusing booking + AI purple/pink gradients
- **Severity:** HIGH

#### Pharmacy/Drug Store

- **No:** 59
- **Recommended_Pattern:** Conversion-Optimized + Trust
- **Style_Priority:** Flat Design + Accessible & Ethical
- **Color_Mood:** Pharmacy Green + Trust Blue + Clean White
- **Typography_Mood:** Clear + Functional typography
- **Key_Effects:** Prescription upload flow + Refill reminders
- **Decision_Rules:** {"must_have": "prescription-management", "must_have": "drug-interaction-warnings"}
- **Anti_Patterns:** Confusing layout + Privacy concerns + AI purple/pink gradients
- **Severity:** HIGH

#### Dental Practice

- **No:** 60
- **Recommended_Pattern:** Social Proof-Focused + Conversion
- **Style_Priority:** Soft UI Evolution + Minimalism
- **Color_Mood:** Fresh Blue + White + Smile Yellow
- **Typography_Mood:** Friendly + Professional typography
- **Key_Effects:** Before/after gallery + Patient testimonial carousel
- **Decision_Rules:** {"must_have": "before-after-gallery", "must_have": "appointment-system"}
- **Anti_Patterns:** Poor imagery + No testimonials
- **Severity:** HIGH

#### Veterinary Clinic

- **No:** 61
- **Recommended_Pattern:** Social Proof-Focused + Trust
- **Style_Priority:** Claymorphism + Accessible & Ethical
- **Color_Mood:** Caring Blue + Pet colors + Warm
- **Typography_Mood:** Friendly + Welcoming typography
- **Key_Effects:** Pet profile management + Service animations
- **Decision_Rules:** {"must_have": "pet-portal", "must_have": "emergency-contact"}
- **Anti_Patterns:** Generic design + Hidden services
- **Severity:** MEDIUM

#### Florist/Plant Shop

- **No:** 62
- **Recommended_Pattern:** Hero-Centric + Conversion
- **Style_Priority:** Organic Biophilic + Vibrant & Block-based
- **Color_Mood:** Natural Green + Floral pinks/purples
- **Typography_Mood:** Elegant + Natural typography
- **Key_Effects:** Product reveal + Seasonal transitions
- **Decision_Rules:** {"must_have": "delivery-scheduling", "must_have": "care-guides"}
- **Anti_Patterns:** Poor imagery + No seasonal content
- **Severity:** MEDIUM

#### Bakery/Cafe

- **No:** 63
- **Recommended_Pattern:** Hero-Centric + Conversion
- **Style_Priority:** Vibrant & Block-based + Soft UI Evolution
- **Color_Mood:** Warm Brown + Cream + Appetizing accents
- **Typography_Mood:** Warm + Inviting typography
- **Key_Effects:** Menu hover + Order animations
- **Decision_Rules:** {"must_have": "menu-display", "must_have": "online-ordering"}
- **Anti_Patterns:** Poor food photos + Hidden hours
- **Severity:** HIGH

#### Brewery/Winery

- **No:** 64
- **Recommended_Pattern:** Storytelling + Hero-Centric
- **Style_Priority:** Motion-Driven + Storytelling-Driven
- **Color_Mood:** Deep amber/burgundy + Gold + Craft
- **Typography_Mood:** Artisanal + Heritage typography
- **Key_Effects:** Tasting note reveals + Heritage timeline
- **Decision_Rules:** {"must_have": "product-showcase", "must_have": "story-heritage"}
- **Anti_Patterns:** Generic product pages + No story
- **Severity:** HIGH

#### Airline

- **No:** 65
- **Recommended_Pattern:** Conversion + Feature-Rich
- **Style_Priority:** Minimalism + Glassmorphism
- **Color_Mood:** Sky Blue + Brand colors + Trust
- **Typography_Mood:** Clear + Professional typography
- **Key_Effects:** Flight search animations + Boarding pass reveals
- **Decision_Rules:** {"must_have": "flight-search", "must_have": "mobile-first"}
- **Anti_Patterns:** Complex booking + Poor mobile
- **Severity:** HIGH

#### News/Media Platform

- **No:** 66
- **Recommended_Pattern:** Hero-Centric + Feature-Rich
- **Style_Priority:** Minimalism + Flat Design
- **Color_Mood:** Brand colors + High contrast
- **Typography_Mood:** Clear + Readable typography
- **Key_Effects:** Breaking news badge + Article reveal animations
- **Decision_Rules:** {"must_have": "mobile-first-reading", "must_have": "category-navigation"}
- **Anti_Patterns:** Cluttered layout + Slow loading
- **Severity:** HIGH

#### Magazine/Blog

- **No:** 67
- **Recommended_Pattern:** Storytelling + Hero-Centric
- **Style_Priority:** Swiss Modernism 2.0 + Motion-Driven
- **Color_Mood:** Editorial colors + Brand + Clean white
- **Typography_Mood:** Editorial + Elegant typography
- **Key_Effects:** Article transitions + Category reveals
- **Decision_Rules:** {"must_have": "article-showcase", "must_have": "newsletter-signup"}
- **Anti_Patterns:** Poor typography + Slow loading
- **Severity:** HIGH

#### Freelancer Platform

- **No:** 68
- **Recommended_Pattern:** Feature-Rich + Conversion
- **Style_Priority:** Flat Design + Minimalism
- **Color_Mood:** Professional Blue + Success Green
- **Typography_Mood:** Clear + Professional typography
- **Key_Effects:** Skill match animations + Review reveals
- **Decision_Rules:** {"must_have": "portfolio-display", "must_have": "skill-matching"}
- **Anti_Patterns:** Poor profiles + No reviews
- **Severity:** HIGH

#### Marketing Agency

- **No:** 69
- **Recommended_Pattern:** Storytelling + Feature-Rich
- **Style_Priority:** Brutalism + Motion-Driven
- **Color_Mood:** Bold brand colors + Creative freedom
- **Typography_Mood:** Bold + Expressive typography
- **Key_Effects:** Portfolio reveals + Results animations
- **Decision_Rules:** {"must_have": "portfolio", "must_have": "results-metrics"}
- **Anti_Patterns:** Boring design + Hidden work
- **Severity:** HIGH

#### Event Management

- **No:** 70
- **Recommended_Pattern:** Hero-Centric + Feature-Rich
- **Style_Priority:** Vibrant & Block-based + Motion-Driven
- **Color_Mood:** Event theme colors + Excitement accents
- **Typography_Mood:** Bold + Engaging typography
- **Key_Effects:** Countdown timer + Registration flow
- **Decision_Rules:** {"must_have": "registration", "must_have": "agenda-display"}
- **Anti_Patterns:** Confusing registration + No countdown
- **Severity:** HIGH

#### Membership/Community

- **No:** 71
- **Recommended_Pattern:** Social Proof + Conversion
- **Style_Priority:** Vibrant & Block-based + Soft UI Evolution
- **Color_Mood:** Community brand colors + Engagement
- **Typography_Mood:** Friendly + Engaging typography
- **Key_Effects:** Member counter + Benefit reveals
- **Decision_Rules:** {"must_have": "member-benefits", "must_have": "pricing-tiers"}
- **Anti_Patterns:** Hidden benefits + No community proof
- **Severity:** HIGH

#### Newsletter Platform

- **No:** 72
- **Recommended_Pattern:** Minimal + Conversion
- **Style_Priority:** Minimalism + Flat Design
- **Color_Mood:** Brand primary + Clean white + CTA
- **Typography_Mood:** Clean + Readable typography
- **Key_Effects:** Subscribe form + Archive reveals
- **Decision_Rules:** {"must_have": "subscribe-form", "must_have": "sample-content"}
- **Anti_Patterns:** Complex signup + No preview
- **Severity:** MEDIUM

#### Digital Products/Downloads

- **No:** 73
- **Recommended_Pattern:** Feature-Rich + Conversion
- **Style_Priority:** Vibrant & Block-based + Motion-Driven
- **Color_Mood:** Product colors + Brand + Success green
- **Typography_Mood:** Modern + Clear typography
- **Key_Effects:** Product preview + Instant delivery animations
- **Decision_Rules:** {"must_have": "product-preview", "must_have": "instant-delivery"}
- **Anti_Patterns:** No preview + Slow delivery
- **Severity:** HIGH

#### Church/Religious Organization

- **No:** 74
- **Recommended_Pattern:** Hero-Centric + Social Proof
- **Style_Priority:** Accessible & Ethical + Soft UI Evolution
- **Color_Mood:** Warm Gold + Deep Purple/Blue + White
- **Typography_Mood:** Welcoming + Clear typography
- **Key_Effects:** Service time highlights + Event calendar
- **Decision_Rules:** {"must_have": "service-times", "must_have": "community-events"}
- **Anti_Patterns:** Outdated design + Hidden info
- **Severity:** MEDIUM

#### Sports Team/Club

- **No:** 75
- **Recommended_Pattern:** Hero-Centric + Feature-Rich
- **Style_Priority:** Vibrant & Block-based + Motion-Driven
- **Color_Mood:** Team colors + Energetic accents
- **Typography_Mood:** Bold + Impactful typography
- **Key_Effects:** Score animations + Schedule reveals
- **Decision_Rules:** {"must_have": "schedule", "must_have": "roster"}
- **Anti_Patterns:** Static content + Poor fan engagement
- **Severity:** HIGH

#### Museum/Gallery

- **No:** 76
- **Recommended_Pattern:** Storytelling + Feature-Rich
- **Style_Priority:** Minimalism + Motion-Driven
- **Color_Mood:** Art-appropriate neutrals + Exhibition accents
- **Typography_Mood:** Elegant + Minimal typography
- **Key_Effects:** Virtual tour + Collection reveals
- **Decision_Rules:** {"must_have": "virtual-tour", "must_have": "exhibition-info"}
- **Anti_Patterns:** Cluttered layout + No online access
- **Severity:** HIGH

#### Theater/Cinema

- **No:** 77
- **Recommended_Pattern:** Hero-Centric + Conversion
- **Style_Priority:** Dark Mode (OLED) + Motion-Driven
- **Color_Mood:** Dark + Spotlight accents + Gold
- **Typography_Mood:** Dramatic + Bold typography
- **Key_Effects:** Seat selection + Trailer reveals
- **Decision_Rules:** {"must_have": "showtimes", "must_have": "seat-selection"}
- **Anti_Patterns:** Poor booking UX + No trailers
- **Severity:** HIGH

#### Language Learning App

- **No:** 78
- **Recommended_Pattern:** Feature-Rich + Social Proof
- **Style_Priority:** Claymorphism + Vibrant & Block-based
- **Color_Mood:** Playful colors + Progress indicators
- **Typography_Mood:** Friendly + Clear typography
- **Key_Effects:** Progress animations + Achievement unlocks
- **Decision_Rules:** {"must_have": "progress-tracking", "must_have": "gamification"}
- **Anti_Patterns:** Boring design + No motivation
- **Severity:** HIGH

#### Coding Bootcamp

- **No:** 79
- **Recommended_Pattern:** Feature-Rich + Social Proof
- **Style_Priority:** Dark Mode (OLED) + Minimalism
- **Color_Mood:** Code editor colors + Brand + Success
- **Typography_Mood:** Technical + Clear typography
- **Key_Effects:** Terminal animations + Career outcome reveals
- **Decision_Rules:** {"must_have": "curriculum", "must_have": "career-outcomes"}
- **Anti_Patterns:** Light mode only + Hidden results
- **Severity:** HIGH

#### Cybersecurity Platform

- **No:** 80
- **Recommended_Pattern:** Trust & Authority + Real-Time
- **Style_Priority:** Cyberpunk UI + Dark Mode (OLED)
- **Color_Mood:** Matrix Green (#00FF00) + Deep Black
- **Typography_Mood:** Technical + Clear typography
- **Key_Effects:** Threat visualization + Alert animations
- **Decision_Rules:** {"must_have": "real-time-monitoring", "must_have": "threat-display"}
- **Anti_Patterns:** Light mode + Poor data viz
- **Severity:** HIGH

#### Developer Tool / IDE

- **No:** 81
- **Recommended_Pattern:** Minimal + Documentation
- **Style_Priority:** Dark Mode (OLED) + Minimalism
- **Color_Mood:** Dark syntax theme + Blue focus
- **Typography_Mood:** Monospace + Functional typography
- **Key_Effects:** Syntax highlighting + Command palette
- **Decision_Rules:** {"must_have": "keyboard-shortcuts", "must_have": "documentation"}
- **Anti_Patterns:** Light mode default + Slow performance
- **Severity:** HIGH

#### Biotech / Life Sciences

- **No:** 82
- **Recommended_Pattern:** Storytelling + Data
- **Style_Priority:** Glassmorphism + Clean Science
- **Color_Mood:** Sterile White + DNA Blue + Life Green
- **Typography_Mood:** Scientific + Clear typography
- **Key_Effects:** Data visualization + Research reveals
- **Decision_Rules:** {"must_have": "data-accuracy", "must_have": "clean-aesthetic"}
- **Anti_Patterns:** Cluttered data + Poor credibility
- **Severity:** HIGH

#### Space Tech / Aerospace

- **No:** 83
- **Recommended_Pattern:** Immersive + Feature-Rich
- **Style_Priority:** Holographic/HUD + Dark Mode
- **Color_Mood:** Deep Space Black + Star White + Metallic
- **Typography_Mood:** Futuristic + Precise typography
- **Key_Effects:** Telemetry animations + 3D renders
- **Decision_Rules:** {"must_have": "high-tech-feel", "must_have": "precision-data"}
- **Anti_Patterns:** Generic design + No immersion
- **Severity:** HIGH

#### Architecture / Interior

- **No:** 84
- **Recommended_Pattern:** Portfolio + Hero-Centric
- **Style_Priority:** Exaggerated Minimalism + High Imagery
- **Color_Mood:** Monochrome + Gold Accent + High Imagery
- **Typography_Mood:** Architectural + Elegant typography
- **Key_Effects:** Project gallery + Blueprint reveals
- **Decision_Rules:** {"must_have": "high-res-images", "must_have": "project-portfolio"}
- **Anti_Patterns:** Poor imagery + Cluttered layout
- **Severity:** HIGH

#### Quantum Computing Interface

- **No:** 85
- **Recommended_Pattern:** Immersive + Interactive
- **Style_Priority:** Holographic/HUD + Dark Mode
- **Color_Mood:** Quantum Blue (#00FFFF) + Deep Black
- **Typography_Mood:** Futuristic + Scientific typography
- **Key_Effects:** Probability visualizations + Qubit state animations
- **Decision_Rules:** {"must_have": "complexity-visualization", "must_have": "scientific-credibility"}
- **Anti_Patterns:** Generic tech design + No viz
- **Severity:** HIGH

#### Biohacking / Longevity App

- **No:** 86
- **Recommended_Pattern:** Data-Dense + Storytelling
- **Style_Priority:** Biomimetic/Organic 2.0 + Minimalism
- **Color_Mood:** Cellular Pink/Red + DNA Blue + White
- **Typography_Mood:** Scientific + Clear typography
- **Key_Effects:** Biological data viz + Progress animations
- **Decision_Rules:** {"must_have": "data-privacy", "must_have": "scientific-credibility"}
- **Anti_Patterns:** Generic health app + No privacy
- **Severity:** HIGH

#### Autonomous Drone Fleet Manager

- **No:** 87
- **Recommended_Pattern:** Real-Time + Feature-Rich
- **Style_Priority:** HUD/Sci-Fi FUI + Real-Time
- **Color_Mood:** Tactical Green + Alert Red + Map Dark
- **Typography_Mood:** Technical + Functional typography
- **Key_Effects:** Telemetry animations + 3D spatial awareness
- **Decision_Rules:** {"must_have": "real-time-telemetry", "must_have": "safety-alerts"}
- **Anti_Patterns:** Slow updates + Poor spatial viz
- **Severity:** HIGH

#### Generative Art Platform

- **No:** 88
- **Recommended_Pattern:** Showcase + Feature-Rich
- **Style_Priority:** Minimalism + Gen Z Chaos
- **Color_Mood:** Neutral (#F5F5F5) + User Content
- **Typography_Mood:** Minimal + Content-focused typography
- **Key_Effects:** Gallery masonry + Minting animations
- **Decision_Rules:** {"must_have": "fast-loading", "must_have": "creator-attribution"}
- **Anti_Patterns:** Heavy chrome + Slow loading
- **Severity:** HIGH

#### Spatial Computing OS / App

- **No:** 89
- **Recommended_Pattern:** Immersive + Interactive
- **Style_Priority:** Spatial UI (VisionOS) + Glassmorphism
- **Color_Mood:** Frosted Glass + System Colors + Depth
- **Typography_Mood:** Spatial + Readable typography
- **Key_Effects:** Depth hierarchy + Gaze interactions
- **Decision_Rules:** {"must_have": "depth-hierarchy", "must_have": "environment-awareness"}
- **Anti_Patterns:** 2D design + No spatial depth
- **Severity:** HIGH

#### Sustainable Energy / Climate Tech

- **No:** 90
- **Recommended_Pattern:** Data + Trust
- **Style_Priority:** Organic Biophilic + E-Ink/Paper
- **Color_Mood:** Earth Green + Sky Blue + Solar Yellow
- **Typography_Mood:** Clear + Informative typography
- **Key_Effects:** Impact viz + Progress animations
- **Decision_Rules:** {"must_have": "data-transparency", "must_have": "impact-visualization"}
- **Anti_Patterns:** Greenwashing + No real data
- **Severity:** HIGH

#### Personal Finance Tracker

- **No:** 91
- **Recommended_Pattern:** Interactive Product Demo
- **Style_Priority:** Glassmorphism + Dark Mode (OLED)
- **Color_Mood:** Calm blue + success green + alert red + chart accents
- **Typography_Mood:** Modern + Clear hierarchy
- **Key_Effects:** Backdrop blur (10-20px) + Translucent overlays
- **Decision_Rules:** {"if_light_mode_needed": "provide-theme-toggle", "if_low_performance": "fallback-to-flat"}
- **Anti_Patterns:** Pure white backgrounds
- **Severity:** HIGH

#### Chat & Messaging App

- **No:** 92
- **Recommended_Pattern:** Feature-Rich Showcase + Demo
- **Style_Priority:** Minimalism + Micro-interactions
- **Color_Mood:** Brand primary + bubble contrast (sender/receiver) + typing grey
- **Typography_Mood:** Professional + Clean hierarchy
- **Key_Effects:** Subtle hover 200ms + Smooth transitions + Clean
- **Decision_Rules:** {"if_ux_focused": "prioritize-clarity", "if_mobile": "optimize-touch-targets"}
- **Anti_Patterns:** Excessive decoration
- **Severity:** HIGH

#### Notes & Writing App

- **No:** 93
- **Recommended_Pattern:** Minimal & Direct
- **Style_Priority:** Minimalism + Flat Design
- **Color_Mood:** Clean white/cream + minimal accent + editor syntax colors
- **Typography_Mood:** Professional + Clean hierarchy
- **Key_Effects:** Color shift hover + Fast 150ms transitions + No shadows
- **Decision_Rules:** {"if_ux_focused": "prioritize-clarity", "if_mobile": "optimize-touch-targets"}
- **Anti_Patterns:** Excessive decoration + Complex shadows + 3D effects
- **Severity:** HIGH

#### Habit Tracker

- **No:** 94
- **Recommended_Pattern:** Social Proof-Focused + Demo
- **Style_Priority:** Claymorphism + Vibrant & Block-based
- **Color_Mood:** Streak warm (amber/orange) + progress green + motivational accents
- **Typography_Mood:** Playful + Rounded + Friendly
- **Key_Effects:** Multi-layer shadows + Spring bounce + Soft press 200ms
- **Decision_Rules:** {"if_trust_needed": "add-testimonials"}
- **Anti_Patterns:** Muted colors + Low energy
- **Severity:** HIGH

#### Food Delivery / On-Demand

- **No:** 95
- **Recommended_Pattern:** Hero-Centric Design + Feature-Rich
- **Style_Priority:** Vibrant & Block-based + Motion-Driven
- **Color_Mood:** Appetizing warm (orange/red) + trust blue + map accent
- **Typography_Mood:** Energetic + Bold + Large
- **Key_Effects:** Scroll animations + Parallax + Page transitions
- **Decision_Rules:** {"if_ux_focused": "prioritize-clarity", "if_mobile": "optimize-touch-targets"}
- **Anti_Patterns:** Muted colors + Low energy
- **Severity:** HIGH

#### Ride Hailing / Transportation

- **No:** 96
- **Recommended_Pattern:** Conversion-Optimized + Demo
- **Style_Priority:** Minimalism + Glassmorphism
- **Color_Mood:** Brand primary + map neutral + status indicator colors
- **Typography_Mood:** Professional + Clean hierarchy
- **Key_Effects:** Backdrop blur (10-20px) + Translucent overlays
- **Decision_Rules:** {"if_low_performance": "fallback-to-flat", "if_conversion_focused": "add-urgency-colors"}
- **Anti_Patterns:** Excessive decoration
- **Severity:** HIGH

#### Recipe & Cooking App

- **No:** 97
- **Recommended_Pattern:** Hero-Centric Design + Feature-Rich
- **Style_Priority:** Claymorphism + Vibrant & Block-based
- **Color_Mood:** Warm food tones (terracotta/sage/cream) + appetizing imagery
- **Typography_Mood:** Playful + Rounded + Friendly
- **Key_Effects:** Multi-layer shadows + Spring bounce + Soft press 200ms
- **Decision_Rules:** {"if_ux_focused": "prioritize-clarity", "if_mobile": "optimize-touch-targets"}
- **Anti_Patterns:** Muted colors + Low energy
- **Severity:** HIGH

#### Meditation & Mindfulness

- **No:** 98
- **Recommended_Pattern:** Storytelling-Driven + Social Proof
- **Style_Priority:** Neumorphism + Soft UI Evolution
- **Color_Mood:** Ultra-calm pastels (lavender/sage/sky) + breathing animation gradient
- **Typography_Mood:** Subtle + Soft + Monochromatic
- **Key_Effects:** Dual shadows (light+dark) + Soft press 150ms
- **Decision_Rules:** {"if_trust_needed": "add-testimonials"}
- **Anti_Patterns:** Inconsistent styling + Poor contrast ratios
- **Severity:** HIGH

#### Weather App

- **No:** 99
- **Recommended_Pattern:** Hero-Centric Design
- **Style_Priority:** Glassmorphism + Aurora UI
- **Color_Mood:** Atmospheric gradients (sky blue → sunset → storm grey) + temp scale
- **Typography_Mood:** Modern + Clear hierarchy
- **Key_Effects:** Backdrop blur (10-20px) + Translucent overlays
- **Decision_Rules:** {"if_low_performance": "fallback-to-flat"}
- **Anti_Patterns:** Inconsistent styling + Poor contrast ratios
- **Severity:** HIGH

#### Diary & Journal App

- **No:** 100
- **Recommended_Pattern:** Storytelling-Driven
- **Style_Priority:** Soft UI Evolution + Minimalism
- **Color_Mood:** Warm paper tones (cream/linen) + muted ink + mood-coded accents
- **Typography_Mood:** Professional + Clean hierarchy
- **Key_Effects:** Subtle hover 200ms + Smooth transitions + Clean
- **Decision_Rules:** {"if_ux_focused": "prioritize-clarity", "if_mobile": "optimize-touch-targets"}
- **Anti_Patterns:** Excessive decoration
- **Severity:** HIGH

#### CRM & Client Management

- **No:** 101
- **Recommended_Pattern:** Feature-Rich Showcase + Demo
- **Style_Priority:** Flat Design + Minimalism
- **Color_Mood:** Professional blue + pipeline stage colors + closed-won green
- **Typography_Mood:** Professional + Clean hierarchy
- **Key_Effects:** Color shift hover + Fast 150ms transitions + No shadows
- **Decision_Rules:** {"if_ux_focused": "prioritize-clarity", "if_mobile": "optimize-touch-targets"}
- **Anti_Patterns:** Excessive decoration + Complex shadows + 3D effects
- **Severity:** HIGH

#### Inventory & Stock Management

- **No:** 102
- **Recommended_Pattern:** Feature-Rich Showcase
- **Style_Priority:** Flat Design + Minimalism
- **Color_Mood:** Functional neutral + status traffic-light (green/amber/red) + scanner accent
- **Typography_Mood:** Professional + Clean hierarchy
- **Key_Effects:** Color shift hover + Fast 150ms transitions + No shadows
- **Decision_Rules:** {"if_ux_focused": "prioritize-clarity", "if_mobile": "optimize-touch-targets"}
- **Anti_Patterns:** Excessive decoration + Complex shadows + 3D effects
- **Severity:** HIGH

#### Flashcard & Study Tool

- **No:** 103
- **Recommended_Pattern:** Feature-Rich Showcase + Demo
- **Style_Priority:** Claymorphism + Micro-interactions
- **Color_Mood:** Playful primary + correct green + incorrect red + progress blue
- **Typography_Mood:** Playful + Rounded + Friendly
- **Key_Effects:** Multi-layer shadows + Spring bounce + Soft press 200ms
- **Decision_Rules:** {"if_ux_focused": "prioritize-clarity", "if_mobile": "optimize-touch-targets"}
- **Anti_Patterns:** Inconsistent styling + Poor contrast ratios
- **Severity:** HIGH

#### Booking & Appointment App

- **No:** 104
- **Recommended_Pattern:** Conversion-Optimized
- **Style_Priority:** Soft UI Evolution + Flat Design
- **Color_Mood:** Trust blue + available green + booked grey + confirm accent
- **Typography_Mood:** Bold + Clean + Sans-serif
- **Key_Effects:** Color shift hover + Fast 150ms transitions + No shadows
- **Decision_Rules:** {"if_conversion_focused": "add-urgency-colors"}
- **Anti_Patterns:** Complex shadows + 3D effects
- **Severity:** HIGH

#### Invoice & Billing Tool

- **No:** 105
- **Recommended_Pattern:** Conversion-Optimized + Trust
- **Style_Priority:** Minimalism + Flat Design
- **Color_Mood:** Professional navy + paid green + overdue red + neutral grey
- **Typography_Mood:** Professional + Clean hierarchy
- **Key_Effects:** Color shift hover + Fast 150ms transitions + No shadows
- **Decision_Rules:** {"if_conversion_focused": "add-urgency-colors"}
- **Anti_Patterns:** Excessive decoration + Complex shadows + 3D effects
- **Severity:** HIGH

#### Grocery & Shopping List

- **No:** 106
- **Recommended_Pattern:** Minimal & Direct + Demo
- **Style_Priority:** Flat Design + Vibrant & Block-based
- **Color_Mood:** Fresh green + food-category colors + checkmark accent
- **Typography_Mood:** Bold + Clean + Sans-serif
- **Key_Effects:** Color shift hover + Fast 150ms transitions + No shadows
- **Decision_Rules:** {"if_ux_focused": "prioritize-clarity", "if_mobile": "optimize-touch-targets"}
- **Anti_Patterns:** Complex shadows + 3D effects + Muted colors + Low energy
- **Severity:** HIGH

#### Timer & Pomodoro

- **No:** 107
- **Recommended_Pattern:** Minimal & Direct
- **Style_Priority:** Minimalism + Neumorphism
- **Color_Mood:** High-contrast on dark + focus red/amber + break green
- **Typography_Mood:** Professional + Clean hierarchy
- **Key_Effects:** Dual shadows (light+dark) + Soft press 150ms
- **Decision_Rules:** {"if_ux_focused": "prioritize-clarity", "if_mobile": "optimize-touch-targets"}
- **Anti_Patterns:** Excessive decoration
- **Severity:** HIGH

#### Parenting & Baby Tracker

- **No:** 108
- **Recommended_Pattern:** Social Proof-Focused + Trust
- **Style_Priority:** Claymorphism + Soft UI Evolution
- **Color_Mood:** Soft pastels (baby pink/sky blue/mint/peach) + warm accents
- **Typography_Mood:** Playful + Rounded + Friendly
- **Key_Effects:** Multi-layer shadows + Spring bounce + Soft press 200ms
- **Decision_Rules:** {"if_trust_needed": "add-testimonials"}
- **Anti_Patterns:** Inconsistent styling + Poor contrast ratios
- **Severity:** HIGH

#### Scanner & Document Manager

- **No:** 109
- **Recommended_Pattern:** Feature-Rich Showcase + Demo
- **Style_Priority:** Minimalism + Flat Design
- **Color_Mood:** Clean white + camera viewfinder accent + file-type color coding
- **Typography_Mood:** Professional + Clean hierarchy
- **Key_Effects:** Color shift hover + Fast 150ms transitions + No shadows
- **Decision_Rules:** {"if_ux_focused": "prioritize-clarity", "if_mobile": "optimize-touch-targets"}
- **Anti_Patterns:** Excessive decoration + Complex shadows + 3D effects
- **Severity:** HIGH

#### Calendar & Scheduling App

- **No:** 110
- **Recommended_Pattern:** Feature-Rich Showcase + Demo
- **Style_Priority:** Flat Design + Micro-interactions
- **Color_Mood:** Clean blue + event category accent colors + success green
- **Typography_Mood:** Bold + Clean + Sans-serif
- **Key_Effects:** Color shift hover + Fast 150ms transitions + No shadows
- **Decision_Rules:** {"if_ux_focused": "prioritize-clarity", "if_mobile": "optimize-touch-targets"}
- **Anti_Patterns:** Complex shadows + 3D effects
- **Severity:** HIGH

#### Password Manager

- **No:** 111
- **Recommended_Pattern:** Trust & Authority + Feature-Rich
- **Style_Priority:** Minimalism + Accessible & Ethical
- **Color_Mood:** Trust blue + security green + dark neutral
- **Typography_Mood:** Professional + Clean hierarchy
- **Key_Effects:** Subtle hover 200ms + Smooth transitions + Clean
- **Decision_Rules:** {"if_ux_focused": "prioritize-clarity", "if_mobile": "optimize-touch-targets"}
- **Anti_Patterns:** Excessive decoration + Color-only indicators
- **Severity:** HIGH

#### Expense Splitter / Bill Split

- **No:** 112
- **Recommended_Pattern:** Minimal & Direct + Demo
- **Style_Priority:** Flat Design + Vibrant & Block-based
- **Color_Mood:** Success green + alert red + neutral grey + avatar accent colors
- **Typography_Mood:** Bold + Clean + Sans-serif
- **Key_Effects:** Color shift hover + Fast 150ms transitions + No shadows
- **Decision_Rules:** {"if_ux_focused": "prioritize-clarity", "if_mobile": "optimize-touch-targets"}
- **Anti_Patterns:** Complex shadows + 3D effects + Muted colors + Low energy
- **Severity:** HIGH

#### Voice Recorder & Memo

- **No:** 113
- **Recommended_Pattern:** Interactive Product Demo + Minimal
- **Style_Priority:** Minimalism + AI-Native UI
- **Color_Mood:** Clean white + recording red + waveform accent
- **Typography_Mood:** Professional + Clean hierarchy
- **Key_Effects:** Subtle hover 200ms + Smooth transitions + Clean
- **Decision_Rules:** {"if_ux_focused": "prioritize-clarity", "if_mobile": "optimize-touch-targets"}
- **Anti_Patterns:** Excessive decoration
- **Severity:** HIGH

#### Bookmark & Read-Later

- **No:** 114
- **Recommended_Pattern:** Minimal & Direct + Demo
- **Style_Priority:** Minimalism + Flat Design
- **Color_Mood:** Paper warm white + ink neutral + minimal accent + tag colors
- **Typography_Mood:** Professional + Clean hierarchy
- **Key_Effects:** Color shift hover + Fast 150ms transitions + No shadows
- **Decision_Rules:** {"if_ux_focused": "prioritize-clarity", "if_mobile": "optimize-touch-targets"}
- **Anti_Patterns:** Excessive decoration + Complex shadows + 3D effects
- **Severity:** HIGH

#### Translator App

- **No:** 115
- **Recommended_Pattern:** Feature-Rich Showcase + Interactive Demo
- **Style_Priority:** Flat Design + AI-Native UI
- **Color_Mood:** Global blue + neutral grey + language flag accent
- **Typography_Mood:** Bold + Clean + Sans-serif
- **Key_Effects:** Color shift hover + Fast 150ms transitions + No shadows
- **Decision_Rules:** {"if_ux_focused": "prioritize-clarity", "if_mobile": "optimize-touch-targets"}
- **Anti_Patterns:** Complex shadows + 3D effects
- **Severity:** HIGH

#### Calculator & Unit Converter

- **No:** 116
- **Recommended_Pattern:** Minimal & Direct
- **Style_Priority:** Neumorphism + Minimalism
- **Color_Mood:** Dark functional + orange operation keys + clear button hierarchy
- **Typography_Mood:** Professional + Clean hierarchy
- **Key_Effects:** Dual shadows (light+dark) + Soft press 150ms
- **Decision_Rules:** {"if_ux_focused": "prioritize-clarity", "if_mobile": "optimize-touch-targets"}
- **Anti_Patterns:** Excessive decoration
- **Severity:** HIGH

#### Alarm & World Clock

- **No:** 117
- **Recommended_Pattern:** Minimal & Direct
- **Style_Priority:** Dark Mode (OLED) + Minimalism
- **Color_Mood:** Deep dark + ambient glow accent + timezone gradient
- **Typography_Mood:** Professional + Clean hierarchy
- **Key_Effects:** Subtle glow + Neon accents + High contrast
- **Decision_Rules:** {"if_light_mode_needed": "provide-theme-toggle"}
- **Anti_Patterns:** Excessive decoration + Pure white backgrounds
- **Severity:** HIGH

#### File Manager & Transfer

- **No:** 118
- **Recommended_Pattern:** Feature-Rich Showcase + Demo
- **Style_Priority:** Flat Design + Minimalism
- **Color_Mood:** Functional neutral + file type color coding (PDF orange, doc blue, image purple)
- **Typography_Mood:** Professional + Clean hierarchy
- **Key_Effects:** Color shift hover + Fast 150ms transitions + No shadows
- **Decision_Rules:** {"if_ux_focused": "prioritize-clarity", "if_mobile": "optimize-touch-targets"}
- **Anti_Patterns:** Excessive decoration + Complex shadows + 3D effects
- **Severity:** HIGH

#### Email Client

- **No:** 119
- **Recommended_Pattern:** Feature-Rich Showcase + Demo
- **Style_Priority:** Flat Design + Minimalism
- **Color_Mood:** Clean white + brand primary + priority red + snooze amber
- **Typography_Mood:** Professional + Clean hierarchy
- **Key_Effects:** Color shift hover + Fast 150ms transitions + No shadows
- **Decision_Rules:** {"if_ux_focused": "prioritize-clarity", "if_mobile": "optimize-touch-targets"}
- **Anti_Patterns:** Excessive decoration + Complex shadows + 3D effects
- **Severity:** HIGH

#### Casual Puzzle Game

- **No:** 120
- **Recommended_Pattern:** Feature-Rich Showcase + Social Proof
- **Style_Priority:** Claymorphism + Vibrant & Block-based
- **Color_Mood:** Cheerful pastels + progression gradient + reward gold + bright accent
- **Typography_Mood:** Playful + Rounded + Friendly
- **Key_Effects:** Multi-layer shadows + Spring bounce + Soft press 200ms
- **Decision_Rules:** {"if_trust_needed": "add-testimonials"}
- **Anti_Patterns:** Muted colors + Low energy
- **Severity:** HIGH

#### Trivia & Quiz Game

- **No:** 121
- **Recommended_Pattern:** Feature-Rich Showcase + Social Proof
- **Style_Priority:** Vibrant & Block-based + Micro-interactions
- **Color_Mood:** Energetic blue + correct green + incorrect red + leaderboard gold
- **Typography_Mood:** Energetic + Bold + Large
- **Key_Effects:** Haptic feedback + Small 50-100ms animations
- **Decision_Rules:** {"if_trust_needed": "add-testimonials"}
- **Anti_Patterns:** Muted colors + Low energy
- **Severity:** HIGH

#### Card & Board Game

- **No:** 122
- **Recommended_Pattern:** Feature-Rich Showcase
- **Style_Priority:** 3D & Hyperrealism + Flat Design
- **Color_Mood:** Game-theme felt green + dark wood + card back patterns
- **Typography_Mood:** Bold + Clean + Sans-serif
- **Key_Effects:** Color shift hover + Fast 150ms transitions + No shadows
- **Decision_Rules:** {"if_ux_focused": "prioritize-clarity", "if_mobile": "optimize-touch-targets"}
- **Anti_Patterns:** Complex shadows + 3D effects
- **Severity:** HIGH

#### Idle & Clicker Game

- **No:** 123
- **Recommended_Pattern:** Feature-Rich Showcase
- **Style_Priority:** Vibrant & Block-based + Motion-Driven
- **Color_Mood:** Coin gold + upgrade blue + prestige purple + progress green
- **Typography_Mood:** Energetic + Bold + Large
- **Key_Effects:** Scroll animations + Parallax + Page transitions
- **Decision_Rules:** {"if_ux_focused": "prioritize-clarity", "if_mobile": "optimize-touch-targets"}
- **Anti_Patterns:** Muted colors + Low energy
- **Severity:** HIGH

#### Word & Crossword Game

- **No:** 124
- **Recommended_Pattern:** Minimal & Direct + Demo
- **Style_Priority:** Minimalism + Flat Design
- **Color_Mood:** Clean white + warm letter tiles + success green + shake red
- **Typography_Mood:** Professional + Clean hierarchy
- **Key_Effects:** Color shift hover + Fast 150ms transitions + No shadows
- **Decision_Rules:** {"if_ux_focused": "prioritize-clarity", "if_mobile": "optimize-touch-targets"}
- **Anti_Patterns:** Excessive decoration + Complex shadows + 3D effects
- **Severity:** HIGH

#### Arcade & Retro Game

- **No:** 125
- **Recommended_Pattern:** Feature-Rich Showcase + Hero-Centric
- **Style_Priority:** Pixel Art + Retro-Futurism
- **Color_Mood:** Neon on black + pixel palette + score gold + danger red
- **Typography_Mood:** Nostalgic + Monospace + Neon
- **Key_Effects:** Subtle hover (200ms) + Smooth transitions
- **Decision_Rules:** {"if_ux_focused": "prioritize-clarity", "if_mobile": "optimize-touch-targets"}
- **Anti_Patterns:** Inconsistent styling + Poor contrast ratios
- **Severity:** HIGH

#### Photo Editor & Filters

- **No:** 126
- **Recommended_Pattern:** Feature-Rich Showcase + Interactive Demo
- **Style_Priority:** Minimalism + Dark Mode (OLED)
- **Color_Mood:** Dark editor background + vibrant filter preview strip + tool icon accent
- **Typography_Mood:** Professional + Clean hierarchy
- **Key_Effects:** Subtle glow + Neon accents + High contrast
- **Decision_Rules:** {"if_light_mode_needed": "provide-theme-toggle"}
- **Anti_Patterns:** Excessive decoration + Pure white backgrounds
- **Severity:** HIGH

#### Short Video Editor

- **No:** 127
- **Recommended_Pattern:** Feature-Rich Showcase + Hero-Centric
- **Style_Priority:** Dark Mode (OLED) + Motion-Driven
- **Color_Mood:** Dark background + timeline track accent colors + effect preview vivid
- **Typography_Mood:** High contrast + Light on dark
- **Key_Effects:** Subtle glow + Neon accents + High contrast
- **Decision_Rules:** {"if_light_mode_needed": "provide-theme-toggle"}
- **Anti_Patterns:** Pure white backgrounds
- **Severity:** HIGH

#### Drawing & Sketching Canvas

- **No:** 128
- **Recommended_Pattern:** Interactive Product Demo + Storytelling
- **Style_Priority:** Minimalism + Dark Mode (OLED)
- **Color_Mood:** Neutral canvas + full-spectrum color picker + tool panel dark
- **Typography_Mood:** Professional + Clean hierarchy
- **Key_Effects:** Subtle glow + Neon accents + High contrast
- **Decision_Rules:** {"if_light_mode_needed": "provide-theme-toggle"}
- **Anti_Patterns:** Excessive decoration + Pure white backgrounds
- **Severity:** HIGH

#### Music Creation & Beat Maker

- **No:** 129
- **Recommended_Pattern:** Interactive Product Demo + Storytelling
- **Style_Priority:** Dark Mode (OLED) + Motion-Driven
- **Color_Mood:** Dark studio background + track colors rainbow + waveform accent + BPM pulse
- **Typography_Mood:** High contrast + Light on dark
- **Key_Effects:** Subtle glow + Neon accents + High contrast
- **Decision_Rules:** {"if_light_mode_needed": "provide-theme-toggle"}
- **Anti_Patterns:** Pure white backgrounds
- **Severity:** HIGH

#### Meme & Sticker Maker

- **No:** 130
- **Recommended_Pattern:** Feature-Rich Showcase + Social Proof
- **Style_Priority:** Vibrant & Block-based + Flat Design
- **Color_Mood:** Bold primary + comedic yellow + viral red + high saturation accent
- **Typography_Mood:** Bold + Clean + Sans-serif
- **Key_Effects:** Color shift hover + Fast 150ms transitions + No shadows
- **Decision_Rules:** {"if_trust_needed": "add-testimonials"}
- **Anti_Patterns:** Complex shadows + 3D effects + Muted colors + Low energy
- **Severity:** HIGH

#### AI Photo & Avatar Generator

- **No:** 131
- **Recommended_Pattern:** Feature-Rich Showcase + Social Proof
- **Style_Priority:** AI-Native UI + Aurora UI
- **Color_Mood:** AI purple + aurora gradients + before/after neutral
- **Typography_Mood:** Elegant + Gradient-friendly
- **Key_Effects:** Flowing gradients 8-12s + Color morphing
- **Decision_Rules:** {"if_trust_needed": "add-testimonials"}
- **Anti_Patterns:** Inconsistent styling + Poor contrast ratios
- **Severity:** HIGH

#### Link-in-Bio Page Builder

- **No:** 132
- **Recommended_Pattern:** Conversion-Optimized + Social Proof
- **Style_Priority:** Vibrant & Block-based + Bento Box Grid
- **Color_Mood:** Brand-customizable + accent link color + clean white canvas
- **Typography_Mood:** Energetic + Bold + Large
- **Key_Effects:** Large section gaps 48px+ + Color shift hover + Scroll-snap
- **Decision_Rules:** {"if_conversion_focused": "add-urgency-colors", "if_trust_needed": "add-testimonials"}
- **Anti_Patterns:** Muted colors + Low energy
- **Severity:** HIGH

#### Wardrobe & Outfit Planner

- **No:** 133
- **Recommended_Pattern:** Storytelling-Driven + Feature-Rich
- **Style_Priority:** Minimalism + Motion-Driven
- **Color_Mood:** Clean fashion neutral + full clothes color palette + accent
- **Typography_Mood:** Professional + Clean hierarchy
- **Key_Effects:** Subtle hover 200ms + Smooth transitions + Clean
- **Decision_Rules:** {"if_ux_focused": "prioritize-clarity", "if_mobile": "optimize-touch-targets"}
- **Anti_Patterns:** Excessive decoration
- **Severity:** HIGH

#### Plant Care Tracker

- **No:** 134
- **Recommended_Pattern:** Storytelling-Driven + Social Proof
- **Style_Priority:** Organic Biophilic + Soft UI Evolution
- **Color_Mood:** Nature greens + earth brown + sunny yellow reminder + water blue
- **Typography_Mood:** Warm + Humanist + Natural
- **Key_Effects:** Rounded 16-24px + Natural shadows + Flowing SVG
- **Decision_Rules:** {"if_trust_needed": "add-testimonials"}
- **Anti_Patterns:** Inconsistent styling + Poor contrast ratios
- **Severity:** HIGH

#### Book & Reading Tracker

- **No:** 135
- **Recommended_Pattern:** Social Proof-Focused + Feature-Rich
- **Style_Priority:** Swiss Modernism 2.0 + Minimalism
- **Color_Mood:** Warm paper white + ink brown + reading progress green + book cover colors
- **Typography_Mood:** Professional + Clean hierarchy
- **Key_Effects:** Subtle hover 200ms + Smooth transitions + Clean
- **Decision_Rules:** {"if_trust_needed": "add-testimonials"}
- **Anti_Patterns:** Excessive decoration
- **Severity:** HIGH

#### Couple & Relationship App

- **No:** 136
- **Recommended_Pattern:** Storytelling-Driven + Social Proof
- **Style_Priority:** Aurora UI + Soft UI Evolution
- **Color_Mood:** Warm romantic pink/rose + soft gradient + memory photo tones
- **Typography_Mood:** Elegant + Gradient-friendly
- **Key_Effects:** Flowing gradients 8-12s + Color morphing
- **Decision_Rules:** {"if_trust_needed": "add-testimonials"}
- **Anti_Patterns:** Inconsistent styling + Poor contrast ratios
- **Severity:** HIGH

#### Family Calendar & Chores

- **No:** 137
- **Recommended_Pattern:** Feature-Rich Showcase + Social Proof
- **Style_Priority:** Flat Design + Claymorphism
- **Color_Mood:** Warm playful + member color coding + chore completion green
- **Typography_Mood:** Playful + Rounded + Friendly
- **Key_Effects:** Multi-layer shadows + Spring bounce + Soft press 200ms
- **Decision_Rules:** {"if_trust_needed": "add-testimonials"}
- **Anti_Patterns:** Complex shadows + 3D effects
- **Severity:** HIGH

#### Mood Tracker

- **No:** 138
- **Recommended_Pattern:** Storytelling-Driven + Social Proof
- **Style_Priority:** Soft UI Evolution + Minimalism
- **Color_Mood:** Emotion gradient (blue sad to yellow happy) + pastel per mood + insight accent
- **Typography_Mood:** Professional + Clean hierarchy
- **Key_Effects:** Subtle hover 200ms + Smooth transitions + Clean
- **Decision_Rules:** {"if_trust_needed": "add-testimonials"}
- **Anti_Patterns:** Excessive decoration
- **Severity:** HIGH

#### Gift & Wishlist

- **No:** 139
- **Recommended_Pattern:** Minimal & Direct + Conversion
- **Style_Priority:** Vibrant & Block-based + Soft UI Evolution
- **Color_Mood:** Celebration warm pink/gold/red + category colors + surprise accent
- **Typography_Mood:** Energetic + Bold + Large
- **Key_Effects:** Large section gaps 48px+ + Color shift hover + Scroll-snap
- **Decision_Rules:** {"if_conversion_focused": "add-urgency-colors"}
- **Anti_Patterns:** Muted colors + Low energy
- **Severity:** HIGH

#### Running & Cycling GPS

- **No:** 140
- **Recommended_Pattern:** Feature-Rich Showcase + Social Proof
- **Style_Priority:** Dark Mode (OLED) + Vibrant & Block-based
- **Color_Mood:** Energetic orange + map accent + pace zones (green/yellow/red)
- **Typography_Mood:** High contrast + Light on dark
- **Key_Effects:** Subtle glow + Neon accents + High contrast
- **Decision_Rules:** {"if_light_mode_needed": "provide-theme-toggle", "if_trust_needed": "add-testimonials"}
- **Anti_Patterns:** Pure white backgrounds + Muted colors + Low energy
- **Severity:** HIGH

#### Yoga & Stretching Guide

- **No:** 141
- **Recommended_Pattern:** Storytelling-Driven + Social Proof
- **Style_Priority:** Organic Biophilic + Soft UI Evolution
- **Color_Mood:** Earth calming sage/terracotta/cream + breathing gradient + warm accent
- **Typography_Mood:** Warm + Humanist + Natural
- **Key_Effects:** Rounded 16-24px + Natural shadows + Flowing SVG
- **Decision_Rules:** {"if_trust_needed": "add-testimonials"}
- **Anti_Patterns:** Inconsistent styling + Poor contrast ratios
- **Severity:** HIGH

#### Sleep Tracker

- **No:** 142
- **Recommended_Pattern:** Feature-Rich Showcase + Social Proof
- **Style_Priority:** Dark Mode (OLED) + Neumorphism
- **Color_Mood:** Deep midnight blue + stars/moon accent + sleep quality gradient (poor red to great green)
- **Typography_Mood:** High contrast + Light on dark
- **Key_Effects:** Dual shadows (light+dark) + Soft press 150ms
- **Decision_Rules:** {"if_light_mode_needed": "provide-theme-toggle", "if_trust_needed": "add-testimonials"}
- **Anti_Patterns:** Pure white backgrounds
- **Severity:** HIGH

#### Calorie & Nutrition Counter

- **No:** 143
- **Recommended_Pattern:** Feature-Rich Showcase + Social Proof
- **Style_Priority:** Flat Design + Vibrant & Block-based
- **Color_Mood:** Healthy green + macro colors (protein blue, carb orange, fat yellow) + progress circle
- **Typography_Mood:** Bold + Clean + Sans-serif
- **Key_Effects:** Color shift hover + Fast 150ms transitions + No shadows
- **Decision_Rules:** {"if_trust_needed": "add-testimonials"}
- **Anti_Patterns:** Complex shadows + 3D effects + Muted colors + Low energy
- **Severity:** HIGH

#### Period & Cycle Tracker

- **No:** 144
- **Recommended_Pattern:** Social Proof-Focused + Trust
- **Style_Priority:** Soft UI Evolution + Aurora UI
- **Color_Mood:** Rose/blush + lavender + fertility green + soft calendar tones
- **Typography_Mood:** Elegant + Gradient-friendly
- **Key_Effects:** Flowing gradients 8-12s + Color morphing
- **Decision_Rules:** {"if_trust_needed": "add-testimonials"}
- **Anti_Patterns:** Inconsistent styling + Poor contrast ratios
- **Severity:** HIGH

#### Medication & Pill Reminder

- **No:** 145
- **Recommended_Pattern:** Trust & Authority + Feature-Rich
- **Style_Priority:** Accessible & Ethical + Flat Design
- **Color_Mood:** Medical trust blue + missed alert red + taken green + clean white
- **Typography_Mood:** Bold + Clean + Sans-serif
- **Key_Effects:** Color shift hover + Fast 150ms transitions + No shadows
- **Decision_Rules:** {"if_ux_focused": "prioritize-clarity", "if_mobile": "optimize-touch-targets"}
- **Anti_Patterns:** Complex shadows + 3D effects + Color-only indicators
- **Severity:** HIGH

#### Water & Hydration Reminder

- **No:** 146
- **Recommended_Pattern:** Minimal & Direct + Demo
- **Style_Priority:** Claymorphism + Vibrant & Block-based
- **Color_Mood:** Refreshing blue + water wave animation + goal progress accent
- **Typography_Mood:** Playful + Rounded + Friendly
- **Key_Effects:** Multi-layer shadows + Spring bounce + Soft press 200ms
- **Decision_Rules:** {"if_ux_focused": "prioritize-clarity", "if_mobile": "optimize-touch-targets"}
- **Anti_Patterns:** Muted colors + Low energy
- **Severity:** HIGH

#### Fasting & Intermittent Timer

- **No:** 147
- **Recommended_Pattern:** Feature-Rich Showcase + Social Proof
- **Style_Priority:** Minimalism + Dark Mode (OLED)
- **Color_Mood:** Fasting deep blue/purple + eating window green + timeline neutral
- **Typography_Mood:** Professional + Clean hierarchy
- **Key_Effects:** Subtle glow + Neon accents + High contrast
- **Decision_Rules:** {"if_light_mode_needed": "provide-theme-toggle", "if_trust_needed": "add-testimonials"}
- **Anti_Patterns:** Excessive decoration + Pure white backgrounds
- **Severity:** HIGH

#### Anonymous Community / Confession

- **No:** 148
- **Recommended_Pattern:** Social Proof-Focused + Feature-Rich
- **Style_Priority:** Dark Mode (OLED) + Minimalism
- **Color_Mood:** Dark protective + subtle gradient + upvote green + empathy warm accent
- **Typography_Mood:** Professional + Clean hierarchy
- **Key_Effects:** Subtle glow + Neon accents + High contrast
- **Decision_Rules:** {"if_light_mode_needed": "provide-theme-toggle", "if_trust_needed": "add-testimonials"}
- **Anti_Patterns:** Excessive decoration + Pure white backgrounds
- **Severity:** HIGH

#### Local Events & Discovery

- **No:** 149
- **Recommended_Pattern:** Hero-Centric Design + Feature-Rich
- **Style_Priority:** Vibrant & Block-based + Motion-Driven
- **Color_Mood:** City vibrant + event category colors + map accent + date highlight
- **Typography_Mood:** Energetic + Bold + Large
- **Key_Effects:** Scroll animations + Parallax + Page transitions
- **Decision_Rules:** {"if_ux_focused": "prioritize-clarity", "if_mobile": "optimize-touch-targets"}
- **Anti_Patterns:** Muted colors + Low energy
- **Severity:** HIGH

#### Study Together / Virtual Coworking

- **No:** 150
- **Recommended_Pattern:** Social Proof-Focused + Feature-Rich
- **Style_Priority:** Minimalism + Soft UI Evolution
- **Color_Mood:** Calm focus blue + session progress indicator + ambient warm neutrals
- **Typography_Mood:** Professional + Clean hierarchy
- **Key_Effects:** Subtle hover 200ms + Smooth transitions + Clean
- **Decision_Rules:** {"if_trust_needed": "add-testimonials"}
- **Anti_Patterns:** Excessive decoration
- **Severity:** HIGH

#### Coding Challenge & Practice

- **No:** 151
- **Recommended_Pattern:** Feature-Rich Showcase + Social Proof
- **Style_Priority:** Dark Mode (OLED) + Cyberpunk UI
- **Color_Mood:** Code editor dark + success green + difficulty gradient (easy green / medium amber / hard red)
- **Typography_Mood:** High contrast + Light on dark
- **Key_Effects:** Subtle glow + Neon accents + High contrast
- **Decision_Rules:** {"if_light_mode_needed": "provide-theme-toggle", "if_trust_needed": "add-testimonials"}
- **Anti_Patterns:** Pure white backgrounds
- **Severity:** HIGH

#### Kids Learning (ABC & Math)

- **No:** 152
- **Recommended_Pattern:** Social Proof-Focused + Trust
- **Style_Priority:** Claymorphism + Vibrant & Block-based
- **Color_Mood:** Bright primary + child-safe pastels + reward gold + interactive accent
- **Typography_Mood:** Playful + Rounded + Friendly
- **Key_Effects:** Multi-layer shadows + Spring bounce + Soft press 200ms
- **Decision_Rules:** {"if_trust_needed": "add-testimonials"}
- **Anti_Patterns:** Muted colors + Low energy
- **Severity:** HIGH

#### Music Instrument Learning

- **No:** 153
- **Recommended_Pattern:** Interactive Product Demo + Social Proof
- **Style_Priority:** Vibrant & Block-based + Motion-Driven
- **Color_Mood:** Musical warm deep red/brown + note color system + skill progress bar
- **Typography_Mood:** Energetic + Bold + Large
- **Key_Effects:** Scroll animations + Parallax + Page transitions
- **Decision_Rules:** {"if_trust_needed": "add-testimonials"}
- **Anti_Patterns:** Muted colors + Low energy
- **Severity:** HIGH

#### Parking Finder

- **No:** 154
- **Recommended_Pattern:** Conversion-Optimized + Feature-Rich
- **Style_Priority:** Minimalism + Glassmorphism
- **Color_Mood:** Trust blue + available green + occupied red + map neutral
- **Typography_Mood:** Professional + Clean hierarchy
- **Key_Effects:** Backdrop blur (10-20px) + Translucent overlays
- **Decision_Rules:** {"if_low_performance": "fallback-to-flat", "if_conversion_focused": "add-urgency-colors"}
- **Anti_Patterns:** Excessive decoration
- **Severity:** HIGH

#### Public Transit Guide

- **No:** 155
- **Recommended_Pattern:** Feature-Rich Showcase + Interactive Demo
- **Style_Priority:** Flat Design + Accessible & Ethical
- **Color_Mood:** Transit brand line colors + real-time indicator green/red + map neutral
- **Typography_Mood:** Bold + Clean + Sans-serif
- **Key_Effects:** Color shift hover + Fast 150ms transitions + No shadows
- **Decision_Rules:** {"if_ux_focused": "prioritize-clarity", "if_mobile": "optimize-touch-targets"}
- **Anti_Patterns:** Complex shadows + 3D effects + Color-only indicators
- **Severity:** HIGH

#### Road Trip Planner

- **No:** 156
- **Recommended_Pattern:** Storytelling-Driven + Hero-Centric
- **Style_Priority:** Aurora UI + Organic Biophilic
- **Color_Mood:** Adventure warm sunset orange + map teal + stop markers + road neutral
- **Typography_Mood:** Elegant + Gradient-friendly
- **Key_Effects:** Flowing gradients 8-12s + Color morphing
- **Decision_Rules:** {"if_ux_focused": "prioritize-clarity", "if_mobile": "optimize-touch-targets"}
- **Anti_Patterns:** Inconsistent styling + Poor contrast ratios
- **Severity:** HIGH

#### VPN & Privacy Tool

- **No:** 157
- **Recommended_Pattern:** Trust & Authority + Conversion-Optimized
- **Style_Priority:** Minimalism + Dark Mode (OLED)
- **Color_Mood:** Dark shield blue + connected green + disconnected red + trust accent
- **Typography_Mood:** Professional + Clean hierarchy
- **Key_Effects:** Subtle glow + Neon accents + High contrast
- **Decision_Rules:** {"if_light_mode_needed": "provide-theme-toggle", "if_conversion_focused": "add-urgency-colors"}
- **Anti_Patterns:** Excessive decoration + Pure white backgrounds
- **Severity:** HIGH

#### Emergency SOS & Safety

- **No:** 158
- **Recommended_Pattern:** Trust & Authority + Social Proof
- **Style_Priority:** Accessible & Ethical + Flat Design
- **Color_Mood:** Alert red + safety blue + location green + high contrast critical
- **Typography_Mood:** Bold + Clean + Sans-serif
- **Key_Effects:** Color shift hover + Fast 150ms transitions + No shadows
- **Decision_Rules:** {"if_trust_needed": "add-testimonials"}
- **Anti_Patterns:** Complex shadows + 3D effects + Color-only indicators
- **Severity:** HIGH

#### Wallpaper & Theme App

- **No:** 159
- **Recommended_Pattern:** Feature-Rich Showcase + Social Proof
- **Style_Priority:** Vibrant & Block-based + Aurora UI
- **Color_Mood:** Content-driven + trending aesthetic palettes + download accent
- **Typography_Mood:** Energetic + Bold + Large
- **Key_Effects:** Large section gaps 48px+ + Color shift hover + Scroll-snap
- **Decision_Rules:** {"if_trust_needed": "add-testimonials"}
- **Anti_Patterns:** Muted colors + Low energy
- **Severity:** HIGH

#### White Noise & Ambient Sound

- **No:** 160
- **Recommended_Pattern:** Minimal & Direct + Social Proof
- **Style_Priority:** Minimalism + Dark Mode (OLED)
- **Color_Mood:** Calming dark + ambient texture visual + subtle sound wave + sleep blue
- **Typography_Mood:** Professional + Clean hierarchy
- **Key_Effects:** Subtle glow + Neon accents + High contrast
- **Decision_Rules:** {"if_light_mode_needed": "provide-theme-toggle", "if_trust_needed": "add-testimonials"}
- **Anti_Patterns:** Excessive decoration + Pure white backgrounds
- **Severity:** HIGH

#### Home Decoration & Interior Design

- **No:** 161
- **Recommended_Pattern:** Storytelling-Driven + Feature-Rich
- **Style_Priority:** Minimalism + 3D Product Preview
- **Color_Mood:** Neutral interior palette + material texture accent + AR blue
- **Typography_Mood:** Professional + Clean hierarchy
- **Key_Effects:** Subtle hover 200ms + Smooth transitions + Clean
- **Decision_Rules:** {"if_ux_focused": "prioritize-clarity", "if_mobile": "optimize-touch-targets"}
- **Anti_Patterns:** Excessive decoration
- **Severity:** HIGH

