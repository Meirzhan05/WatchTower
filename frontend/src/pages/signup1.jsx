import { useState, useEffect } from "react";
import Button from '../components/button.tsx';
import { useNavigate } from "react-router-dom";
import Cookies from 'js-cookie';

export default function SignupPage() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    fullname: "",
    phoneNumber: "",
    password: "",
    confirmPassword: "",
  });
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  useEffect(() => {
    if (!navigator.cookieEnabled) {
      setError("Cookies are disabled. Please enable cookies to sign up.");
    }
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    setError("");
  };

  const validatePhoneNumber = (number) => {
    if (!number) return true; 
    const phoneRegex = /^\+?1?\d{9,15}$/;
    return phoneRegex.test(number);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError("");

    if (!formData.username.trim()) {
      setError("Username is required");
      setIsLoading(false);
      return;
    }

    if (!formData.email.trim()) {
      setError("Email is required");
      setIsLoading(false);
      return;
    }

    if (!formData.fullname.trim()) {
      setError("Full name is required");
      setIsLoading(false);
      return;
    }

    if (!formData.password) {
      setError("Password is required");
      setIsLoading(false);
      return;
    }

    if (formData.password !== formData.confirmPassword) {
      setError("Passwords do not match");
      setIsLoading(false);
      return;
    }

    if (formData.phoneNumber.trim() && !validatePhoneNumber(formData.phoneNumber.trim())) {
      setError("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.");
      setIsLoading(false);
      return;
    }

    const requestBody = {
      username: formData.username.trim(),
      email: formData.email.trim(),
      fullname: formData.fullname.trim(),
      password: formData.password,
      phone_number: formData.phoneNumber.trim() || null,
    };

    try {
      const response = await fetch("http://127.0.0.1:8000/api/signup/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Accept": "application/json",
        },
        body: JSON.stringify(requestBody),
      });

      console.log('Response status:', response.status);
      const data = await response.json();
      console.log('Response data:', data);
    

      if (response.ok) {
        try {
          Cookies.set('username', formData.username, {
            expires: 365, // 1 year
            path: '/', // accessible on all paths
            sameSite: 'Lax',
            secure: window.location.protocol === 'https:',
          });
      
          const storedUsername = Cookies.get('username');
          if (!storedUsername) {
            throw new Error('Failed to store username');
          }
          
          // a small delay to ensure cookie is set
          setTimeout(() => {
            navigate('/verify');
          }, 100);
        } catch (storageError) {
          console.error('Storage error:', storageError);
          setError('Failed to store user data. Please check your browser settings.');
          setIsLoading(false);
        }
      
      } else {
        if (response.status === 400) {
          setError(data.message || "Please check your input data");
        } else if (response.status === 409) {
          setError("Username or email already exists");
        } else {
          setError(data.message || "Registration failed");
        }
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
        <h2 className="text-2xl font-bold mb-4 text-center">Sign Up</h2>
        {error && (
          <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-4">
            <p className="text-red-700">{error}</p>
          </div>
        )}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <input
              type="text"
              name="username"
              placeholder="Username"
              value={formData.username}
              onChange={handleChange}
              className="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              disabled={isLoading}
            />
          </div>
          <div>
            <input
              type="email"
              name="email"
              placeholder="Email Address"
              value={formData.email}
              onChange={handleChange}
              className="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              disabled={isLoading}
            />
          </div>
          <div>
            <input
              type="text"
              name="fullname"
              placeholder="Full Name"
              value={formData.fullname}
              onChange={handleChange}
              className="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              disabled={isLoading}
            />
          </div>
          <div>
            <input
              type="tel"
              name="phoneNumber"
              placeholder="Phone Number (optional)"
              value={formData.phoneNumber}
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
          <div>
            <input
              type={showPassword ? "text" : "password"}
              name="confirmPassword"
              placeholder="Confirm Password"
              value={formData.confirmPassword}
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
            {isLoading ? 'Signing up...' : 'Sign Up'}
          </Button>
        </form>
      </div>
    </div>
  );
}