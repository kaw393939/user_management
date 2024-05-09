"use server";
import { cookies } from "next/headers";
import { redirect } from "next/navigation";
export default async function action(prevState: any, formData: FormData) {
  let payload = {
    email: formData.get("email") as string,
    password: formData.get("password") as string,
  };
  console.log(
    `username=${encodeURIComponent(
      payload.email
    )}&password=${encodeURIComponent(payload.password)}`
  );
  let setcookie = cookies();
  const response = await fetch("http://localhost/api/login/", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: `username=${encodeURIComponent(
      payload.email
    )}&password=${encodeURIComponent(payload.password)}`,
  });
  const data = await response.json();
  if (data.access_token) {
    setcookie.set("access_token", data.access_token);
    redirect("/profile");
  }
  return { ...prevState, ...data };
}
