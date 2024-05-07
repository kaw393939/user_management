"use client";

import { ChakraProvider } from "@chakra-ui/react";

export function Providers({ children }: { children: React.ReactNode }) {
  return <ChakraProvider>{children}</ChakraProvider>;
}
// see the docs here
// https://v2.chakra-ui.com/getting-started/nextjs-app-guide
