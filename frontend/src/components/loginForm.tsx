"use client";
import { useFormState } from "react-dom";
import action from "./loginAction";
import { Button, Input } from "@chakra-ui/react";
const FormElm = () => {
  const defaultData = {
    email: "",
    password: "",
  };
  const [state, formAction] = useFormState(action, defaultData); //default to system theme

  return (
    <form
      action={formAction}
      className="register-form bg-white relative border border-gray-300 rounded-lg p-4 flex flex-col gap-3 justify-center items-center"
    >
      {/* <input
        type="email"
        name="email"
        id="email"
        placeholder="Email"
        className="border border-gray-300 rounded-lg pl-2"
      /> */}
      <h2 className="text-start w-full font-bold">Welcome to WISClub</h2>
      <Input type="email" name="email" id="email" placeholder="Email" />
      {/* <input
        className="border border-gray-300 rounded-lg pl-2"
        type="password"
        name="password"
        id="password"
        placeholder="Password"
      /> */}
      <Input
        type="password"
        name="password"
        id="password"
        placeholder="Password"
      />

      {/* <button
        type="submit"
        className="bg-blue-500 text-white rounded-lg p-2 mt-4"
      >
        Logincd
      </button> */}
      <Button className="w-full" colorScheme="teal" type="submit">
        Continue
      </Button>
      <p>{state.detail&& JSON.stringify(state)}</p>
    </form>
  );
};

export default FormElm;
