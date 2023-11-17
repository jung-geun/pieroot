// @ts-nocheck
import { readable } from "svelte/store";

export const clock = readable(displayClockObject(), (set) => {
  const interval = setInterval(() => {
    set(displayClockObject());
  }, 100);

  return () => clearInterval(interval);
});

function displayClockObject() {
  let now = new Date();
  let timezoneOffset = now.getTimezoneOffset() / 60;
  let timezone =
    "GMT" +
    (timezoneOffset <= 0 ? "+" : "-") +
    Math.abs(timezoneOffset).toString().padStart(2, "0");
  let clock = {
    hour: now.getHours(),
    minute: now.getMinutes(),
    second: now.getSeconds(),
    millisecond: now.getMilliseconds(),
    period: now.getHours() < 12 ? "AM" : "PM",
    weekday: ["일", "월", "화", "수", "목", "금", "토"][now.getDay()],
    day: now.getDate(),
    month: now.getMonth() + 1,
    year: now.getFullYear(),
    timezone: timezone,
    unix: Math.floor(now.getTime() / 1000),
  };

  let clockString = "let clock = " + JSON.stringify(clock, null, 4) + ";";
  return clockString;
}
