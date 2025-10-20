import type { Metadata } from "next";
import { Zain } from "next/font/google";
import "./globals.css";

const geistSans = Zain({
  variable: "--font-Zain-sans",
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
        className={`${geistSans.variable} ${geistSans.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
