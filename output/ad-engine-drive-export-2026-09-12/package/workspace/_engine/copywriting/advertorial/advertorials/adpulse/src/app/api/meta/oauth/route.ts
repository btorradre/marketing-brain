import { NextRequest, NextResponse } from "next/server";
import { getMetaOAuthUrl } from "@/lib/meta-api";

export async function GET(req: NextRequest) {
  const oauthUrl = getMetaOAuthUrl();
  return NextResponse.redirect(oauthUrl);
}
