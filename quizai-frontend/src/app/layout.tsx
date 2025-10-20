import type { Metadata } from "next";
import { Zain } from "next/font/google";
import "./globals.css";

const zain = Zain({
  variable: "--font-zain-sans",
  subsets: ["latin"],
  weight: "400",
});

export const metadata: Metadata = {
  title: "QUESTY",
  description: "AI-Powered Fun Quizzes",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${zain.variable} ${zain.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
