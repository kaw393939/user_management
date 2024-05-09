"use client";
import React from "react";
import Form from "@/components/loginForm";
import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
  Button,
  useDisclosure,
} from "@chakra-ui/react";

const Page = () => {
  const { isOpen, onOpen, onClose } = useDisclosure();
  return (
    <>
      <Button onClick={onOpen}>Open Modal</Button>

      <Modal isOpen={isOpen} onClose={onClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Welcome to WIS Club</ModalHeader>
          <ModalCloseButton />
          {/* <ModalBody>
            Lorem ipsum dolor, sit amet consectetur adipisicing elit. Aliquam
            culpa corporis molestiae minus consequuntur, porro quis nemo
            adipisci quibusdam temporibus reprehenderit deserunt cupiditate
            veritatis cum ea quaerat, a, assumenda corrupti.
          </ModalBody> */}
          <Form />;
          <ModalFooter>
            <Button colorScheme="blue" mr={3} onClick={onClose}>
              Close
            </Button>
            {/* <Button variant="ghost">Secondary Action</Button> */}
          </ModalFooter>
        </ModalContent>
      </Modal>
    </>
  );
};

export default Page;
