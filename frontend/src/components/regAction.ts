"use server";

import { redirect } from "next/navigation";

export default async function action(prevState: any, formData: FormData) {
  let payload = {
    email: formData.get("email"),
    nickname: formData.get("username"),
    first_name: formData.get("fname"),
    last_name: formData.get("lname"),
    bio: "Experienced software developer specializing in web applications.",
    profile_picture_url: "https://example.com/profiles/john.jpg",
    linkedin_profile_url: "https://linkedin.com/in/johndoe",
    github_profile_url: "https://github.com/johndoe",
    role: "ANONYMOUS",
    password: formData.get("password"),
  };
  const response = await fetch("http://localhost/api/register/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },

    body: JSON.stringify(payload),
  });
  const data = await response.json();
  if (data.status === 201 || data.status === 200 || data.status === 204) {
    return { ...prevState, ...data, close: true } && redirect("/");
  }
  return { ...prevState, ...data };
}
