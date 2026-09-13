import { PrismaClient } from "@prisma/client";
import bcrypt from "bcryptjs";

const prisma = new PrismaClient();

function rand(min: number, max: number) {
  return Math.random() * (max - min) + min;
}

function randInt(min: number, max: number) {
  return Math.floor(rand(min, max));
}

function pick<T>(arr: T[]): T {
  return arr[Math.floor(Math.random() * arr.length)];
}

// --- Creative Analysis Templates ---
const analysisTemplates = [
  // High-performing UGC
  {
    assetType: "UGC_TALKING_HEAD" as const,
    messagingAngle: "PROBLEM_SOLUTION" as const,
    hookTactic: "QUESTION" as const,
    visualStyle: "RAW_AUTHENTIC" as const,
    ctaStyle: "SHOP_NOW" as const,
    emotionalTone: "EMPATHETIC" as const,
    productPresentation: "IN_USE" as const,
    aiSummary: "Authentic UGC talking head format where creator addresses common skincare frustration before showing product as solution. Raw, relatable feel builds trust.",
    aiStrengths: ["Authentic creator voice builds trust", "Clear problem-solution narrative", "Strong emotional hook in first 3 seconds"],
    aiWeaknesses: ["Audio quality could be improved", "CTA could be more prominent"],
    aiIterationIdeas: [
      { idea: "Test with a before/after visual in the first 3 seconds", reasoning: "Before/after visuals are proven to increase hook rate by 15-25%", priority: "HIGH", estimatedImpact: "Hook Rate" },
      { idea: "Add text overlay summarizing key benefit", reasoning: "Many users watch without sound; text overlay captures silent scrollers", priority: "MEDIUM", estimatedImpact: "CTR" },
      { idea: "Test different creators with same script", reasoning: "Creator-audience fit is a major performance variable", priority: "HIGH", estimatedImpact: "ROAS" },
    ],
  },
  {
    assetType: "UGC_TESTIMONIAL" as const,
    messagingAngle: "SOCIAL_PROOF" as const,
    hookTactic: "TESTIMONIAL_LEAD" as const,
    visualStyle: "RAW_AUTHENTIC" as const,
    ctaStyle: "SOFT_CTA" as const,
    emotionalTone: "CONFIDENT" as const,
    productPresentation: "RESULT_FOCUS" as const,
    aiSummary: "Customer testimonial highlighting dramatic skin transformation results. Social proof-heavy approach with genuine enthusiasm that feels native to the platform.",
    aiStrengths: ["Genuine customer enthusiasm is compelling", "Results-focused messaging drives action", "Platform-native feel reduces ad blindness"],
    aiWeaknesses: ["Could include more specific details about the product", "No urgency element to drive immediate action"],
    aiIterationIdeas: [
      { idea: "Add a limited-time discount code at the end", reasoning: "Urgency element can increase conversion rate by 20-30%", priority: "HIGH", estimatedImpact: "ROAS" },
      { idea: "Test starting with the most dramatic before/after moment", reasoning: "Leading with the payoff creates stronger hook", priority: "MEDIUM", estimatedImpact: "Hook Rate" },
    ],
  },
  {
    assetType: "STUDIO_PRODUCT_SHOT" as const,
    messagingAngle: "FEATURE_BENEFIT" as const,
    hookTactic: "PRODUCT_IN_ACTION" as const,
    visualStyle: "POLISHED_STUDIO" as const,
    ctaStyle: "DIRECT_HARD_SELL" as const,
    emotionalTone: "CONFIDENT" as const,
    productPresentation: "HERO_SHOT" as const,
    aiSummary: "Clean, polished studio product shot with ingredient callouts and benefit badges. Professional feel positions brand as premium but may lack authenticity for TOF.",
    aiStrengths: ["High production value signals quality", "Clean design makes information scannable", "Strong brand consistency"],
    aiWeaknesses: ["May feel too 'ad-like' for cold audiences", "Lacks human element for emotional connection", "No social proof element"],
    aiIterationIdeas: [
      { idea: "Test a hybrid version with UGC creator holding the product in studio setting", reasoning: "Combines credibility of production with authenticity of UGC", priority: "HIGH", estimatedImpact: "CTR" },
      { idea: "Add customer review quotes as text overlays", reasoning: "Social proof in studio content can bridge the trust gap", priority: "MEDIUM", estimatedImpact: "ROAS" },
    ],
  },
  {
    assetType: "UGC_UNBOXING" as const,
    messagingAngle: "CURIOSITY" as const,
    hookTactic: "UNBOXING_REVEAL" as const,
    visualStyle: "BRIGHT_COLORFUL" as const,
    ctaStyle: "SHOP_NOW" as const,
    emotionalTone: "EXCITING" as const,
    productPresentation: "UNBOXING" as const,
    aiSummary: "Energetic unboxing video creating anticipation and excitement around the product reveal. ASMR elements with packaging sounds add sensory appeal.",
    aiStrengths: ["Unboxing format naturally builds anticipation", "Packaging shown adds premium perception", "Creator excitement is contagious"],
    aiWeaknesses: ["Takes too long to show the product", "Doesn't address specific skin concerns"],
    aiIterationIdeas: [
      { idea: "Speed up the unboxing to show product within 3 seconds", reasoning: "Faster reveal improves hook rate and reduces scroll-away", priority: "HIGH", estimatedImpact: "Hook Rate" },
      { idea: "Add text hook: 'This changed my skin in 2 weeks'", reasoning: "Outcome-based text hooks outperform generic unboxing intros", priority: "HIGH", estimatedImpact: "CTR" },
    ],
  },
  {
    assetType: "GRAPHIC_DESIGN" as const,
    messagingAngle: "PRICE_VALUE" as const,
    hookTactic: "BOLD_CLAIM" as const,
    visualStyle: "TEXT_HEAVY" as const,
    ctaStyle: "LIMITED_TIME" as const,
    emotionalTone: "URGENT" as const,
    productPresentation: "HERO_SHOT" as const,
    aiSummary: "Bold graphic design ad leading with a promotional offer. Heavy text overlay with price callout and urgency timer. Direct response approach optimized for BOF remarketing.",
    aiStrengths: ["Clear value proposition immediately visible", "Urgency element drives action", "Clean layout hierarchy guides eye"],
    aiWeaknesses: ["Heavy text may perform poorly at TOF", "No social proof or testimonials", "Could feel spammy in some contexts"],
    aiIterationIdeas: [
      { idea: "Test with a customer photo background instead of solid color", reasoning: "Adding human element to promotional graphics increases engagement 15-20%", priority: "MEDIUM", estimatedImpact: "CTR" },
      { idea: "A/B test the discount percentage vs dollar amount framing", reasoning: "Different price frames resonate with different audience segments", priority: "LOW", estimatedImpact: "ROAS" },
    ],
  },
  {
    assetType: "BEFORE_AFTER" as const,
    messagingAngle: "TRANSFORMATION" as const,
    hookTactic: "BEFORE_AFTER_VISUAL" as const,
    visualStyle: "BRIGHT_COLORFUL" as const,
    ctaStyle: "SHOP_NOW" as const,
    emotionalTone: "INSPIRATIONAL" as const,
    productPresentation: "RESULT_FOCUS" as const,
    aiSummary: "Powerful before/after transformation ad showing clear visible results. Side-by-side comparison creates instant understanding of product efficacy. Strong conversion driver.",
    aiStrengths: ["Visual proof of results is highly persuasive", "Instant comprehension without reading", "Strong emotional impact"],
    aiWeaknesses: ["May face ad policy scrutiny", "Limited audience diversity in example"],
    aiIterationIdeas: [
      { idea: "Add timeline text: 'Week 1 vs Week 4'", reasoning: "Timeline context makes results feel more achievable and realistic", priority: "MEDIUM", estimatedImpact: "CTR" },
      { idea: "Create a carousel with multiple before/afters from different users", reasoning: "Multiple transformations provide stronger social proof", priority: "HIGH", estimatedImpact: "ROAS" },
    ],
  },
  {
    assetType: "UGC_LIFESTYLE" as const,
    messagingAngle: "LIFESTYLE" as const,
    hookTactic: "RELATABLE_MOMENT" as const,
    visualStyle: "LIFESTYLE_ASPIRATIONAL" as const,
    ctaStyle: "SOFT_CTA" as const,
    emotionalTone: "CALM" as const,
    productPresentation: "LIFESTYLE_CONTEXT" as const,
    aiSummary: "Aspirational lifestyle content showing the product seamlessly integrated into a desirable daily routine. Calm, elevated aesthetics appeal to the target demographic.",
    aiStrengths: ["Aspirational content resonates with target demo", "Product integration feels natural not forced", "High rewatch potential"],
    aiWeaknesses: ["Soft sell approach may not drive immediate conversions", "Product features not highlighted"],
    aiIterationIdeas: [
      { idea: "Add a text overlay with the key product benefit", reasoning: "Combining lifestyle with benefit callout balances brand and performance", priority: "HIGH", estimatedImpact: "ROAS" },
      { idea: "Test a version that ends with a direct CTA card", reasoning: "Adding clear next-step can improve click-through without sacrificing aesthetic", priority: "MEDIUM", estimatedImpact: "CTR" },
    ],
  },
  {
    assetType: "FOUNDER_STORY" as const,
    messagingAngle: "AUTHORITY" as const,
    hookTactic: "BOLD_CLAIM" as const,
    visualStyle: "MINIMAL_CLEAN" as const,
    ctaStyle: "LEARN_MORE" as const,
    emotionalTone: "CONFIDENT" as const,
    productPresentation: "INGREDIENT_FOCUS" as const,
    aiSummary: "Founder-led content explaining the science behind the formulation. Authority-building approach with educational value creates trust and positions brand as expert.",
    aiStrengths: ["Founder credibility builds brand trust", "Educational content provides value", "Science-backed claims differentiate from competitors"],
    aiWeaknesses: ["May be too long for TOF attention spans", "Could feel overly technical for some audiences"],
    aiIterationIdeas: [
      { idea: "Create a 15-second cut with the most compelling soundbite", reasoning: "Shorter versions perform better at TOF while full version works for retargeting", priority: "HIGH", estimatedImpact: "Hook Rate" },
      { idea: "Add customer result photos while founder speaks", reasoning: "Combining authority with social proof creates powerful dual persuasion", priority: "MEDIUM", estimatedImpact: "ROAS" },
    ],
  },
  {
    assetType: "MEME" as const,
    messagingAngle: "CONTRARIAN" as const,
    hookTactic: "CONTROVERSY" as const,
    visualStyle: "MEME_NATIVE" as const,
    ctaStyle: "NO_CTA" as const,
    emotionalTone: "HUMOROUS" as const,
    productPresentation: "MINIMAL_PRODUCT" as const,
    aiSummary: "Platform-native meme format using humor and contrarian positioning to stop the scroll. Low production value is intentional — feels like organic content rather than an ad.",
    aiStrengths: ["Extremely high scroll-stop potential", "Native format bypasses ad blindness", "Highly shareable content"],
    aiWeaknesses: ["Brand association may be weak", "Humor doesn't work for everyone", "No clear conversion path"],
    aiIterationIdeas: [
      { idea: "Create a carousel: meme on slide 1, product pitch on slide 2-3", reasoning: "Meme hook + product sell combo captures attention then converts", priority: "HIGH", estimatedImpact: "ROAS" },
      { idea: "Test 5 different meme variations with same messaging", reasoning: "Meme performance is highly variable; volume testing finds winners", priority: "MEDIUM", estimatedImpact: "CTR" },
    ],
  },
  {
    assetType: "SPLIT_SCREEN" as const,
    messagingAngle: "COMPARISON" as const,
    hookTactic: "PATTERN_INTERRUPT" as const,
    visualStyle: "SPLIT_SCREEN" as const,
    ctaStyle: "DIRECT_HARD_SELL" as const,
    emotionalTone: "CONFIDENT" as const,
    productPresentation: "COMPARISON" as const,
    aiSummary: "Split-screen comparison between the product and competitors/alternatives. Visual side-by-side format makes the value proposition immediately clear and drives consideration.",
    aiStrengths: ["Comparison format creates instant clarity", "Visual contrast is compelling", "Addresses competitive objections proactively"],
    aiWeaknesses: ["Could trigger competitor awareness", "May need careful compliance review"],
    aiIterationIdeas: [
      { idea: "Test 'Your current routine vs. this' framing instead of naming competitors", reasoning: "Generic comparison avoids trademark issues while maintaining effectiveness", priority: "MEDIUM", estimatedImpact: "CTR" },
      { idea: "Add price comparison element", reasoning: "Cost savings angle combined with visual comparison strengthens value proposition", priority: "LOW", estimatedImpact: "ROAS" },
    ],
  },
];

