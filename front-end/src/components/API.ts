import axios from 'axios';
import Phase from '../Phase';

class API {
    static endpoint = "http://127.0.0.1:8000";

    static async get(module: string, method: string) {
        const response = await axios.get(`${this.endpoint}/${module}/${method}`)
        return response.data;
    }

    static async post(module: string, method: string, data?: Object) {
        return await axios.post(`${this.endpoint}/${module}/${method}`, data);
    }

    static async getCurrentGame(): Promise<{game: number}> {
        return await this.get('viewer', 'game');
    }

    static async getPrompt(game: number): Promise<{prompt: string}> {
        return await this.get('viewer', `game/${game}`);
    }

    static async getPhase(game: number): Promise<{phase: string}> {
        return await this.get('viewer', `phase/${game}`);
    }

    static async getAllPlayers(): Promise<{players: string[]}> {
        return await this.get('viewer', 'players');
    }

    static async getAllSongs(): Promise<{songs: string[]}> {
        return await this.get('viewer', 'songs');
    }

    static async getVotesForSong(song: string): Promise<{votes: number}> {
        return await this.get('viewer', `votes/${song}`);
    }

    static async addPlayerList(player: string, songs: string[]) {
        return await this.post('list', 'add', {player, songs})
    }

    static async vote(songs: string[]) {
        return await this.post('vote', '', {songs});
    }
}

export default API