// src/components/Home.jsx
import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { SignedIn, SignedOut, useUser, SignInButton, SignUpButton } from '@clerk/clerk-react';

const Home = () => {
    const navigate = useNavigate();
    const { isSignedIn } = useUser();

    // Redirect signed-in users to dashboard
    useEffect(() => {
        if (isSignedIn) {
            navigate('/dashboard');
        }
    }, [isSignedIn, navigate]);

    return (
        <div className="flex items-center justify-center min-h-screen bg-gray-100">
            <div className="bg-white rounded-2xl shadow-xl p-10 max-w-md w-full text-center">
                <h1 className="text-3xl font-bold mb-6 text-gray-900">
                    Welcome to <span className="text-indigo-600">Image Generator</span>
                </h1>
                <p className="text-gray-600 mb-8">
                    Upload images and transform them with AI-powered magic.
                </p>

                <SignedOut>
                    <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
                        <SignInButton redirectUrl="/dashboard">
                            <button className="px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition">
                                Sign In
                            </button>
                        </SignInButton>

                        <SignUpButton redirectUrl="/dashboard">
                            <button className="px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition">
                                Sign Up
                            </button>
                        </SignUpButton>
                    </div>
                </SignedOut>

                <SignedIn>
                    <p className="text-gray-500 mt-4 animate-pulse">
                        Redirecting to your dashboard...
                    </p>
                </SignedIn>
            </div>
        </div>
    );
};

export default Home;