// --- Ad Name Templates ---
const adNamePrefixes = [
  "GlowSkin", "VS", "GS", "Glow"
];

const adNameFormats = [
  "{prefix} - {type} - {angle} - V{n}",
  "{prefix} | {creator} | {angle} | {date}",
  "{prefix} - {type} - {hook} #{n}",
  "{date} - {prefix} - {type} - {angle}",
];

const creatorNames = [
  "Sarah K.", "Mike R.", "Emma L.", "Jason T.", "Nina P.",
  "Alex W.", "Jess M.", "Chris D.", "Taylor B.", "Mia S.",
];

const adCopyTemplates = [
  "I was SO skeptical about another skincare product... but after 2 weeks with GlowSkin, my skin has never looked better. The hyaluronic acid formula actually penetrates deep into the skin. If you're dealing with dryness, uneven tone, or fine lines — try this.",
  "Stop wasting money on products that don't work. GlowSkin's clinical formula is backed by dermatologists and has helped 50,000+ people achieve their best skin. See results in as little as 14 days.",
  "POV: You finally found the skincare routine that actually works. GlowSkin combines 5 clinical-grade ingredients in one simple step. No more 10-step routines. No more guessing.",
  "My dermatologist asked me what I've been doing differently... I showed her GlowSkin and she was actually impressed. Clinical-grade ingredients at a fraction of the price.",
  "Before GlowSkin, I spent $200+/month on skincare. Now I use one product that actually delivers. The retinol + niacinamide combo is chef's kiss.",
  "ALERT: GlowSkin just dropped their biggest sale of the year. 40% off everything. I've been using this for 6 months and my skin has never been clearer. Don't sleep on this.",
  "I was today years old when I learned that most skincare is just marketing. GlowSkin actually lists their clinical concentration levels. 2% retinol, 5% niacinamide, 1% hyaluronic acid. That's what actually matters.",
  "3 months ago, I couldn't go outside without foundation. Today, I'm bare-faced and confident. GlowSkin changed my relationship with my skin.",
];

