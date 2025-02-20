// TODO: add the ability to update user profile

import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"
import Cookies from "js-cookie"
import { Mail, Phone, Calendar, DollarSign, Clock } from "lucide-react"

const UserProfile = () => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const navigate = useNavigate()

  useEffect(() => {
    const fetchUserProfile = async () => {
      try {
        const id_token = Cookies.get("idToken")
        if (!id_token) {
          navigate("/login")
          return
        }

        const response = await fetch("http://127.0.0.1:8000/api/user-profile/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ id_token }),
        })

        if (!response.ok) {
          throw new Error("Failed to fetch user profile")
        }

        const data = await response.json()
        setUser(data.user_data)
        setLoading(false)
      } catch (error) {
        console.error("Error fetching profile:", error)
        setError("Failed to load user profile. Please try again later.")
        setLoading(false)
      }
    }

    fetchUserProfile()
  }, [navigate])

  if (loading) {
    return <div className="flex justify-center items-center h-screen text-2xl text-white bg-blue-800">Loading...</div>
  }

  if (error) {
    return <div className="flex justify-center items-center h-screen text-2xl text-white bg-blue-800">{error}</div>
  }

  if (!user) {
    return (
      <div className="flex justify-center items-center h-screen text-2xl text-white bg-blue-800">
        No user data available.
      </div>
    )
  }

  return (
    <div className="bg-blue-800 text-white min-h-screen flex flex-col items-center p-8 font-sans">
      <div className="flex flex-col items-center mb-8">
        <img
          src={user.profile_photo || "/placeholder.svg?height=150&width=150"}
          alt={user.full_name}
          className="w-36 h-36 rounded-full object-cover border-4 border-white mb-4"
        />
        <h1 className="text-3xl font-bold mb-2">{user.full_name}</h1>
        <p className="text-xl text-blue-200">@{user.username}</p>
      </div>
      <div className="bg-blue-900 rounded-lg p-8 w-full max-w-md shadow-lg">
        <InfoItem icon={<Mail className="text-blue-300" size={20} />} text={user.email} />
        <InfoItem icon={<Phone className="text-blue-300" size={20} />} text={user.phone_number || "Not provided"} />
        <InfoItem
          icon={<DollarSign className="text-blue-300" size={20} />}
          text={`Preferred Currency: ${user.currency}`}
        />
        <InfoItem
          icon={<Calendar className="text-blue-300" size={20} />}
          text={`Joined: ${new Date(user.created_at).toLocaleDateString()}`}
        />
        <InfoItem
          icon={<Clock className="text-blue-300" size={20} />}
          text={`Last Updated: ${new Date(user.updated_at).toLocaleDateString()}`}
        />
      </div>
    </div>
  )
}

const InfoItem = ({ icon, text }) => (
  <div className="flex items-center mb-4 last:mb-0">
    <span className="mr-4">{icon}</span>
    <span className="text-blue-100">{text}</span>
  </div>
)

export default UserProfile