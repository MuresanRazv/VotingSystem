import { readable, writable } from "svelte/store";
import { browser } from "$app/environment";

type User = {
    _id: string;
    username: string;
    email: string;
    password: string;
    firstname: string;
    lastname: string;
    county: string;
    city: string;
    CNP: string;
};

export const userToken = readable(browser && localStorage.getItem("access_token"));
const user = writable<User>({
    _id: "",
    username: "",
    email: "",
    password: "",
    firstname: "",
    lastname: "",
    county: "",
    city: "",
    CNP: ""
});

export default user;