const headlines = [
  "Dermatologist-Backed Formula",
  "Transform Your Skin in 14 Days",
  "Clinical Results. Simple Routine.",
  "50,000+ Happy Customers",
  "Your Best Skin Starts Here",
  "40% Off — Limited Time",
  "Finally, Skincare That Works",
  "One Product. Visible Results.",
];

// --- Campaign/Ad Set Structures ---
const campaignTemplates = [
  // TOF
  { name: "GS - TOF - Prospecting - Broad", objective: "OUTCOME_SALES", stage: "TOF" as const, adSets: ["Broad - 25-54 F", "Interest - Skincare", "LAL - Purchasers 1%", "LAL - ATC 1%", "Interest - Beauty"] },
  { name: "GS - TOF - Video Views - Content", objective: "VIDEO_VIEWS", stage: "TOF" as const, adSets: ["Broad - 18-44 F", "Interest - Clean Beauty", "LAL - Video Viewers 1%"] },
  { name: "GS - TOF - Cold - UGC Testing", objective: "OUTCOME_SALES", stage: "TOF" as const, adSets: ["Broad - 25-65 F", "Interest - Anti-Aging", "LAL - IC 1%", "Interest - Organic Skincare"] },
  // MOF
  { name: "GS - MOF - Retargeting - Engaged", objective: "OUTCOME_ENGAGEMENT", stage: "MOF" as const, adSets: ["Video Viewers 50%", "IG Engagers 30D", "Website Visitors 14D"] },
  { name: "GS - MOF - Warm - Social Proof", objective: "OUTCOME_LEADS", stage: "MOF" as const, adSets: ["Page Engagers 60D", "Video Viewers 75% 14D"] },
  // BOF
  { name: "GS - BOF - Purchase - ATC Retarget", objective: "CONVERSIONS", stage: "BOF" as const, adSets: ["ATC 7D", "IC 7D", "VC 3D"] },
  { name: "GS - BOF - DPA - Catalog", objective: "CATALOG_SALES", stage: "BOF" as const, adSets: ["DPA - All Products", "DPA - Bestsellers"] },
];

