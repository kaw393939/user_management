import React from "react";

const page = () => {
  return (
    <form className="register-form bg-white relative min-h-96 border border-gray-300 rounded-lg p-4 flex flex-col justify-center items-center">
      <h1 className="text-4xl font-bold text-center m-0 absolute z-10 bottom-4 left-4">
        Welcome to the the Alumnni Network!
      </h1>
      <input
        type="text"
        name="fname"
        id="fname"
        placeholder="First Name"
        className="border border-gray-300 rounded-lg pl-2"
      />
      <input
        type="text"
        name="lname"
        id="lname"
        placeholder="Last Name"
        className="border border-gray-300 rounded-lg pl-2"
      />
      <input
        type="email"
        name="email"
        id="email"
        placeholder="Email"
        className="border border-gray-300 rounded-lg pl-2"
      />
      <input
        className="border border-gray-300 rounded-lg pl-2"
        type="username"
        name="username"
        id="username"
        placeholder="Username"
      />
      <input
        className="border border-gray-300 rounded-lg pl-2"
        type="password"
        name="password"
        id="password"
        placeholder="Password"
      />
      <p>Are you a professional looking to provide lectures?*</p>
      <input type="radio" name="prof" id="prof1" value="prof1" />
      <label htmlFor="prof1">Yes</label>
      <input type="radio" name="prof" id="prof2" value="prof2" />
      <label htmlFor="prof2">No</label>
    </form>
  );
};

export default page;
