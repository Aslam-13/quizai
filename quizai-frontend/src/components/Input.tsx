"use client";
import { useState, useEffect, useRef } from "react";

const quizIdeas = [
  "Create a quiz about the Low-Level System Design.",
  "Generate a quiz on the Data Structures and Algorithms.",
  "Make a quiz about Java OOP's.",
  "Design a quiz on similar structure of TCS NQT.",
  "Develop a quiz about High-Level System Design.",
];

export default function Input() {
  const [text, setText] = useState("");
  const [placeholderIndex, setPlaceholderIndex] = useState(0);
  const [animationClass, setAnimationClass] = useState('opacity-100 translate-y-0');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    const interval = setInterval(() => {
      setAnimationClass('opacity-0 -translate-y-5'); // Slide up and fade out

      setTimeout(() => {
        setPlaceholderIndex((prevIndex) => (prevIndex + 1) % quizIdeas.length);
        setAnimationClass('opacity-0 translate-y-5'); // Prepare to enter from bottom

        setTimeout(() => {
          setAnimationClass('opacity-100 translate-y-0'); // Slide in and fade in
        }, 50); // Short delay for class application
      }, 500); // Animation duration
    }, 4000);

    return () => clearInterval(interval);
  }, []);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Tab" && quizIdeas[placeholderIndex]) {
      e.preventDefault();
      setText(quizIdeas[placeholderIndex]);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const words = e.target.value.split(/\s+/).filter(Boolean);
    if (words.length <= 250) {
      setText(e.target.value);
    }
  };

  const handleSubmit = () => {
    console.log("Submitted:", text);
    setText("");
  };

  return (
    <div className="relative w-full max-w-2xl mx-auto">
      <div
        className="absolute top-4 left-4 text-gray-400 pointer-events-none"
        style={{ display: text ? "none" : "block" }}
      >
        <span
          className={`transition-all duration-500 ease-in-out inline-block ${animationClass}`}
        >
          {quizIdeas[placeholderIndex]}
        </span>
      </div>
      <textarea
        ref={textareaRef}
        value={text}
        onChange={handleChange}
        onKeyDown={handleKeyDown}
        placeholder=""
        className="w-full p-4 pr-20 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary resize-none bg-transparent relative z-10"
        rows={1}
        style={{
          minHeight: "48px",
          maxHeight: "200px",
        }}
      />
      <button
        onClick={handleSubmit}
        className="absolute right-2 top-1/2 -translate-y-1/2 p-2 rounded-full bg-primary text-white disabled:opacity-50 z-20"
        disabled={!text}
        style={{ backgroundColor: "var(--primary)" }}
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          className="h-6 w-6"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M5 10l7-7m0 0l7 7m-7-7v18"
          />
        </svg>
      </button>
    </div>
  );
}