async function main() {
  console.log("Seeding database...");

  // Clean existing data
  await prisma.winRateCache.deleteMany();
  await prisma.creativeAnalysis.deleteMany();
  await prisma.performanceSnapshot.deleteMany();
  await prisma.analysisRun.deleteMany();
  await prisma.ad.deleteMany();
  await prisma.adSet.deleteMany();
  await prisma.campaign.deleteMany();
  await prisma.adAccount.deleteMany();
  await prisma.user.deleteMany();

  // Create demo user
  const hashedPassword = await bcrypt.hash("demo123", 12);
  const user = await prisma.user.create({
    data: {
      email: "demo@adpulse.io",
      password: hashedPassword,
      name: "Demo User",
    },
  });
  console.log("Created demo user:", user.email);

  // Create ad account
  const adAccount = await prisma.adAccount.create({
    data: {
      userId: user.id,
      metaAccountId: "act_demo_glowskin",
      metaAccountName: "GlowSkin Beauty Co.",
      accessToken: "demo_token_encrypted",
      status: "CONNECTED",
      lastSyncAt: new Date(),
    },
  });
  console.log("Created ad account:", adAccount.metaAccountName);

  let adCount = 0;

  for (const campaignTemplate of campaignTemplates) {
    const campaign = await prisma.campaign.create({
      data: {
        adAccountId: adAccount.id,
        metaCampaignId: `camp_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`,
        name: campaignTemplate.name,
        objective: campaignTemplate.objective,
        status: "ACTIVE",
        funnelStage: campaignTemplate.stage,
        lastSyncAt: new Date(),
      },
    });

    for (const adSetName of campaignTemplate.adSets) {
      const adSet = await prisma.adSet.create({
        data: {
          campaignId: campaign.id,
          metaAdSetId: `adset_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`,
          name: `${campaign.name} | ${adSetName}`,
          status: "ACTIVE",
          targetingSnapshot: JSON.stringify({ description: adSetName }),
        },
      });

      // Create 2-4 ads per ad set
      const numAds = randInt(2, 5);
      for (let i = 0; i < numAds; i++) {
        const template = pick(analysisTemplates);
        const isVideo = ["UGC_TALKING_HEAD", "UGC_TESTIMONIAL", "UGC_UNBOXING", "UGC_LIFESTYLE", "UGC_TUTORIAL", "FOUNDER_STORY"].includes(template.assetType);
        const creativeType = isVideo ? "VIDEO" : "IMAGE";

        // Performance varies by funnel stage and creative quality
        const qualityFactor = rand(0.3, 2.5); // Some ads are great, some are terrible
        const stageFactor = campaignTemplate.stage === "BOF" ? 1.8 : campaignTemplate.stage === "MOF" ? 1.2 : 1.0;

        const spend = rand(20, 5000) * (campaignTemplate.stage === "BOF" ? 0.6 : 1);
        const impressions = Math.floor(spend * rand(80, 200));
        const ctr = rand(0.005, 0.04) * qualityFactor * Math.min(stageFactor, 1.5);
        const clicks = Math.floor(impressions * ctr);
        const cpc = clicks > 0 ? spend / clicks : 0;
        const cpm = impressions > 0 ? (spend / impressions) * 1000 : 0;
        const roas = rand(0.3, 5.5) * qualityFactor * stageFactor;
        const purchaseValue = spend * roas;
        const purchases = Math.floor(purchaseValue / rand(35, 80));
        const costPerPurchase = purchases > 0 ? spend / purchases : 0;

        const hookRate = isVideo ? rand(0.1, 0.5) * Math.min(qualityFactor, 1.3) : 0;
        const holdRate = isVideo ? rand(0.05, 0.35) * Math.min(qualityFactor, 1.3) : 0;
        const videoViews = isVideo ? Math.floor(impressions * 0.4) : 0;
        const thruPlays = isVideo ? Math.floor(videoViews * holdRate) : 0;

        const creator = pick(creatorNames);
        const adName = `${pick(adNamePrefixes)} - ${template.assetType.replace(/_/g, " ")} - ${creator} - V${i + 1}`;

        const ad = await prisma.ad.create({
          data: {
            adSetId: adSet.id,
            metaAdId: `ad_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`,
            name: adName,
            status: pick(["ACTIVE", "ACTIVE", "ACTIVE", "PAUSED"]),
            creativeType: creativeType as any,
            thumbnailUrl: null,
            videoUrl: isVideo ? "https://example.com/video-placeholder" : null,
            imageUrl: !isVideo ? "https://example.com/image-placeholder" : null,
            adCopy: pick(adCopyTemplates),
            headline: pick(headlines),
            callToAction: pick(["SHOP_NOW", "LEARN_MORE", "SIGN_UP", "ORDER_NOW"]),
          },
        });

        // Create performance snapshot
        await prisma.performanceSnapshot.create({
          data: {
            adId: ad.id,
            date: new Date(),
            dateRange: "LIFETIME",
            spend,
            impressions,
            reach: Math.floor(impressions * rand(0.6, 0.9)),
            clicks,
            ctr,
            cpc,
            cpm,
            purchases,
            purchaseValue,
            roas,
            costPerPurchase,
            videoViews,
            thruPlays,
            hookRate,
            holdRate,
            videoAvgWatchTime: isVideo ? rand(2, 15) : 0,
            outboundClicks: Math.floor(clicks * rand(0.4, 0.8)),
            outboundCtr: ctr * rand(0.4, 0.8),
            addToCart: Math.floor(purchases * rand(1.5, 3)),
            atcRate: rand(0.01, 0.08),
            initiateCheckout: Math.floor(purchases * rand(1.1, 1.8)),
            frequency: rand(1.1, 3.5),
            uniqueClicks: Math.floor(clicks * rand(0.7, 0.95)),
            uniqueCtr: ctr * rand(0.7, 0.95),
          },
        });

        // Create a second snapshot for trend comparison
        await prisma.performanceSnapshot.create({
          data: {
            adId: ad.id,
            date: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000),
            dateRange: "SEVEN_DAY",
            spend: spend * rand(0.3, 0.6),
            impressions: Math.floor(impressions * rand(0.3, 0.6)),
            reach: Math.floor(impressions * rand(0.2, 0.5)),
            clicks: Math.floor(clicks * rand(0.3, 0.6)),
            ctr: ctr * rand(0.8, 1.2),
            cpc: cpc * rand(0.8, 1.2),
            cpm: cpm * rand(0.8, 1.2),
            purchases: Math.floor(purchases * rand(0.2, 0.5)),
            purchaseValue: purchaseValue * rand(0.2, 0.5),
            roas: roas * rand(0.7, 1.3),
            costPerPurchase: costPerPurchase * rand(0.8, 1.3),
            videoViews: Math.floor(videoViews * rand(0.3, 0.6)),
            thruPlays: Math.floor(thruPlays * rand(0.3, 0.6)),
            hookRate: hookRate * rand(0.8, 1.2),
            holdRate: holdRate * rand(0.8, 1.2),
            videoAvgWatchTime: isVideo ? rand(2, 15) : 0,
            outboundClicks: Math.floor(clicks * rand(0.2, 0.5)),
            outboundCtr: ctr * rand(0.3, 0.7),
            addToCart: Math.floor(purchases * rand(0.8, 2)),
            atcRate: rand(0.01, 0.06),
            initiateCheckout: Math.floor(purchases * rand(0.6, 1.2)),
            frequency: rand(1.0, 2.5),
            uniqueClicks: Math.floor(clicks * rand(0.5, 0.8)),
            uniqueCtr: ctr * rand(0.6, 0.9),
          },
        });

        // Create AI analysis
        await prisma.creativeAnalysis.create({
          data: {
            adId: ad.id,
            analyzedAt: new Date(),
            modelVersion: "claude-sonnet-4-20250514",
            assetType: template.assetType,
            messagingAngle: template.messagingAngle,
            hookTactic: template.hookTactic,
            visualStyle: template.visualStyle,
            ctaStyle: template.ctaStyle,
            emotionalTone: template.emotionalTone,
            productPresentation: template.productPresentation,
            hookTranscript: isVideo ? "Have you ever felt like no skincare product actually works?" : null,
            fullTranscript: null,
            copyAnalysis: JSON.stringify({
              hookStrength: randInt(4, 10),
              clarityOfOffer: randInt(5, 10),
              urgencyLevel: randInt(2, 9),
              socialProofPresent: Math.random() > 0.4,
              emotionalAppeal: randInt(4, 10),
              copyNotes: "Copy is well-structured with clear benefit hierarchy. The opening hook creates curiosity and the body delivers on the promise.",
            }),
            aiSummary: template.aiSummary,
            aiStrengths: JSON.stringify(template.aiStrengths),
            aiWeaknesses: JSON.stringify(template.aiWeaknesses),
            aiIterationIdeas: JSON.stringify(template.aiIterationIdeas),
            confidenceScore: randInt(70, 95),
          },
        });

        adCount++;
      }
    }
  }

  console.log(`Created ${adCount} ads with analyses`);

  // Compute win rate caches
  console.log("Computing win rate caches...");

  // Get all ads with data for win rate computation
  const allAds = await prisma.ad.findMany({
    include: {
      creativeAnalysis: true,
      performanceSnapshots: {
        where: { dateRange: "LIFETIME" },
        take: 1,
        orderBy: { createdAt: "desc" },
      },
      adSet: {
        include: {
          campaign: { select: { funnelStage: true } },
        },
      },
    },
  });

  // Account avg ROAS
  let totalSpend = 0;
  let weightedRoas = 0;
  for (const ad of allAds) {
    const snap = ad.performanceSnapshots[0];
    if (snap) {
      totalSpend += snap.spend;
      weightedRoas += snap.roas * snap.spend;
    }
  }
  const avgRoas = totalSpend > 0 ? weightedRoas / totalSpend : 0;

  const dimensions = [
    { key: "assetType", getter: (a: typeof allAds[0]) => a.creativeAnalysis?.assetType },
    { key: "messagingAngle", getter: (a: typeof allAds[0]) => a.creativeAnalysis?.messagingAngle },
    { key: "hookTactic", getter: (a: typeof allAds[0]) => a.creativeAnalysis?.hookTactic },
    { key: "visualStyle", getter: (a: typeof allAds[0]) => a.creativeAnalysis?.visualStyle },
    { key: "emotionalTone", getter: (a: typeof allAds[0]) => a.creativeAnalysis?.emotionalTone },
    { key: "productPresentation", getter: (a: typeof allAds[0]) => a.creativeAnalysis?.productPresentation },
  ];

  const funnelStages = ["ALL", "TOF", "MOF", "BOF"] as const;

  for (const dim of dimensions) {
    for (const stage of funnelStages) {
      const filteredAds = stage === "ALL"
        ? allAds
        : allAds.filter((a) => a.adSet.campaign.funnelStage === stage);

      const groups: Record<string, typeof allAds> = {};
      for (const ad of filteredAds) {
        const val = dim.getter(ad);
        if (!val) continue;
        if (!groups[val]) groups[val] = [];
        groups[val].push(ad);
      }

      for (const [value, ads] of Object.entries(groups)) {
        let groupSpend = 0;
        let groupRoasWeighted = 0;
        let groupCtrWeighted = 0;
        let groupImps = 0;
        let groupHookWeighted = 0;
        let groupHoldWeighted = 0;
        let groupVideoViews = 0;
        let wins = 0;
        let groupClicks = 0;
        let groupCpcWeighted = 0;

        for (const ad of ads) {
          const snap = ad.performanceSnapshots[0];
          if (!snap) continue;
          groupSpend += snap.spend;
          groupRoasWeighted += snap.roas * snap.spend;
          groupCtrWeighted += snap.ctr * snap.impressions;
          groupImps += snap.impressions;
          groupHookWeighted += snap.hookRate * snap.impressions;
          groupHoldWeighted += snap.holdRate * snap.videoViews;
          groupVideoViews += snap.videoViews;
          groupClicks += snap.clicks;
          groupCpcWeighted += snap.cpc * snap.clicks;
          if (snap.roas > avgRoas) wins++;
        }

        await prisma.winRateCache.create({
          data: {
            adAccountId: adAccount.id,
            dimension: dim.key,
            dimensionValue: value,
            funnelStage: stage,
            dateRange: "30D",
            adCount: ads.length,
            totalSpend: groupSpend,
            avgRoas: groupSpend > 0 ? groupRoasWeighted / groupSpend : 0,
            avgCtr: groupImps > 0 ? groupCtrWeighted / groupImps : 0,
            avgCpc: groupClicks > 0 ? groupCpcWeighted / groupClicks : 0,
            avgHookRate: groupImps > 0 ? groupHookWeighted / groupImps : 0,
            avgHoldRate: groupVideoViews > 0 ? groupHoldWeighted / groupVideoViews : 0,
            winRate: ads.length > 0 ? wins / ads.length : 0,
            computedAt: new Date(),
          },
        });
      }
    }
  }

  // Create additional win rate caches at different dates for trend lines
  const trendDates = [28, 21, 14, 7, 3].map((d) => {
    const date = new Date();
    date.setDate(date.getDate() - d);
    return date;
  });

  for (const dim of dimensions) {
    const groups: Record<string, boolean> = {};
    for (const ad of allAds) {
      const val = dim.getter(ad);
      if (val) groups[val] = true;
    }

    for (const value of Object.keys(groups)) {
      for (const date of trendDates) {
        // Slightly randomize win rates for trend variation
        const baseWinRate = rand(0.2, 0.8);
        const trendDirection = Math.random() > 0.5 ? 1 : -1;
        const dayOffset = (Date.now() - date.getTime()) / (24 * 60 * 60 * 1000);
        const winRate = Math.max(0, Math.min(1, baseWinRate + trendDirection * dayOffset * 0.005));

        await prisma.winRateCache.create({
          data: {
            adAccountId: adAccount.id,
            dimension: dim.key,
            dimensionValue: value,
            funnelStage: "ALL",
            dateRange: "7D",
            adCount: randInt(2, 15),
            totalSpend: rand(500, 5000),
            avgRoas: rand(0.8, 4.5),
            avgCtr: rand(0.008, 0.035),
            avgCpc: rand(0.5, 3.5),
            avgHookRate: rand(0.1, 0.4),
            avgHoldRate: rand(0.05, 0.25),
            winRate,
            computedAt: date,
          },
        });
      }
    }
  }

  // Create an analysis run record
  await prisma.analysisRun.create({
    data: {
      userId: user.id,
      adAccountId: adAccount.id,
      status: "COMPLETED",
      totalAds: adCount,
      analyzedAds: adCount,
      failedAds: 0,
      startedAt: new Date(Date.now() - 300000),
      completedAt: new Date(),
    },
  });

  console.log("Win rate caches computed");
  console.log(`\nSeed complete! Login with: demo@adpulse.io / demo123`);
}

main()
  .catch(console.error)
  .finally(() => prisma.$disconnect());
