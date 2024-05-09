"use server";
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
  console.log(data);

  return { ...prevState, ...data };
}
