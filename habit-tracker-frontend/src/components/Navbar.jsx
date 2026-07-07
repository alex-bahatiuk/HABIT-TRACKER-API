import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  return (
    <nav>
      <Link to="/dashboard">Dashboard</Link>
    

    {user ? (
       <>
           <span> {user.email}</span>
           <button onClick={handleLogout}>Logout</button>
       </>
    ) : (
       <span> Not logged in</span>
)}

    </nav>
  );
}
export default Navbar;