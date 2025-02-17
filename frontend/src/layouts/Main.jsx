import { Outlet, Link } from 'react-router-dom';

function Main() {
  return (
    <div>
      <nav>
        <ul>
          <li><Link to="/">Home</Link></li>
          <li><Link to="/about">About</Link></li>
          <li><Link to="/contact">Contact</Link></li>
        </ul>
      </nav>

      {/* Outlet renders the child route components */}
      <main>
        <Outlet />
      </main>

      <footer>
        {/* Add your footer content here */}
      </footer>
    </div>
  );
}

export default Main;