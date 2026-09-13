import { NextRequest, NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth";
import { exchangeCodeForToken, getLongLivedToken, getAdAccounts } from "@/lib/meta-api";
import { encrypt } from "@/lib/encryption";
import { prisma } from "@/lib/prisma";

export async function GET(req: NextRequest) {
  const session = await getServerSession(authOptions);
  if (!session?.user) {
    return NextResponse.redirect(new URL("/login", req.url));
  }

  const { searchParams } = new URL(req.url);
  const code = searchParams.get("code");
  const error = searchParams.get("error");

  if (error) {
    return NextResponse.redirect(
      new URL(`/onboarding?error=${error}`, req.url)
    );
  }

  if (!code) {
    return NextResponse.redirect(
      new URL("/onboarding?error=no_code", req.url)
    );
  }

  try {
    // Exchange code for short-lived token
    const shortToken = await exchangeCodeForToken(code);

    // Exchange for long-lived token
    const longToken = await getLongLivedToken(shortToken.access_token);

    // Get ad accounts
    const accountsData = await getAdAccounts(longToken.access_token);

    // Store each ad account
    for (const account of accountsData.data) {
      await prisma.adAccount.upsert({
        where: { metaAccountId: account.account_id },
        update: {
          accessToken: encrypt(longToken.access_token),
          tokenExpiresAt: new Date(
            Date.now() + longToken.expires_in * 1000
          ),
          status: "CONNECTED",
        },
        create: {
          userId: (session.user as any).id,
          metaAccountId: account.account_id,
          metaAccountName: account.name,
          accessToken: encrypt(longToken.access_token),
          tokenExpiresAt: new Date(
            Date.now() + longToken.expires_in * 1000
          ),
          status: "CONNECTED",
        },
      });
    }

    return NextResponse.redirect(new URL("/onboarding?step=2", req.url));
  } catch (error) {
    console.error("Meta OAuth callback error:", error);
    return NextResponse.redirect(
      new URL("/onboarding?error=oauth_failed", req.url)
    );
  }
}
