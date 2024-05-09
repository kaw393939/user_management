"use client";
import { useFormState } from "react-dom";
import action from "./loginAction";
const FormElm = () => {
  const defaultData = {
    email: "",
    password: "",
  };
  const [state, formAction] = useFormState(action, defaultData); //default to system theme

  return (
    <form
      action={formAction}
      className="register-form bg-white relative min-h-96 border border-gray-300 rounded-lg p-4 flex flex-col justify-center items-center"
    >
      <input
        type="email"
        name="email"
        id="email"
        placeholder="Email"
        className="border border-gray-300 rounded-lg pl-2"
      />
      <input
        className="border border-gray-300 rounded-lg pl-2"
        type="password"
        name="password"
        id="password"
        placeholder="Password"
      />
      <button
        type="submit"
        className="bg-blue-500 text-white rounded-lg p-2 mt-4"
      >
        Login
      </button>
      <p>{state.detail?.map((d: { msg: any }) => d.msg).join(", ")}</p>
    </form>
  );
};

export default FormElm;
