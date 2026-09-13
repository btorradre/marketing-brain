import Anthropic from "@anthropic-ai/sdk";

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY || "",
});

const ANALYSIS_PROMPT = `You are an expert direct response advertising analyst specializing in Meta (Facebook/Instagram) ads for DTC e-commerce brands.

Analyze this creative and provide your assessment in the following JSON structure. Return ONLY valid JSON, no other text.

{
  "assetType": "one of: UGC_TALKING_HEAD, UGC_LIFESTYLE, UGC_UNBOXING, UGC_TESTIMONIAL, UGC_TUTORIAL, STUDIO_PRODUCT_SHOT, STUDIO_LIFESTYLE, GRAPHIC_DESIGN, MEME, SLIDESHOW, BEFORE_AFTER, SPLIT_SCREEN, TEXT_OVERLAY, FOUNDER_STORY, OTHER",
  "messagingAngle": "one of: PROBLEM_SOLUTION, SOCIAL_PROOF, URGENCY_SCARCITY, ASPIRATIONAL, EDUCATIONAL, COMPARISON, EMOTIONAL_STORY, FEATURE_BENEFIT, PRICE_VALUE, TRANSFORMATION, AUTHORITY, CURIOSITY, FEAR_OF_MISSING, CONTRARIAN, LIFESTYLE",
  "hookTactic": "one of: QUESTION, BOLD_CLAIM, PATTERN_INTERRUPT, SOCIAL_PROOF_LEAD, BEFORE_AFTER_VISUAL, TEXT_HOOK, CONTROVERSY, RELATABLE_MOMENT, PRODUCT_IN_ACTION, UNBOXING_REVEAL, STATISTIC, TESTIMONIAL_LEAD, MOVEMENT_ACTION, ASMR_SENSORY, PROBLEM_CALLOUT",
  "visualStyle": "one of: BRIGHT_COLORFUL, DARK_MOODY, MINIMAL_CLEAN, RAW_AUTHENTIC, POLISHED_STUDIO, MEME_NATIVE, TEXT_HEAVY, LIFESTYLE_ASPIRATIONAL, BEFORE_AFTER, SPLIT_SCREEN",
  "ctaStyle": "one of: DIRECT_HARD_SELL, SOFT_CTA, NO_CTA, LINK_IN_BIO, LEARN_MORE, SHOP_NOW, LIMITED_TIME",
  "emotionalTone": "one of: EXCITING, CALM, URGENT, HUMOROUS, INSPIRATIONAL, FEARFUL, EDUCATIONAL, EMPATHETIC, CONFIDENT, CONTROVERSIAL",
  "productPresentation": "one of: HERO_SHOT, IN_USE, LIFESTYLE_CONTEXT, UNBOXING, COMPARISON, INGREDIENT_FOCUS, RESULT_FOCUS, MINIMAL_PRODUCT, NO_PRODUCT",
  "hookDescription": "Brief description of what happens in the first 3 seconds",
  "aiSummary": "2-3 sentence summary of the overall creative strategy and approach",
  "aiStrengths": ["strength 1", "strength 2", "strength 3"],
  "aiWeaknesses": ["weakness 1", "weakness 2"],
  "aiIterationIdeas": [
    {
      "idea": "Specific iteration idea",
      "reasoning": "Why this would likely improve performance",
      "priority": "HIGH or MEDIUM or LOW",
      "estimatedImpact": "Which metric this would most likely improve"
    }
  ],
  "copyAnalysis": {
    "hookStrength": 7,
    "clarityOfOffer": 8,
    "urgencyLevel": 5,
    "socialProofPresent": false,
    "emotionalAppeal": 6,
    "copyNotes": "Brief analysis of the ad copy effectiveness"
  },
  "confidenceScore": 85
}`;

export interface AnalysisResult {
  assetType: string;
  messagingAngle: string;
  hookTactic: string;
  visualStyle: string;
  ctaStyle: string;
  emotionalTone: string;
  productPresentation: string;
  hookDescription: string;
  aiSummary: string;
  aiStrengths: string[];
  aiWeaknesses: string[];
  aiIterationIdeas: Array<{
    idea: string;
    reasoning: string;
    priority: string;
    estimatedImpact: string;
  }>;
  copyAnalysis: {
    hookStrength: number;
    clarityOfOffer: number;
    urgencyLevel: number;
    socialProofPresent: boolean;
    emotionalAppeal: number;
    copyNotes: string;
  };
  confidenceScore: number;
}

