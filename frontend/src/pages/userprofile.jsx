import Cookies from 'js-cookie';
import { useState, useEffect } from 'react';

export default function UserProfile() {
    const [user, setUser] = useState({
        name: 'John Doe',
        email: 'john@example.com',
        phone: '+1 (555) 123-4567',
        profilePicture: 'https://via.placeholder.com/150'
    });

    useEffect(() => {
        const fetchUserProfile = async () => {
            try {
                const id_token = Cookies.get('idToken');
                if (!id_token) {
                    navigate('/login');
                    return;
                }

                const response = await fetch('http://127.0.0.1:8000/api/user-profile/', {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ id_token }),
                });

                if (!response.ok) {
                    throw new Error('Failed to fetch user profile');
                }

                const data = await response.json();
                console.log(data)
                setUser(data.user_data);
            } catch (error) {
                console.error('Error fetching profile:', error);
            }
        };

        fetchUserProfile();
    }, []);

    return (
        <div className="min-h-screen bg-blue-600 text-white flex items-center justify-center">
            <div className="bg-white text-gray-800 rounded-lg shadow-xl p-8 max-w-md w-full">
                <div className="flex flex-col items-center">

                    <img 
                        src={user.profile_photo} 
                        alt="Profile"
                        className="w-32 h-32 rounded-full border-4 border-blue-600 mb-4"
                    />
                    
                    <div className="text-center">
                        <h1 className="text-2xl font-bold mb-2">{user.full_name}</h1>
                        <div className="space-y-2">
                            <div className="flex items-center justify-center gap-2">
                                <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207" />
                                </svg>
                                <span>{user.email}</span>
                            </div>
                            <div className="flex items-center justify-center gap-2">
                                <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                                </svg>
                                <span>{user.phone_number}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
