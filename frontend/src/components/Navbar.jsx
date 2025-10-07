import React, { useState } from "react";
import { FiMenu, FiX } from "react-icons/fi";

export default function Navbar({ pages, activePage, setActivePage }) {
    const [isMobileMenuOpen, setMobileMenuOpen] = useState(false);

    const handleLinkClick = (page) => {
        setActivePage(page);
        setMobileMenuOpen(false); // close menu on mobile
    };

    return (
        <nav className="w-full bg-slate-900 bg-opacity-90 backdrop-blur-md shadow-md fixed top-0 left-0 z-50">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between h-16 items-center">
                    {/* Logo / Brand */}
                    <div className="flex-shrink-0 text-white font-bold text-xl">
                        ImageGen
                    </div>

                    {/* Desktop Links */}
                    <div className="hidden md:flex space-x-6">
                        {pages.map((page) => (
                            <button
                                key={page}
                                className={`text-white font-medium hover:text-purple-400 ${activePage === page ? "text-purple-400" : ""
                                    }`}
                                onClick={() => handleLinkClick(page)}
                            >
                                {page.charAt(0).toUpperCase() + page.slice(1)}
                            </button>
                        ))}
                    </div>

                    {/* Mobile Menu Button */}
                    <div className="md:hidden">
                        <button
                            onClick={() => setMobileMenuOpen(!isMobileMenuOpen)}
                            className="text-white focus:outline-none"
                        >
                            {isMobileMenuOpen ? <FiX size={24} /> : <FiMenu size={24} />}
                        </button>
                    </div>
                </div>

                {/* Mobile Menu */}
                {isMobileMenuOpen && (
                    <div className="md:hidden bg-slate-900 bg-opacity-95 backdrop-blur-md mt-2 rounded shadow-lg">
                        {pages.map((page) => (
                            <button
                                key={page}
                                className={`block w-full text-left px-4 py-3 text-white font-medium hover:text-purple-400 ${activePage === page ? "text-purple-400" : ""
                                    }`}
                                onClick={() => handleLinkClick(page)}
                            >
                                {page.charAt(0).toUpperCase() + page.slice(1)}
                            </button>
                        ))}
                    </div>
                )}
            </div>
        </nav>
    );
}