export async function analyzeImageCreative(
  imageUrl: string,
  adCopy: string | null,
  headline: string | null,
  cta: string | null
): Promise<AnalysisResult> {
  const contextParts = [];
  if (adCopy) contextParts.push(`Primary text: ${adCopy}`);
  if (headline) contextParts.push(`Headline: ${headline}`);
  if (cta) contextParts.push(`CTA: ${cta}`);
  const adContext = contextParts.length > 0
    ? `\n\nHere is the ad copy:\n${contextParts.join("\n")}`
    : "";

  const response = await anthropic.messages.create({
    model: "claude-sonnet-4-20250514",
    max_tokens: 2000,
    messages: [
      {
        role: "user",
        content: [
          {
            type: "image",
            source: { type: "url", url: imageUrl },
          },
          {
            type: "text",
            text: `${ANALYSIS_PROMPT}${adContext}\n\nAnalyze this static image ad creative.`,
          },
        ],
      },
    ],
  });

  const text = response.content[0].type === "text" ? response.content[0].text : "";
  return parseAnalysisResponse(text);
}

export async function analyzeVideoCreative(
  frameUrls: string[],
  adCopy: string | null,
  headline: string | null,
  cta: string | null
): Promise<AnalysisResult> {
  const contextParts = [];
  if (adCopy) contextParts.push(`Primary text: ${adCopy}`);
  if (headline) contextParts.push(`Headline: ${headline}`);
  if (cta) contextParts.push(`CTA: ${cta}`);
  const adContext = contextParts.length > 0
    ? `\n\nHere is the ad copy:\n${contextParts.join("\n")}`
    : "";

  const imageContent = frameUrls.map((url, i) => ({
    type: "image" as const,
    source: { type: "url" as const, url },
  }));

  const response = await anthropic.messages.create({
    model: "claude-sonnet-4-20250514",
    max_tokens: 2000,
    messages: [
      {
        role: "user",
        content: [
          ...imageContent,
          {
            type: "text",
            text: `${ANALYSIS_PROMPT}${adContext}\n\nThese are key frames from a video ad creative at timestamps 0s, 1s, 3s, 5s, 10s. Analyze the full video creative.`,
          },
        ],
      },
    ],
  });

  const text = response.content[0].type === "text" ? response.content[0].text : "";
  return parseAnalysisResponse(text);
}

function parseAnalysisResponse(text: string): AnalysisResult {
  // Extract JSON from the response (handle markdown code blocks)
  const jsonMatch = text.match(/\{[\s\S]*\}/);
  if (!jsonMatch) {
    throw new Error("Failed to parse AI analysis response");
  }

  const parsed = JSON.parse(jsonMatch[0]);

  return {
    assetType: parsed.assetType || "OTHER",
    messagingAngle: parsed.messagingAngle || "FEATURE_BENEFIT",
    hookTactic: parsed.hookTactic || "PRODUCT_IN_ACTION",
    visualStyle: parsed.visualStyle || "MINIMAL_CLEAN",
    ctaStyle: parsed.ctaStyle || "SHOP_NOW",
    emotionalTone: parsed.emotionalTone || "CONFIDENT",
    productPresentation: parsed.productPresentation || "HERO_SHOT",
    hookDescription: parsed.hookDescription || "",
    aiSummary: parsed.aiSummary || "",
    aiStrengths: parsed.aiStrengths || [],
    aiWeaknesses: parsed.aiWeaknesses || [],
    aiIterationIdeas: parsed.aiIterationIdeas || [],
    copyAnalysis: parsed.copyAnalysis || {
      hookStrength: 5,
      clarityOfOffer: 5,
      urgencyLevel: 5,
      socialProofPresent: false,
      emotionalAppeal: 5,
      copyNotes: "",
    },
    confidenceScore: parsed.confidenceScore || 70,
  };
}
