import { test, expect } from "@playwright/test";

test("page gives 200 status", async ({ page }) => {
  await page.goto("/");
  const status = await page.evaluate(() => {
    return fetch("/").then((response) => response.status);
  });
  expect(status).toBe(200);
});
test("page has a title", async ({ page }) => {
  await page.goto("/");
  const title = await page.title();
  expect(title).not.toBeFalsy();
});

test("check the nav", async ({ page }) => {
  await page.goto("/");
  let nav = await page.locator(".chakra-tabs");
  expect(nav).toBeTruthy();
  let tabs = await page.$$(".chakra-tab button.chakra-tabs__tab");
  let old_url = await page.url();
  for (let tab of tabs) {
    expect(await tab.textContent()).not.toBeFalsy();
    tab.click();
    await page.waitForNavigation();
    expect(await page.url()).not.toBe(old_url);
    old_url = await page.url();
  }
});
test("events button works", async ({ page }) => {
  await page.goto("/");
  let events_button = await page.locator(".chakra-button");
  expect(events_button).toBeTruthy();
  events_button.click();
  await page.waitForURL("/events");
  expect(await page.url()).toContain("/events");
});
test("login form works", async ({ page }) => {
  await page.goto("/");
  let login_button = await page.locator("button:has-text('Login')");
  expect(login_button).toBeTruthy();
  login_button.click();
  await page.waitForSelector("form");
  let form = await page.locator("form");
  expect(form).toBeTruthy();
  let email = await form.locator("input[name='email']");
  let password = await form.locator("input[name='password']");
  let submit = await form.locator("button[type='submit']");
  expect(email).toBeTruthy();
  expect(password).toBeTruthy();
  expect(submit).toBeTruthy();
  await email.fill("test@test.com");
  await password.fill("password");
  submit.click();
});
