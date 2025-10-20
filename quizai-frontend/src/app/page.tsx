"use client";

import Input from "@/components/Input";

export default function Home() {
  return (
    <main className="flex h-[70vh] flex-col items-center justify-center p-24">
      <div className="w-full max-w-2xl">
      <h1 className="text-4xl font-bold text-center mb-8">Generate Quiz on any topic</h1>
      <Input />
      </div>
    </main>
  );
}