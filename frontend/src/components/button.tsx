import React from 'react';

type ButtonVariant = 'primary' | 'secondary' | 'outline';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
  className?: string;
  variant?: ButtonVariant;
}

const Button: React.FC<ButtonProps> = ({ 
  children, 
  className, 
  variant = 'primary',
  ...props 
}) => {
  const variants = {
    primary: "bg-yellow-400 text-black hover:bg-yellow-500 focus:outline-none",
    secondary: "bg-blue-600 text-white hover:bg-blue-700 focus:outline-none",
    outline: "border-2 border-yellow-400 text-yellow-400 hover:bg-yellow-400 hover:text-black focus:outline-none"
  };

  const baseStyle = "px-4 py-2 rounded-lg transition-all duration-200 font-semibold focus:ring-0 hover-bounce";
  
  return (
    <button 
      className={`${baseStyle} ${variants[variant]} ${className ?? ''}`}
      {...props}
    >
      {children}
    </button>
  );
};

export default Button;