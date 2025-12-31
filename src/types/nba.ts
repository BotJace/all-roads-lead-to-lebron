// TypeScript interfaces for NBA data structures

export interface PlayerCareerRecord {
  PLAYER_ID: number;
  SEASON_ID: string;
  LEAGUE_ID: string;
  TEAM_ID: number;
  TEAM_ABBREVIATION: string;
  PLAYER_AGE: number;
  GP: number;
  GS: number;
  MIN: number;
  FGM: number;
  FGA: number;
  FG_PCT: number;
  FG3M: number;
  FG3A: number;
  FG3_PCT: number;
  FTM: number;
  FTA: number;
  FT_PCT: number;
  OREB: number;
  DREB: number;
  REB: number;
  AST: number;
  STL: number;
  BLK: number;
  TOV: number;
  PF: number;
  PTS: number;
}

export interface TeamRosterRecord {
  TeamID: number;
  SEASON: string;
  LeagueID: string;
  PLAYER: string;
  NICKNAME: string;
  PLAYER_SLUG: string;
  NUM: string;
  POSITION: string;
  HEIGHT: string;
  WEIGHT: string;
  BIRTH_DATE: string;
  AGE: number;
  EXP: string;
  SCHOOL: string;
  PLAYER_ID: number;
  HOW_ACQUIRED: string | null;
}

// Graph node types
export type NodeType = 'player' | 'team-season';

export interface GraphNode {
  id: string;
  type: NodeType;
  label: string;
  // Player node data
  playerId?: number;
  playerName?: string;
  // Team-season node data
  teamId?: number;
  teamAbbr?: string;
  season?: string;
  // Visual properties
  x?: number;
  y?: number;
  vx?: number;
  vy?: number;
  fx?: number; // Fixed x-coordinate (for pinning nodes)
  fy?: number; // Fixed y-coordinate (for pinning nodes)
}

export interface GraphLink {
  source: string | GraphNode;
  target: string | GraphNode;
  // Relationship metadata
  season?: string;
  teamAbbr?: string;
}

