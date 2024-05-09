"use client";
import Image from "next/image";
import { Button, ButtonGroup } from "@chakra-ui/react";
import { useRouter } from "next/navigation";
export default function Home() {
  let isOpen = false;
  const router = useRouter();

  return (
    <>
      <div className=" bg-white text-white relative min-h-96">
        <h1 className="text-4xl font-bold text-center m-0 text-white absolute z-10 bottom-4 left-4">
          s Welcome to the the Alumnni Network!
        </h1>
        <Button
          colorScheme="teal"
          onClick={() => {
            router.push("/events");
          }}
          className="!absolute z-10 bottom-3 right-3"
        >
          Find Your Next Event
        </Button>
        <Image
          src="/pexels-photo-5940838 3.png"
          alt="Alumni Network"
          width={1500}
          height={100}
          className="w-full h-full absolute top-0 left-0"
        />
      </div>
    </>
  );
}
