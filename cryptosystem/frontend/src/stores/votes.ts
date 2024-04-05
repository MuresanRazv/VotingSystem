import { writable } from 'svelte/store';
import type { Candidate } from './polls';

export type Vote = {
    _id?: string,
    poll_id: string,
    user_id: string,
    candidates: Candidate[],
}

export const votes = writable<Vote[]>([]);