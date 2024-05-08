"use server";
export default async function action(prevState: any, formData: FormData) {
  const response = await fetch("http://localhost:8000/api/register", {
    method: "POST",
    body: formData,
  });
  const data = await response.json();
  return { ...prevState, ...data };
}
