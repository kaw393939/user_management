const NavBar = () => {
  let navItems = [
    { title: "Home", path: "/" },
    { title: "Find Events", path: "/events" },
    { title: "Create Event", path: "/create" },
    { title: "Login", path: "/login" },
    { title: "Register", path: "/register" },
  ];

  return (
    <nav className="nav flex justify-between items-center p-4">
      <h2>logo here</h2>
      <input
        type="search"
        name="search"
        id="searach"
        className="search border border-gray-300 rounded-lg pl-2"
        placeholder="Search"
      />
      <ul className="nav-list flex justify-center space-x-4">
        {navItems.map((item) => (
          <li key={item.title} className="nav-item inline-block">
            <a
              href={item.path}
              className="nav-link text-black hover:text-blue-500 font-bold"
            >
              {item.title}
            </a>
          </li>
        ))}
      </ul>
    </nav>
  );
};

export default NavBar;
