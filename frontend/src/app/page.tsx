"use client";
import Image from "next/image";

export default function Home() {
  let isOpen = false;
  return (
    <>
      <div className=" bg-white text-white relative min-h-96">
        <h1 className="text-4xl font-bold text-center m-0 text-white absolute z-10 bottom-4 left-4">
          Welcome to the the Alumnni Network!
        </h1>
        <a
          href="/events"
          className="bg-teal-400 text-white text-xl font-bold p-2 rounded-lg absolute z-10 bottom-3 right-3"
        >
          Find Your Next Event
        </a>

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
