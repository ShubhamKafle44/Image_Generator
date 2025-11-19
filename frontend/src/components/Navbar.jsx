import React, { useState } from "react";
import { UserButton } from "@clerk/clerk-react";

export default function Navbar({ pages, activePage, setActivePage }) {
    const [isOpen, setIsOpen] = useState(false);

    return (
        <nav className="bg-slate-900 p-4 flex justify-between items-center relative">
            {/* Logo / Brand */}
            <div className="text-white font-bold text-lg">ImageGen</div>

            {/* Desktop Menu */}
            <div className="hidden sm:flex gap-4 items-center">
                {pages.map((page) => (
                    <button
                        key={page}
                        onClick={() => setActivePage(page)}
                        className={`px-3 py-1 rounded ${activePage === page
                                ? "bg-purple-600"
                                : "bg-slate-700 hover:bg-slate-600"
                            }`}
                    >
                        {page.charAt(0).toUpperCase() + page.slice(1)}
                    </button>
                ))}

                {/* Profile Button */}
                <UserButton />
            </div>

            {/* Mobile Hamburger */}
            <div className="sm:hidden flex items-center gap-2">
                <UserButton />
                <button
                    onClick={() => setIsOpen(!isOpen)}
                    className="text-white focus:outline-none"
                >
                    {isOpen ? (
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
                                d="M6 18L18 6M6 6l12 12"
                            />
                        </svg>
                    ) : (
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
                                d="M4 6h16M4 12h16M4 18h16"
                            />
                        </svg>
                    )}
                </button>
            </div>

            {/* Mobile Menu */}
            {isOpen && (
                <div className="absolute top-16 left-0 w-full bg-slate-900 flex flex-col gap-2 p-4 sm:hidden z-10">
                    {pages.map((page) => (
                        <button
                            key={page}
                            onClick={() => {
                                setActivePage(page);
                                setIsOpen(false); // close menu after click
                            }}
                            className={`w-full text-left px-3 py-2 rounded ${activePage === page
                                    ? "bg-purple-600"
                                    : "bg-slate-700 hover:bg-slate-600"
                                }`}
                        >
                            {page.charAt(0).toUpperCase() + page.slice(1)}
                        </button>
                    ))}
                </div>
            )}
        </nav>
    );
}
