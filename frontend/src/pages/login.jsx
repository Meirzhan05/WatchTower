import React, { useState } from 'react';
import Button from '../components/button.tsx';
import { useNavigate } from "react-router-dom";
import Cookies from 'js-cookie'
function Login() {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        email: "", 
        password: "",
    });
    const [showPassword, setShowPassword] = useState(false);
    const [error, setError] = useState("");
    const [isLoading, setIsLoading] = useState(false);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
        setError("");
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setError("");

        if (!formData.email.trim()) {
            setError("Email is required");
            setIsLoading(false);
            return;
        }

        if (!formData.password) {
            setError("Password is required");
            setIsLoading(false);
            return;
        }

        try {
            const response = await fetch("http://127.0.0.1:8000/api/login/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                },
                body: JSON.stringify({
                    email: formData.email.trim(),
                    password: formData.password,
                }),
            });

            const data = await response.json();

            if (response.ok) {
                // Refresh token - long lived (365 days)
                Cookies.set('refreshToken', data.refresh_token, {
                    expires: 365,
                    secure: true,
                    sameSite: 'strict',
                    path: '/'
                });
                
                // ID token - short lived (1 hour)
                Cookies.set('idToken', data.id_token, {
                    expires: 1/24, // This evaluates to almost 0, should be 1/24
                    secure: true,
                    sameSite: 'strict',
                    path: '/'
                });
                
                // Access token - short lived (1 hour)
                Cookies.set('accessToken', data.access_token, {
                    expires: new Date(new Date().getTime() + 60 * 60 * 1000), // 1 hour in milliseconds
                    secure: true,
                    sameSite: 'strict',
                    path: '/'
                });

                navigate('/dashboard');
            } else {
                setError(data.message || "Login failed. Please check your credentials.");
            }
        } catch (err) {
            console.error("Network error:", err);
            setError("Cannot connect to server. Please try again.");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-blue-600 text-white flex items-center justify-center">
            <div className="bg-white text-black p-8 rounded-lg shadow-lg w-96">
                <h2 className="text-2xl font-bold mb-4 text-center">Login</h2>
                
                {error && (
                    <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-4">
                        <p className="text-red-700">{error}</p>
                    </div>
                )}

                <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                        <input
                            type="email"
                            name="email"
                            placeholder="Email"
                            value={formData.email}
                            onChange={handleChange}
                            className="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                            disabled={isLoading}
                        />
                    </div>
                    <div>
                        <input
                            type={showPassword ? "text" : "password"}
                            name="password"
                            placeholder="Password"
                            value={formData.password}
                            onChange={handleChange}
                            className="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                            disabled={isLoading}
                        />
                    </div>
                    <label className="flex items-center">
                        <input
                            type="checkbox"
                            checked={showPassword}
                            onChange={() => setShowPassword(!showPassword)}
                            className="mr-2"
                            disabled={isLoading}
                        />
                        <span className="text-sm">Show Password</span>
                    </label>
                    <Button 
                        className="w-full mt-4" 
                        type="submit"
                        disabled={isLoading}
                    >
                        {isLoading ? 'Logging in...' : 'Login'}
                    </Button>
                    <div className="text-center mt-4">
                        <p className="text-sm">
                            Don't have an account?{' '}
                            <a 
                                onClick={() => navigate('/signup')} 
                                className="text-blue-600 hover:text-blue-800 cursor-pointer"
                            >
                                Sign up
                            </a>
                        </p>
                        <p className="text-sm mt-2">
                            <a 
                                onClick={() => navigate('/reset-password')} 
                                className="text-blue-600 hover:text-blue-800 cursor-pointer"
                            >
                                Forgot Password?
                            </a>
                        </p>
                    </div>
                </form>
            </div>
        </div>
    );
}

export default Login;
