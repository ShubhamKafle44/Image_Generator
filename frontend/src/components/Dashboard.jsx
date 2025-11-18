import { useUser, UserButton } from "@clerk/clerk-react";
import ImageGenerator from "./ImageGenerator";

export default function Dashboard() {
    const { user } = useUser();

    return (
        <div className="text-white">
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-3xl font-bold">Dashboard</h1>
                <UserButton />
            </div>

            <p>Welcome, {user?.firstName || "User"}!</p>
            <ImageGenerator />
        </div>
    );
}
