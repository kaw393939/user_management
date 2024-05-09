"use client";
import { useFormState } from "react-dom";
import action from "./actions";
const FormElm = () => {
  const defaultData = {
    fname: "",
    lname: "",
    email: "",
    username: "",
    password: "",
    prof: "",
  };
  const [state, formAction] = useFormState(action, defaultData); //default to system theme

  return (
    <form
      action={formAction}
      className="register-form bg-white relative min-h-96 border border-gray-300 rounded-lg p-4 flex flex-col justify-center items-center"
    >
      {/* <h1 className="text-4xl font-bold text-center m-0 absolute z-10 bottom-4 left-4">
        Welcome to the the Alumnni Network!
      </h1> */}
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
      <button
        type="submit"
        className="bg-blue-500 text-white rounded-lg p-2 mt-4"
      >
        Register
      </button>
      <p>{state.detail?.map((d: { msg: any }) => d.msg).join(", ")}</p>
    </form>
  );
};

export default FormElm;
