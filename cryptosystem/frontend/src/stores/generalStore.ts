import { writable } from "svelte/store";

const isMobileStore = writable<boolean>(false);

export default isMobileStore;