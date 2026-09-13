"use client";

import { SessionProvider } from "next-auth/react";
import { Toaster } from "react-hot-toast";
import { TooltipProvider } from "@/components/ui/tooltip";

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <SessionProvider>
      <TooltipProvider>
        {children}
        <Toaster
          position="top-right"
          toastOptions={{
            style: {
              background: "hsl(222 47% 8%)",
              color: "hsl(210 40% 98%)",
              border: "1px solid hsl(217 33% 17%)",
            },
          }}
        />
      </TooltipProvider>
    </SessionProvider>
  );
}
