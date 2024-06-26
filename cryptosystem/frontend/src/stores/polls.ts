import { writable } from 'svelte/store';

export type Candidate = {
    name: string,
    description: string,
    tally?: string,
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
  start_date: string,
  end_date: string,
  status: string,
}

export type CountyStatistics = {
  county: string,
  votes: number,
  percentage: number
}

export type VoteByDay = {
  votes: number,
  day: string
}

export type PollResults = {
  poll_id?: string,
  total_votes: number,
  candidates: Candidate[],
  county_statistics: CountyStatistics[],
  votes_this_week: VoteByDay[],
  status: string
}

export const polls = writable<Poll[] | Promise<any>>([]);