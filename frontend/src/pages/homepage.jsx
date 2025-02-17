import { useNavigate } from 'react-router-dom';
import Button from '../components/button.tsx';
import Navbar_home from '../components/navbar_home.jsx';
export default function HomePage() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-blue-600 text-white">
      <Navbar_home/>
      {/* Hero Section */}
      <section className="flex flex-col items-center justify-center h-[80vh] text-center px-4">
        <h2 className="text-4xl md:text-6xl font-bold mb-4">Track your expenses, to the penny</h2>
        <p className="text-lg md:text-xl mb-6 max-w-2xl">
        Whether you're a group looking to split the bill or an individual aspiring to gain control over your finances, CliquePay has your back.
        </p>
        <Button className="bg-yellow-400 hover:bg-yellow-500 text-black px-6 py-3 text-lg font-semibold rounded-lg shadow-md">
          Get Started
        </Button>
      </section>
    </div>
  );
}
