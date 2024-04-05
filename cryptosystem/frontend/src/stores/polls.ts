import { writable } from 'svelte/store';

export type Candidate = {
    name: string,
    description: string,
  }
  

export type Poll = {
    _id?: string,
    title: string,
    description: string,
    candidates: Candidate[],
    created_at: string,
    updated_at: string,
    is_private: boolean,
    multiple_choice: boolean,
  }

export const polls = writable<Poll[] | Promise<any>>([]);