import React from 'react'
import { useNavigate } from 'react-router-dom';
import Button from '../components/button.tsx';

function Navbar_home() {
    const navigate = useNavigate();

  return (
    <div>
      <nav className="bg-black max-h-[11vh] text-white p-4 flex justify-between items-center">
        <div className="flex items-center gap-6"> 
          <img 
            src="/images/Watchtower-no-words.png" 
            alt="WatchTower Logo" 
            className="h-27" // Increased from h-8 to h-24 (3x larger)
          />
          <h1 className="text-2xl font-semibold">CliquePay</h1>
        </div>
        <div className="flex gap-4 mr-8"> 
          <Button 
            className="bg-yellow-400 hover:bg-yellow-500 text-black"  
            onClick={() => navigate('/signup')}
          >
            Sign-up
          </Button>
          <Button 
            className="bg-yellow-400 hover:bg-yellow-500 text-black"
            onClick={() => navigate('/login')}          
          >
            Login
          </Button>
        </div>
      </nav>
    </div>
  )
}

export default Navbar_home
