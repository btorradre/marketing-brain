import { NextRequest, NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth";
import { prisma } from "@/lib/prisma";

export async function GET(req: NextRequest) {
  const session = await getServerSession(authOptions);
  if (!session?.user) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const accounts = await prisma.adAccount.findMany({
    where: { userId: (session.user as any).id },
    select: {
      id: true,
      metaAccountId: true,
      metaAccountName: true,
      status: true,
      lastSyncAt: true,
    },
    orderBy: { createdAt: "desc" },
  });

  return NextResponse.json(accounts);
}
