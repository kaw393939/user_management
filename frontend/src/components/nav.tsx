"use client";
import { useRouter } from "next/navigation";
import { Tabs, TabList, TabPanels, Tab, TabPanel } from "@chakra-ui/react";
const NavBar = () => {
  let navItems = [
    { title: "Home", path: "/" },
    { title: "Find Events", path: "/events" },
    { title: "Create Event", path: "/create" },
    { title: "Login", path: "/login" },
    { title: "Register", path: "/register" },
  ];
  const router = useRouter();
  return (
    <Tabs colorScheme="teal">
      <TabList>
        {navItems.map((item) => (
          <Tab
            onClick={() => {
              router.push(item.path);
            }}
            key={item.title}
          >
            {item.title}
          </Tab>
        ))}
      </TabList>
    </Tabs>
  );
};

export default NavBar;
