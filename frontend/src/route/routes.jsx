import { createBrowserRouter } from "react-router-dom";
import HomePage from "../pages/homepage";
import SignupPage from "../pages/signup1";
import Verify from "../pages/verify";
import Login from "../pages/login";
import UserProfile from "../pages/userprofile";

const router = createBrowserRouter([
  {
    path: "/",    
    element: <HomePage />
  },
  {
    path:"/signup",
    element: < SignupPage/>
  },
  {
    path:"/verify",
    element: < Verify/>
  },
  {
    path:"/login",
    element: < Login/>
  },
  {
    path:"/profile",
    element: < UserProfile/>
  }
]);

export default router;