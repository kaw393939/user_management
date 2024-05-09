"use client";
import { usePathname, useRouter } from "next/navigation";
import Form from "@/components/regForm";
import Form2 from "@/components/loginForm";

import {
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalCloseButton,
  ModalFooter,
  Button,
  Modal,
  useDisclosure,
} from "@chakra-ui/react";
import { useState } from "react";
const NavBar = () => {
  const router = useRouter();
  const pathname = usePathname();
  console.log(pathname);
  let [formType, setFormType] = useState("login");
  let navItems = [
    {
      title: "Home",
      onclick: () => {
        router.push("/");
      },
      path: "/",
    },
    {
      title: "Find Events",
      onclick: () => {
        router.push("/events");
      },
      path: "/events",
    },
    {
      title: "Create Event",
      onclick: () => {
        router.push("/create");
      },
      path: "/create",
    },
    {
      title: "Profile",
      onclick: () => {
        router.push("/profile");
      },
      path: "/profile",
    },

    {
      title: "Login",
      onclick: () => {
        router.push("#login");
        setFormType("login");
        onOpen();
      },
      path: "#login",
    },

    {
      title: "Register",
      onclick: () => {
        router.push("#register");
        setFormType("register");
        onOpen();
      },
      path: "#register",
    },
  ];
  const { isOpen, onOpen, onClose } = useDisclosure();
  return (
    <>
      <Tabs
        colorScheme="teal"
        defaultIndex={navItems.findIndex((item) => pathname === item.path)}
      >
        <TabList>
          {navItems.map((item) => (
            <Tab onClick={item.onclick} key={item.title}>
              {item.title}
            </Tab>
          ))}
        </TabList>
      </Tabs>
      <Modal isOpen={isOpen} onClose={onClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Welcome to WIS Club</ModalHeader>
          <ModalCloseButton />
          {/* <Form /> */}
          {formType === "login" ? <Form2 /> : <Form />}
          {/* <ModalFooter> */}
          {/* <Button colorScheme="blue" mr={3} onClick={onClose}>
              Close
            </Button> */}
          {/* <Button variant="ghost">Secondary Action</Button> */}
          {/* </ModalFooter> */}
        </ModalContent>
      </Modal>
    </>
  );
};

export default NavBar;
