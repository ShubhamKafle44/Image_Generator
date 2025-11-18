import React, { useState } from "react";
import { FiMenu, FiX } from "react-icons/fi";
import { UserButton } from "@clerk/clerk-react";

export default function Navbar({ pages, activePage, setActivePage }) {
    const [isMobileMenuOpen, setMobileMenuOpen] = useState(false);

    const handleLinkClick = (page) => {
        setActivePage(page);
        setMobileMenuOpen(false);
        const section = document.getElementById(page);
        section?.scrollIntoView({ behavior: "smooth" });
    };

    return (
        <nav className="w-full fixed top-0 left-0 z-50 bg-slate-900 text-white shadow-md">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between h-16 items-center">
                    {/* Logo */}
                    <div className="font-bold text-xl">ImageGen</div>

                    {/* Desktop Links + UserButton */}
                    <div className="hidden md:flex items-center space-x-6 flex-1 justify-end">
                        {pages.map((page) => (
                            <button
                                key={page}
                                className={`font-medium hover:text-purple-400 ${activePage === page ? "text-purple-400" : ""
                                    }`}
                                onClick={() => handleLinkClick(page)}
                            >
                                {page.charAt(0).toUpperCase() + page.slice(1)}
                            </button>
                        ))}

                        {/* UserButton at far right */}
                        <div className="ml-4">
                            <UserButton />
                        </div>
                    </div>

                    {/* Mobile Menu Button */}
                    <div className="md:hidden">
                        <button
                            onClick={() => setMobileMenuOpen(!isMobileMenuOpen)}
                            className="focus:outline-none"
                        >
                            {isMobileMenuOpen ? <FiX size={24} /> : <FiMenu size={24} />}
                        </button>
                    </div>
                </div>

                {/* Mobile Menu */}
                {isMobileMenuOpen && (
                    <div className="md:hidden bg-slate-800">
                        {pages.map((page) => (
                            <button
                                key={page}
                                className={`block w-full text-left px-4 py-3 hover:text-purple-400 ${activePage === page ? "text-purple-400" : ""
                                    }`}
                                onClick={() => handleLinkClick(page)}
                            >
                                {page.charAt(0).toUpperCase() + page.slice(1)}
                            </button>
                        ))}

                        <div className="flex px-4 py-3 border-t border-slate-700 items-center gap-2">
                            <UserButton />
                            <p>Profile</p>
                        </div>
                    </div>
                )}
            </div>
        </nav>
    );
}
