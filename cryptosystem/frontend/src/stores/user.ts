import { readable, writable } from "svelte/store";
import { browser } from "$app/environment";

type User = {
    _id: string;
    username: string;
    email: string;
    password: string;
    full_name: string;
    address: string;
    CNP: string;
} | null;

export const userToken = readable(browser && localStorage.getItem("access_token"));
const user = writable<User>();

export default user;